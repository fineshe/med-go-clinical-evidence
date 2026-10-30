"""Search bundled bibliographic candidates offline; results are not verified clinical recommendations."""
import argparse,json
from pathlib import Path

CATALOG=Path(__file__).resolve().parents[1]/'references/guidelines/catalog.jsonl'
DEFAULT_KINDS={'指南候选','推荐/规范候选','共识/立场声明'}

def search(path,terms=(),specialty=None,include_other=False):
    with Path(path).open(encoding='utf8') as f:
        for line in f:
            r=json.loads(line)
            if not include_other and r['document_kind'] not in DEFAULT_KINDS:continue
            if '非医学数据' in r['specialties']:continue
            if specialty and not any(specialty.casefold() in d.casefold() for d in r['specialties']):continue
            text=' '.join([r['title_zh'],r['title_en'],r['issuing_body_as_supplied'],r['doi'] or '',r['pmid'] or '']).casefold()
            if all(term.casefold() in text for term in terms):yield r

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--query',action='append',default=[],help='Literal substring; repeated options are AND. Run synonym variants separately.')
    p.add_argument('--specialty');p.add_argument('--include-other',action='store_true')
    p.add_argument('--limit',type=int,default=20);p.add_argument('--list-specialties',action='store_true')
    a=p.parse_args()
    if a.limit<1 or a.limit>200:p.error('limit must be 1..200')
    if a.list_specialties:
        counts=json.loads(CATALOG.with_name('catalog-summary.json').read_text('utf8'))['multi_specialty_counts']
        print(json.dumps(counts,ensure_ascii=False,indent=2));return
    records=list(search(CATALOG,a.query,a.specialty,a.include_other))
    order={'指南候选':0,'推荐/规范候选':1,'共识/立场声明':2}
    records.sort(key=lambda x:(order.get(x['document_kind'],3),-(x['year'] or 0)))
    print(json.dumps({'source':'bundled_metadata_catalog','total_matches':len(records),'returned':min(len(records),a.limit),'sort':'document_type_then_year_desc; not evidence quality','warning':'题录线索，版本/推荐原文未核实；零命中不等于不存在指南','records':records[:a.limit]},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
