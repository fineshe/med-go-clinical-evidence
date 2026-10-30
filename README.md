# Med-Go Clinical Evidence

面向临床循证答疑与文献科研检索的中文 AI 技能包。支持中英文检索规划、指南候选定位、证据核查记录和 HTML 临床证据简报。

**版本：0.3.0** · **Python：3.10+** · **脚本依赖：仅标准库**

## 能做什么

- **临床路径**：从适用指南入手，补充系统综述、Meta 分析及必要的原始研究，记录适用条件与证据缺口。
- **科研路径**：根据治疗、诊断、预后、病因等题型制定中英文多库检索方案，保留检索、筛选与提取记录。
- **离线指南候选查找**：随包提供 16,538 条题录，以及学科索引、候选清单和来源记录。
- **PubMed 辅助检索**：小批量抓取题录和摘要，保留查询、原始响应及完整性状态。
- **HTML 简报**：将已撰写、已核查的结构化 JSON 转为可分享、可打印的独立 HTML。

## 获取与使用

```bash
git clone https://github.com/fineshe/med-go-clinical-evidence.git
cd med-go-clinical-evidence
```

也可在 GitHub 点击 **Code → Download ZIP**，解压后使用。需要 AI 技能支持时，将本目录放入所用工具支持的技能目录，并保留 `SKILL.md`、`references/`、`assets/`、`scripts/` 等相对结构。技能入口为 [SKILL.md](SKILL.md)，人工工作流见 [SOP](references/human-sop.md)。

### 离线查找指南候选

```bash
python scripts/find_guidelines.py --list-specialties
python scripts/find_guidelines.py --specialty "心血管内科" --query "高血压" --limit 5
```

重复 `--query` 表示字面子串 AND；同义词应分别检索，再合并结果。目录仅提供文献线索，使用前须回到发布机构或出版方核对原文、当前版本和适用性。详见 [指南目录说明](references/guidelines/README.md)。

### PubMed 辅助检索

把制定好的检索式保存为 UTF-8 文件 `query.txt`，再运行：

```bash
python scripts/pubmed_search.py --query-file query.txt --until YYYY-MM-DD --max-records 50 --out runs/new-run
```

将 `YYYY-MM-DD` 替换为本次检索截止日；输出目录必须尚不存在。需要联网，默认最多 50 条、上限 500 条；超限或抓取不完整时标记 `partial`。这一步不等于完成系统综述或核实医学结论。接口与访问说明见 [api-tools.md](references/api-tools.md)。

### 生成 HTML 简报

复制并填写 [JSON 模板](assets/outputs/clinical-brief-template.json)，再运行：

```bash
python scripts/render_brief.py runs/brief.json runs/brief.html
```

输出文件必须尚不存在。模板中的必填字段和引用需要按实际核查结果填写；渲染器不会代为生成医学结论。字段说明见 [html-output.md](references/html-output.md)。

## 目录

| 路径 | 内容 |
| --- | --- |
| `SKILL.md` | 技能入口与临床、科研用途路由 |
| `agents/` | 技能展示配置 |
| `scripts/` | 指南题录查找、PubMed 检索、HTML 渲染 |
| `references/` | 检索语法、来源、核查规范、SOP 与指南题录 |
| `assets/` | 任务卡、检索日志、筛选、提取与交付模板 |
| `evals/` | 手动评估提示、检查清单与反馈模板 |
| `licenses/` | 保留的上游许可证 |

## 数据与使用边界

指南目录整理于 **2026-10-19**，不代表每条指南当前仍有效。全部题录标为 `current_status=not_verified`、`retrieval_level=catalog_metadata_only`，未逐篇完成原文推荐核查或临床专家审核。目录不含指南全文或付费论文；无命中也不表示不存在相关指南。

本项目用于辅助检索、整理和核查证据。实际临床应用仍需核对原文、适用人群及更新情况，并由具备资质的专业人员作出判断。示例与评估用合成材料不能作为医学证据。

## 开源许可与来源

本项目原创代码、流程文档和模板采用 [MIT License](LICENSE)。改写参考的 K-Dense 上游内容保留其 [MIT 许可证](licenses/K-Dense-MIT.txt) 与署名。

第三方指南题录及其所指向的文献保留各自权利；本项目的 MIT 许可证不授予这些第三方文献的额外使用权限。详细来源见 [NOTICE](NOTICE) 与 [provenance.md](references/provenance.md)。

欢迎通过 Issues 提交可复现的问题，或通过 Pull Request 改进检索规则、模板与脚本。更新题录时请保留来源、日期及核验状态。
