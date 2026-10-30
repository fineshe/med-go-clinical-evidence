"""Render an explicitly authored clinical evidence JSON as safe standalone HTML (Python 3.10+)."""
import argparse
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

CSS='''*{box-sizing:border-box}body{margin:0;background:#f0f4f5;color:#243e45;font:16px/1.8 system-ui,"Microsoft YaHei",sans-serif}main{max-width:960px;margin:32px auto;padding:40px;background:#fff;border:1px solid #d8e4e7;border-radius:14px}h1{font-size:28px;line-height:1.5}h2{margin-top:32px;border-top:1px solid #d8e4e7;padding-top:20px;font-size:22px}h3{font-size:18px}.answer{padding:20px;background:#edf7f3;border-left:4px solid #267864}.muted,small{color:#5c7077}a{color:#126e69;overflow-wrap:anywhere}.card{padding:16px 0;border-bottom:1px solid #e0e9eb}p{white-space:pre-line}dl{display:grid;grid-template-columns:120px 1fr;gap:6px}dt{color:#5c7077}dd{margin:0}details{margin:24px 0;padding:16px;border:1px solid #d8e4e7}summary{cursor:pointer;font-weight:600}table{border-collapse:collapse;width:100%;font-size:14px}td,th{border:1px solid #d8e4e7;text-align:left;padding:8px;vertical-align:top;overflow-wrap:anywhere}li{margin:6px 0}@media(max-width:650px){main{margin:0;padding:22px;border:0;border-radius:0}h1{font-size:24px}dl{display:block}dd{margin-bottom:8px}table{display:block;overflow:auto}}@media print{body{background:white}main{max-width:none;margin:0;padding:0;border:0}details>*{display:block!important}a{color:inherit}.card{break-inside:avoid}}'''

def e(value):return escape(str(value),quote=True)

def render(data):
    for key in ('title','question','as_of','answer','coverage_summary'):
        if not isinstance(data.get(key),str) or not data[key].strip():raise ValueError('Required nonempty text: '+key)
    if data.get('pathway') not in ('clinical','mixed'):raise ValueError('This renderer is for clinical or mixed briefs; not a plan or completed systematic review')
    refs={}
    for ref in data.get('references',[]):
        rid=ref.get('id','')
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]{0,50}',rid) or rid in refs:raise ValueError('Invalid or duplicate reference id')
        try:p=urlsplit(ref.get('url',''))
        except ValueError:raise ValueError('Invalid reference URL') from None
        if p.scheme not in ('https','http') or not p.hostname or p.username or p.password:raise ValueError('Reference needs an HTTP(S) URL without credentials')
        if not ref.get('title') or not ref.get('retrieval_level'):raise ValueError('Reference title and retrieval level required')
        refs[rid]=ref
    def citations(ids):
        if any(rid not in refs for rid in ids):raise ValueError('Unresolved reference id')
        return ' '.join('<a href="#ref-'+e(rid)+'">['+e(rid)+']</a>' for rid in ids)
    def ul(values):return '<ul>'+''.join('<li>'+e(v)+'</li>' for v in values)+'</ul>' if values else '<p class="muted">未提供。</p>'
    def evidence(key,title,ident):
        parts=['<section id="'+ident+'"><h2>'+title+'</h2>']
        for item in data.get(key,[]):
            parts.append('<article class="card"><h3>'+e(item.get('title',''))+'</h3><p>'+e(item.get('text',''))+' '+citations(item.get('refs',[]))+'</p><dl>')
            fields=[('strength','推荐强度'),('certainty','证据确定性'),('applicability','适用性'),('locator','原文位置')]
            for field,label in fields:
                if field in item:parts.append('<dt>'+label+'</dt><dd>'+e(item[field])+'</dd>')
            parts.append('</dl></article>')
        if not data.get(key):parts.append('<p class="muted">未在本简报中列入；实际检索与缺口见下方记录。</p>')
        parts.append('</section>');return ''.join(parts)
    review=data.get('human_review',{'status':'not_requested'})
    status=review.get('status')
    if status=='reviewed':
        if not review.get('reviewer') or not review.get('date'):raise ValueError('Reviewed requires actual reviewer and date')
        human='人工复核：'+str(review['reviewer'])+'，'+str(review['date'])
    elif status=='pending':
        if not review.get('requested_at'):raise ValueError('Pending requires an actual request date')
        human='已请求人工复核，尚未完成。'
    elif status=='not_requested':human='尚未请求人工复核。'
    else:raise ValueError('Unknown human review status')
    out=['<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(data['title'])+'</title><style>'+CSS+'</style></head><body><main>',
         '<p class="muted">Med-Go 临床证据简报 · '+e(data['as_of'])+' · Skill '+e(data.get('skill_version','unknown'))+'</p><h1>'+e(data['title'])+'</h1><p>'+e(data['question'])+'</p>',
         '<section class="answer"><h2 style="margin-top:0;border:0;padding:0">当前判断</h2><p>'+e(data['answer'])+' '+citations(data.get('answer_refs',[]))+'</p></section>',
         '<h2>已知资料与待补信息</h2><h3>已知</h3>'+ul(data.get('known_facts',[]))+'<h3>未知</h3>'+ul(data.get('unknowns',[])),
         evidence('guidelines','指南建议','guidelines'),evidence('secondary_evidence','系统综述与 Meta 分析','secondary'),evidence('primary_evidence','必要的原始研究补充','primary'),
         '<h2>下一步</h2>'+ul(data.get('next_steps',[]))+'<h2>适用限制</h2>'+ul(data.get('limitations',[]))+'<p>'+e(human)+'</p>',
         '<details id="audit"><summary>检索范围与执行记录</summary><p>'+e(data['coverage_summary'])+'</p><table><thead><tr><th>来源</th><th>查询/动作</th><th>状态</th><th>数量/范围</th></tr></thead><tbody>']
    for row in data.get('search_log',[]):out.append('<tr>'+''.join('<td>'+e(row.get(k,''))+'</td>' for k in ('source','query','status','counts'))+'</tr>')
    out.append('</tbody></table></details><section id="references"><h2>原始来源链接</h2><ol>')
    for rid,ref in refs.items():
        out.append('<li id="ref-'+e(rid)+'"><a href="'+e(ref['url'])+'" target="_blank" rel="noopener noreferrer">['+e(rid)+'] '+e(ref['title'])+'</a><br><small>'+e(ref.get('issuing_body',''))+' · '+e(ref.get('year',''))+' · '+e(ref.get('kind',''))+' · 实际读取：'+e(ref['retrieval_level'])+'</small></li>')
    out.append('</ol></section></main></body></html>');return ''.join(out)

def write_brief(data,dest):
    rendered=render(data);dest=Path(dest)
    dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open('x',encoding='utf-8') as f:f.write(rendered)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path);parser.add_argument('output',type=Path)
    args=parser.parse_args();write_brief(json.loads(args.input.read_text('utf-8-sig')),args.output)
    print(args.output)
