#!/usr/bin/env python3
"""Small, auditable PubMed retrieval. Python 3.10+, standard library only.

Retrieves metadata/abstracts, never verifies medical claims or claims exhaustive
literature coverage. See references/api-tools.md for limits and usage policy.
"""
import argparse
from datetime import date, datetime, timezone
import json
import os
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

BASE = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
_last_request = 0.0


def now():
    return datetime.now(timezone.utc).isoformat()


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def fetch(endpoint, params):
    global _last_request
    params = dict(params, tool='med-go-clinical-evidence')
    if os.environ.get('NCBI_EMAIL'):
        params['email'] = os.environ['NCBI_EMAIL']
    url = BASE + endpoint + '?' + urllib.parse.urlencode(params)
    for attempt in range(3):
        time.sleep(max(0, 0.4 - (time.monotonic() - _last_request)))
        _last_request = time.monotonic()
        req = urllib.request.Request(url, headers={'User-Agent': 'med-go-clinical-evidence/0.1.0'})
        try:
            with urllib.request.urlopen(req, timeout=25) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 500, 502, 503, 504) and attempt < 2:
                time.sleep(attempt + 1)
                continue
            raise RuntimeError(f'HTTP {exc.code}: retrieval failed; not zero results') from None
        except (urllib.error.URLError, TimeoutError, OSError):
            if attempt < 2:
                time.sleep(attempt + 1)
                continue
            raise RuntimeError('Network/timeout failure; not zero results') from None


def text_of(node):
    return ''.join(node.itertext()).strip() if node is not None else ''


def author_name(node):
    collective = text_of(node.find('CollectiveName'))
    given = text_of(node.find('ForeName')) or text_of(node.find('Initials'))
    return collective or ' '.join(p for p in (given, text_of(node.find('LastName'))) if p)


def date_text(node):
    return ' '.join(text_of(part) for part in node) if node is not None else ''


def parse_records(raw):
    root = ET.fromstring(raw)
    if root.tag != 'PubmedArticleSet' or root.find('.//ERROR') is not None:
        raise ValueError('Unexpected EFetch XML or API error')
    records = []
    for node in root:
        if node.tag not in ('PubmedArticle', 'PubmedBookArticle'):
            continue
        is_article = node.tag == 'PubmedArticle'
        citation = node.find('MedlineCitation' if is_article else 'BookDocument')
        if citation is None:
            raise ValueError('EFetch record missing citation container')
        article = citation.find('Article') if is_article else citation
        if article is None:
            raise ValueError('EFetch record missing article container')
        pmid = text_of(citation.find('PMID'))
        if not pmid:
            raise ValueError('EFetch record missing PMID')
        identifiers = {}
        id_path = ('PubmedData' if is_article else 'PubmedBookData') + '/ArticleIdList/ArticleId'
        for element in node.findall(id_path):
            identifiers.setdefault(element.get('IdType', 'unknown'), []).append(text_of(element))
        abstract = [{'label': part.get('Label', ''), 'text': text_of(part)}
                    for part in article.findall('Abstract/AbstractText')]
        records.append({
            'pmid': pmid, 'record_type': node.tag,
            'title': text_of(article.find('ArticleTitle')),
            'journal': text_of(article.find('Journal/Title')),
            'publication_date': date_text(article.find('Journal/JournalIssue/PubDate')),
            'article_dates': [{'type': d.get('DateType', ''), 'value': date_text(d)}
                              for d in article.findall('ArticleDate')],
            'authors': [author_name(a) for a in article.findall('AuthorList/Author')],
            'identifiers': identifiers, 'abstract': abstract,
            'publication_types': [text_of(p) for p in article.findall('PublicationTypeList/PublicationType')],
            'correction_links': [{'type': c.get('RefType', ''),
                                  'pmid': text_of(c.find('PMID')),
                                  'source': text_of(c.find('RefSource'))}
                                 for c in citation.findall('CommentsCorrectionsList/CommentsCorrections')],
            'source_url': f'https://pubmed.ncbi.nlm.nih.gov/{pmid}/',
            'retrieval_level': 'abstract' if any(a['text'] for a in abstract) else 'metadata',
            'identity_status': 'unresolved', 'claim_status': 'not_assessed',
            'human_review': 'not_requested',
        })
    return records


