# 来源、改造与许可

本包版本0.3.0，制作/核对日期2026-10-19。主流程按用户要求改为通用临床与健康研究，非某病种专用。v0.2补充本地自编任务/检索/筛选/提取/交付模板、合成填写样例及手动测试材料；数据库规则沿用v0.1已注明的核对状态，没有新增订阅库已验证的声明。

参考并改写：
- [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)，MIT。
- 固定commit：a1043ef544e3a100c28e70a736b6cf32554d0677。
- 相关文件：skills/literature-review/SKILL.md、skills/literature-review/references/database_strategies.md、skills/citation-management/references/pubmed_search.md、skills/database-lookup/references/clinicaltrials.md。
- 借鉴内容：数据库与网页搜索分工、检索来源记录、记录/报告/研究区分、标识符与结论核查区分、API访问与导出完整性约束。
- 上游MIT许可原文保留于 [licenses/K-Dense-MIT.txt](../licenses/K-Dense-MIT.txt)。
- 本地新增：中文通用问题路由、中英文语法卡、人用SOP、数据模板与无第三方依赖PubMed辅助脚本。脚本为本地编写，未复制依赖_common的上游脚本。

没有整体安装上游大包，也没有引入其与本任务无关的付费搜索、绘图或PDF依赖。被比较的其他仓库没有复制进本包；不沿用其质量承诺。

数据库规则依据各参考文档中的官方链接；只保存必要的自编摘要和例式，不打包商业数据库正文或付费论文。上游代码活跃度、星数、测试目录仅供工程选择，不能证明本包已达到临床可靠性。

维护方法：遇到平台迁移/语法错误时先查官方帮助，更新对应单节及核对日期，再做小查询测试；核心流程无需因某个病例更换。更新应保留原始query和版本，不覆写历史记录。



v0.3 新增用途路由、临床指南优先流程、HTML 渲染器和用户提供两份指南表的题录目录。题录只保留书目信息与来源位置，不打包正文/摘要。题录来自用户资料，不因此成为上游 MIT 内容；原机构/出版者权利不因整理改变。目录核验范围见 [目录说明](guidelines/README.md)。
