# 中英文数据库与资源目录

核对日期：2026-10-19。官方入口与接口会更新；“收录到目录”不代表已安装连接器、拥有订阅或在本机完成过检索。操作前再确认访问能力。语法见 [手册](search-syntax.md)。

| 资源 / 平台 | 主要用途 | 启用条件 | 可用路径与受限处理 |
|---|---|---|---|
| [PubMed](https://pubmed.ncbi.nlm.nih.gov/) / NLM | 生物医学题录、摘要及文献关联 | 通用英文入口；不限英文文献本身 | 网页或 E-utilities；免费题录不等于全文；可用本包脚本 |
| [SinoMed](https://www.sinomed.ac.cn/) / 中国医学科学院 | 中文生物医学及其跨库资源；主题检索 | 通用中文入口，记录实际所选子库 | 网页/机构权限；未配置官方API时不编造接口 |
| [CNKI](https://kns.cnki.net/) / KNS | 中文期刊、学位、会议等；中外文混合检索可选 | 中文覆盖补充、学位/会议/本地研究 | 记子库及中文/外文选择；机构登录与全文权限分开 |
| [万方医学网](https://med.wanfangdata.com.cn/Paper) | 医学期刊、学位、会议及其他医学资源 | 中文医学补充 | 按医学网语法；与智搜不可共用同一语法配置 |
| [万方智搜](https://s.wanfangdata.com.cn/) | 跨学科文献、学位、会议等 | 跨学科或机构入口在智搜 | 当前界面高级检索/帮助生成表达式；本次未验证现行专业语法 |
| [维普](https://qikan.cqvip.com/) | 中文期刊补充 | 需要补充中文期刊覆盖或用户指定 | 仅列入口；本包未核实当前语法，执行时读官方帮助 |
| [Cochrane Library](https://www.cochranelibrary.com/) / Wiley | CDSR是综述；CENTRAL是试验报告检索源 | 干预问题重点使用；其他问题按相关性 | 两个资源分别记录；摘要/检索/全文权限可能不同 |
| [Embase](https://www.elsevier.com/products/embase) / Embase.com或Ovid | 生物医学、药物、会议等补充 | 需要更广覆盖、药物/不良事件、系统性检索 | 常需订阅；先记平台，再选Emtree与语法 |
| [CINAHL](https://www.ebsco.com/products/research-databases/cinahl-database) / EBSCO | 护理与相关健康文献 | 护理、康复、体验/实施问题 | 订阅；CINAHL Headings不是MeSH的简单复制 |
| [PsycINFO](https://www.apa.org/pubs/databases/psycinfo) / Ovid、EBSCO等 | 心理与行为文献 | 心理、精神、行为或患者体验 | 订阅；词表及字段随平台核实 |
| [Epistemonikos](https://www.epistemonikos.org/) | 综述与其原始研究关联 | 查相关综述、查重与引文扩展 | 可访问网页；API需另核实授权；不能当所有原始研究的穷尽库 |
| [Web of Science](https://www.webofscience.com/) / Core Collection | 跨学科与引文网络 | 引文追踪、交叉学科、计量 | 记合集和订阅年代；不能只写“SCI数据库” |
| [Scopus](https://www.scopus.com/) | 跨学科题录与引文网络 | 同上，按权限选择 | 高级检索与基本检索字段不同；API权限另核实 |
| [ClinicalTrials.gov](https://clinicaltrials.gov/) | 研究注册、方案、状态和已提交结果 | 临床试验发现、更新与注册核对 | 官方v2 API/网页；结果提交不等于已发表论文 |
| [WHO ICTRP](https://trialsearch.who.int/) / [ChiCTR](https://www.chictr.org.cn/) | 国际注册聚合 / 中国临床试验注册 | 国际/中国试验与未发表研究 | 注册号互相关联去重；聚合记录回溯原注册库；API不预设免费开放 |
| [PROSPERO](https://www.crd.york.ac.uk/prospero/) | 系统综述注册 | 拟做综述、查协议与重复开展 | 注册内容不是综述结果 |
| [Europe PMC](https://europepmc.org/) / [PMC](https://pmc.ncbi.nlm.nih.gov/) | 题录、合法开放全文、关联版本 | 全文获取与身份补全 | Europe PMC REST可用时调用；并非所有记录都含全文；区分预印本 |
| [Crossref](https://api.crossref.org/) / [DOI](https://doi.org/) | DOI元数据、出版方定位 | 逐篇身份核对 | DOI解析/元数据成功仍需核对题名作者年份及正文；非Crossref DOI可无其记录 |
| 官方指南/监测机构 | 发布的指南、统计、政策与更新 | 随地区、专科和问题选择 | 机构官网优先；记录发布、更新、适用地区及推荐原文位置 |

注册、全文、元数据、综述、原始研究各有用途，不把它们简单计为“检索了N个独立文献库”。Google Scholar、Semantic Scholar及普通网页搜索为补充发现；AI摘要和搜索片段不能替代原始来源。

访问失败记录“哪一步失败”：搜索页、导出、摘要或全文。可使用其他合法来源继续，但在覆盖表中保留未完成项目；不购买订阅、不代登录、不绕过验证码。需要用户提供已授权导出或全文时，只说明实际缺口。

官方方法与产品说明：[Cochrane检索章节](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04)、[SinoMed系统说明](https://www.sinomed.ac.cn/zh/classSearch.jsp)、[Epistemonikos方法](https://test.epistemonikos.org/en/about_us/methods)、[WHO ICTRP说明](https://www.who.int/tools/clinical-trials-registry-platform)。本目录的启用条件为团队工作约定。

