# 材料选择指南

v0.3.0。先按任务选材料，再复制到本次输出目录填写；不要直接改Skill内空白模板。空白代表未填写，不代表0、无事件或已核实。模板提供最低记录要求，可以增减有意义字段。

临床任务先用 [临床路径](clinical-pathway.md)、[学科指南目录](guidelines/README.md) 与 [HTML简报](html-output.md)。下方旧 Markdown 模板仍供用户指定格式或科研材料使用，不改变临床默认 HTML。

## 哪一步用哪份

| 时机 | 材料 | 使用方式 |
|---|---|---|
| 新问题、范围不清 | [任务卡](../assets/intake/task-card.yaml) | 从用户原话提取，可推断项标假设；关键未知项才询问 |
| 检索前建词表 | [概念词表](../assets/planning/concept-matrix.csv) | 每个概念一行；主题词候选与已查词表结果分开 |
| 翻译到具体平台 | [逐库方案](../assets/planning/database-strategy.md) | 每库复制一份；保留字段、布尔关系、版本、验证状态 |
| 实际检索 | [检索日志](../assets/search-log-template.csv) | 一条实际查询一行；查询版本不覆盖 |
| 筛选题录与全文 | [筛选表](../assets/screening/screening-log.csv) | 分题录/全文阶段；未获全文可awaiting，不自动排除 |
| 同一研究多篇报告 | [研究—报告关联表](../assets/screening/study-report-map.csv) | 同一study_id、不同report_id，记录关联依据 |
| 提取研究数据 | 下方对应题型表 | 通常只取一种；复合问题可并用，使用相同study_id/report_id |
| 核查具体结论 | [主张表](../assets/claim-template.csv) | 逐主张定位；可读取层级与主张支持分开 |
| 处理不一致 | [证据差异表](../assets/synthesis/evidence-differences.csv) | 对齐人群、设计、结局、时点，保留未解决项 |
| 交付快速答疑 | [一页简报](../assets/outputs/quick-brief.md) | 短结论、最关键证据、覆盖与限制 |
| 标准证据简报 | [详细模板](../assets/evidence-brief-template.md) | 可裁剪，保留日志/主张表链接 |
| 团队测试 | [测试提示词](../evals/manual-test-prompts.md)、[反馈表](../evals/test-feedback.csv) | 只在测试或维护时加载；评分依据不提前给被测agent |

## 按题型选提取表

| 题型 | 模板 | 特别核对 |
|---|---|---|
| 治疗/预防 | [treatment.csv](../assets/extraction/treatment.csv) | 比较方向、绝对事件、效应区间、随访、伤害 |
| 诊断/筛查准确性 | [diagnostic.csv](../assets/extraction/diagnostic.csv) | 阈值/单位、参照标准、患者谱、四格数据与验证偏倚信息 |
| 预后/预测模型 | [prognostic.csv](../assets/extraction/prognostic.csv) | 时间起点、模型版本、内部/外部验证、校准与区分度 |
| 暴露/病因/风险 | [exposure.csv](../assets/extraction/exposure.csv) | 时序、比较、调整项、混杂及未调整/调整效应 |
| 患病率/发病率 | [frequency.csv](../assets/extraction/frequency.csv) | 抽样、病例定义、分母/人时、时期和权重 |
| 体验/质性 | [qualitative.csv](../assets/extraction/qualitative.csv) | 参与者、情境、资料分析、主题与支持材料 |
| 卫生经济/实施 | [health-services.csv](../assets/extraction/health-services.csv) | 视角、环境、价格年份、资源、结局与迁移条件 |
| 指南/共识 | [guideline.csv](../assets/extraction/guideline.csv) | 文件类型/状态、地区、版本、推荐位置、制定方原有分级 |

这些表不自动执行偏倚或证据确定性评价。需要正式评价时选择适用的当前方法，另记录工具版本、逐项依据及复核。

## 填写约定

1. 标识：study_id表示研究，report_id表示一份报告；同一研究可多报告、多结局、多时点。指南使用report_id标识文档，不把指南本身计作独立原始研究。
2. 粒度：每行一个研究/报告中的一个结局、阈值、主题或推荐；多行不等于多个独立研究。表中population可填写研究样本的精确名称而不猜测病例条件。
3. 原文未报告填NR，已报告但本次未取得填not_accessed，不适用填NA；空白仅用于尚未开始填写。未读摘要时retrieval_level为not_retrieved。
4. 数字保留组别、单位、分析集、分母和时点；记录原文结果与自己计算的结果的区别。不要用缺失值当0。
5. 所有关键条目写source_locator；只拿到摘要就定位摘要段，不能造页码、表号。
6. 指南表分别记录 recommendation_strength_as_reported 和 evidence_certainty_as_reported；原文未报告记 NR，本次未核实记 not_accessed。保留旧 grade 字段以兼容原文件，不擅自转换成 GRADE。
7. CSV为UTF-8；Excel若识别错误，用“数据→从文本/CSV”选择UTF-8。含换行/逗号的值应正确加引号。
8. 小任务可把表放进Markdown；不必每次生成全部文件。一个完整起步组合是任务卡+对应检索方案+实际日志+一种提取表+简报。
9. 筛选表decision可记include / exclude / awaiting / uncertain；排除要写理由，未获全文先记awaiting，不能只因无法免费获取就当作不符合科学纳入标准。

填写示例见 [合成资料与完成样例](../assets/examples/worked-example.md)。它只演示记录方法，不是医学证据；常规查询时不加载或引用这些内容。

