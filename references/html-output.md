# HTML 简报输出

临床默认交付可点击原始来源的 HTML，并保留同源 JSON。用户指定其他格式时遵从。科研协议/计划使用现有 Markdown/CSV 模板；不要为运行渲染器而虚构已完成的医学答案。

1. 复制 [空白数据模板](../assets/outputs/clinical-brief-template.json) 到本次输出目录，依据实际核查填写。答案、指南推荐、二次研究、原始研究各有引用 ID；每个 ID 在 references 中唯一。
2. 运行 `python scripts/render_brief.py 本次目录/brief.json 本次目录/brief.html`。Python 3.10+，只用标准库，不需要联网。已有输出不静默覆盖；修改后另取版本文件名。
3. 检查所有关键结论引用、读取层级、推荐强度和确定性。脚本保证引用 ID 存在及链接协议安全，不能自动证明来源支持结论或网址可达。

每条证据记录：`title`, `text`, `refs`，可加 `strength`, `certainty`, `applicability`, `locator`。参考文献：`id`, `title`, `url`, `kind`, `year`, `issuing_body`, `retrieval_level`。URL 必须为 http/https，不接受脚本、文件或含凭据的地址。缺少直接来源时在限制中标记，不伪造链接。

`human_review.status` 默认 `not_requested`；只有真实发起复核时用 `pending` 并写 requested_at，完成时用 `reviewed` 并写 reviewer/date。`as_of` 是本次资料截止/评估日期；重新排版旧检索结果时在 coverage_summary 写明原检索日期，不能改称重新检索。

HTML 无外部脚本/CDN，适合本地分享和打印。检索详情默认折叠，文献引用可定位书目，书目可直达来源。不内嵌带身份的病历信息。