def run(query, until, max_records, output, transport=fetch):
    date.fromisoformat(until)
    if not query.strip() or not 1 <= max_records <= 500:
        raise ValueError('Nonempty query and max_records between 1 and 500 required')
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    full_query = f'({query.strip()}) AND ("1000/01/01"[dp] : "{until.replace("-", "/")}"[dp])'
    log = {'schema_version': '1', 'started_at': now(), 'ended_at': None,
           'database': 'PubMed', 'platform': 'NCBI E-utilities',
           'query_original': query.strip(), 'query_executed': full_query,
           'date_field': 'Publication Date [dp]', 'end_date': until,
           'max_records': max_records, 'sort': 'pub_date', 'status': 'failed',
           'reported_count': None, 'retrieved_count': 0, 'query_translation': None,
           'selected_pmids': [], 'missing_pmids': [], 'unexpected_pmids': [],
           'duplicate_pmids': [], 'warnings': {}, 'capped': False,
           'retrieval_complete_for_query': False,
           'scope_note': 'Query retrieval only; not a complete literature review or claim verification'}
    records = []
    try:
        raw = transport('esearch.fcgi', {'db': 'pubmed', 'retmode': 'json',
                        'term': full_query, 'retmax': max_records, 'sort': 'pub_date'})
        (output / 'esearch.json').write_bytes(raw)
        payload = json.loads(raw)
        data = payload.get('esearchresult')
        if payload.get('error') or not isinstance(data, dict) or data.get('ERROR') or data.get('errorlist'):
            raise ValueError('ESearch error or invalid response; inspect raw file')
        count = int(data['count'])
        ids = data['idlist']
        if count < 0 or not isinstance(ids, list) or any(not str(i).isdigit() for i in ids):
            raise ValueError('Invalid ESearch count or identifiers')
        if len(ids) != len(set(ids)) or len(ids) > min(count, max_records):
            raise ValueError('Inconsistent ESearch identifiers')
        log.update(reported_count=count, selected_pmids=ids,
                   query_translation=data.get('querytranslation'),
                   warnings=data.get('warninglist', {}), capped=count > max_records)
        for offset in range(0, len(ids), 200):
            raw = transport('efetch.fcgi', {'db': 'pubmed', 'retmode': 'xml',
                            'id': ','.join(ids[offset:offset + 200])})
            (output / f'efetch-{offset // 200 + 1}.xml').write_bytes(raw)
            records.extend(parse_records(raw))
        got = [r['pmid'] for r in records]
        log['missing_pmids'] = sorted(set(ids) - set(got))
        log['unexpected_pmids'] = sorted(set(got) - set(ids))
        log['duplicate_pmids'] = sorted({i for i in got if got.count(i) > 1})
        complete = (count == len(ids) == len(got)
                    and not log['missing_pmids'] and not log['unexpected_pmids']
                    and not log['duplicate_pmids'])
        log['retrieval_complete_for_query'] = complete
        log['status'] = 'completed' if complete else 'partial'
    except (RuntimeError, ValueError, KeyError, TypeError, ET.ParseError, OSError) as exc:
        log['error'] = str(exc)
        log['status'] = 'partial' if log['reported_count'] is not None else 'failed'
        got = {r['pmid'] for r in records}
        log['missing_pmids'] = sorted(set(log['selected_pmids']) - got)
    log['retrieved_count'] = len(records)
    log['ended_at'] = now()
    write_json(output / 'records.json', records)
    write_json(output / 'run.json', log)
    return log


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--query-file', required=True, type=Path)
    parser.add_argument('--until', required=True, help='YYYY-MM-DD, Publication Date cutoff')
    parser.add_argument('--max-records', type=int, default=50)
    parser.add_argument('--out', required=True, type=Path, help='New output directory')
    args = parser.parse_args()
    try:
        result = run(args.query_file.read_text(encoding='utf-8-sig'), args.until,
                     args.max_records, args.out)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print(json.dumps({k: result[k] for k in ('status', 'reported_count', 'retrieved_count',
                     'capped', 'retrieval_complete_for_query')}, ensure_ascii=True))
    return 0 if result['status'] == 'completed' else 2


if __name__ == '__main__':
    raise SystemExit(main())
