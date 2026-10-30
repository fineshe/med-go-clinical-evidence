# 公共接口与可选工具

仅使用当前环境已有网络工具或用户授权的访问路径。没有API并不妨碍通过合法网页检索；没有连接器也不能声称所有库可自动调用。

## PubMed

本包 `scripts/pubmed_search.py` 使用Python 3.10+标准库，不需pip、付费API或API key。它执行小批量ESearch+EFetch，保存原始JSON/XML、查询解释和题录；**不下载全文，不生成医学结论，不自动核实主张**。

在skill目录运行，先把自己制定的PubMed检索式保存为UTF-8文本，再执行：
```text
python scripts/pubmed_search.py --query-file query.txt --until YYYY-MM-DD --max-records 50 --out runs/new-run
```
将YYYY-MM-DD替换为本次截止日；脚本要求新输出目录，避免覆盖。日期限定是Publication Date；如任务需入库日/更新日，另用平台相应字段，不把此脚本结果冒充该口径。PubMed可按电子或印刷发表日期命中，所以脚本同时保留期刊日期与ArticleDate；不要仅凭较晚的印刷日期判为超出截止范围。仅按发布日期截止也不等于重建历史时点数据库快照。

命中数超max-records时为partial。最大500条，默认50条、按发表日期排序；这是简报辅助取样，不是系统综述全量导出。要全面导出应使用正式批量工作流；PubMed ESearch的10,000上限不能简单靠History规避，要规划分区并核对完整性。

网络请求低频、有限重试。共享IP上其他agent也占限额，不并发运行大量实例。持续/大规模使用按NCBI要求注册真实tool/contact；可在环境中设置NCBI_EMAIL，不在文件里写API key，不虚构邮箱。
来源：[NCBI用量规范](https://eutilities.github.io/site/API_Key/usageandkey/)、[PubMed帮助](https://pubmed.ncbi.nlm.nih.gov/help/)。

产物：
- run.json：开始/结束时间、原始式/日期限定式、总数/实取数、警告、状态、缺失/异常PMID及完整性。
- esearch.json、efetch-*.xml：原始响应。
- records.json：题名、摘要、标识符与更正关联线索；claim_status默认not_assessed。

退出码0为查询抓取完成；2为partial/failed。即使退出0，也不表示检索策略查全、文献质量良好或结论已核实。

## ClinicalTrials.gov v2

官方入口：[数据API](https://clinicaltrials.gov/data-api/api)、[NLM版本说明](https://www.nlm.nih.gov/pubs/techbull/ma24/ma24_clinicaltrials_api.html)。
```text
GET https://clinicaltrials.gov/api/v2/studies?query.cond=diabetes&pageSize=5&countTotal=true
GET https://clinicaltrials.gov/api/v2/studies/{已核实的NCT编号}
```
读取studies、totalCount、nextPageToken；后续页传pageToken，不能把首页当全量。记录状态、注册/更新日期、结局预设和结果是否提交，回溯正式报告。真实query必须URL编码；以上仅示意。

## Europe PMC 与开放全文

[REST说明](https://europepmc.org/RestfulWebService)：
```text
GET https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=diabetes&format=json&pageSize=5
```
按服务返回的hitCount和cursor继续，记录source/id/DOI/PMID。只对允许获取的OA全文走官方fullTextXML入口；题录存在不保证可取全文。查出预印本时单列版本和发表状态。与PubMed命中有重叠，不能重复计研究。

## Crossref / DOI

[Crossref REST](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)：
```text
GET https://api.crossref.org/works/{URL编码后的DOI}
```
核对题名、作者、年份、期刊与目标文献；论文勘误、撤稿/更新还要检查出版方。Crossref未收录不自动说明DOI不存在，可能属其他注册机构。HTTP错误和无匹配要分开。

## 订阅库

Embase、Scopus、Web of Science的API资格与网页订阅可能不同。SinoMed、知网、万方、维普不预设公开匿名批量接口。使用已配置工具或可访问网页，记录登录/订阅/导出限制。不要把网页登录凭证写入skill或交付包。

