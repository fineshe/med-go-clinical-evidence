# 中英文数据库检索语法补充手册

维护日期：2026-10-19。面向agent逐平台查阅。**规则有官方依据 ≠ 检索式已实际执行 ≠ 检索覆盖完整。** 本包只对PubMed辅助脚本做了可重复测试；各库示例均为说明写法，不是某项研究的完整检索策略。运行状态见研发评估报告，不在本文件预填命中数。

## 1. 通用逻辑与翻译方法

- AND（与/交集）：两个概念都需出现；OR（或/并集）：至少一个同义词出现；NOT（排除）：可能删去同时讨论相关和排除概念的文章，慎用。
- 同义词在一组内OR，必要概念组之间AND：`(A OR A同义词) AND (B OR B同义词)`。这是概念结构，需翻译后才能提交目标平台。
- 不假设“NOT > AND > OR”在所有数据库成立。每组用半角括号明确边界；运算符与词之间留空格。不要让中文智能引号替代平台需要的半角引号。
- 主题词是受控词表中的词；自由词是标题/摘要等字段文字；“主题”搜索框不必然等于MeSH/Emtree主题词。
- 短语会减少变体；截词会增加无关词；邻近算符的距离N在不同平台含义不同。不要把NEAR/3逐字替换成所有平台的“相隔3词”。
- 一次只改一个概念或限制，比较结果与已知相关文献。先单独跑各概念，再组合；保存系统解释、警告、扩展和语言设置。
- 不强制每个问题都有P/I/C/O；不默认限定英文、RCT、近5年或免费全文。增加这些限制必须有任务依据。
- 自动翻译仅生成草稿。中英文概念分别核对标准词、旧称、音译、药品通用名与缩写。最终逐平台审核。
- 日期按平台实际粒度记录。只支持年份而任务要求日级截止时，先取到截止年，再核对每条发表日期；只有年份无法判断者标记日期待核实。不把年过滤写成精确到日，也不把未来执行日期写成实际检索日期。

## 2. PubMed / NLM

**依据：官方帮助已读；脚本执行状态另记。**

大写AND/OR/NOT；默认按从左至右处理，括号优先。字段如`[tiab]`、`[mh]`、`[dp]`；MeSH与自由词并用。双引号和字段限定影响自动词语映射，必须看Search Details。星号截词可用，但邻近检索不能带星号。

邻近：`"sleep duration"[tiab:~3]`，N是两词之间最多间隔词数，顺序不限；N=0是相邻。不是Embase的NEAR/n。日期区间用`("开始日期"[dp] : "截止日期"[dp])`，不要混同入库日。

语法草案：
```text
("Sleep"[mh] OR sleep[tiab])
AND ("Diabetes Mellitus"[mh] OR diabet*[tiab])
```
这些词仅演示主题词+自由词；正式问题需重新选择概念和核对主题词。
来源：[PubMed Help](https://pubmed.ncbi.nlm.nih.gov/help/)。

## 3. Cochrane Library / Wiley Search Manager

**依据：Cochrane官方技术附录；本机未实际检索。**

AND/OR/NOT、括号；`:ti,ab,kw`限定字段。MeSH在词表界面建立后保存生成行，例如`MeSH descriptor: [Diabetes Mellitus] explode all trees`。CDSR和CENTRAL分别选择并记录。

`NEXT`表示相邻且按顺序；`NEAR/n`顺序不限，NEAR/1是相邻，NEAR/3最多隔2词；带截词的词组优先用NEXT。使用显式距离，避免依赖默认值。通配`*`与`?`按平台帮助检查。

```text
#1 (sleep* OR insomnia*):ti,ab,kw
#2 (diabet*):ti,ab,kw
#3 #1 AND #2
```
历史编号取本次会话实际编号，不把示例编号当已有历史。
来源：[技术附录](https://training.cochrane.org/handbook/current/technical-supplement-chapter-4-searching-and-selecting-studies-v63)。旧版手册中“PubMed不支持邻近”已不适用，PubMed看其当前帮助。

## 4. Embase.com（不要用于Ovid Embase）

**依据：Elsevier官方支持页，更新2026-03-06；未在订阅账户运行。**

AND/OR/NOT，先括号再从左到右。Emtree爆炸检索常见`'词'/exp`，非爆炸`'词'/de`；自由词字段`:ti,ab,kw`。词表词必须现场核对。

`NEAR/n`无序，`NEXT/n`有序；NEAR/1为相邻。星号可截词，问号替代单字符，美元符可替代0或1字符；不使用前导通配符。当前帮助允许短语中通配符，不能沿用旧版“一律不允许”的规则。

```text
((sleep* OR insomnia*):ti,ab,kw) AND (diabet*:ti,ab,kw)
```
来源：[运算符官方说明](https://service.elsevier.com/app/answers/detail/a_id/17875/supporthub/embase/kw/proximity/)、[官方字段/过滤器示例](https://www.elsevier.support/embase/answer/embase-study-type-filters)。

## 5. Ovid MEDLINE / Ovid Embase / Ovid PsycINFO

**依据：Ovid官方指南索引与Cochrane技术附录；当前账户字段未实测。**

Ovid是平台，MEDLINE/Embase/PsycINFO是不同库，词表及字段不能混。常见写法`(sleep or insomnia).ti,ab.`；受控词由映射界面生成，如`exp 主题词/`。分行建立集合后组合。

`adj3`通常为任意顺序、最多隔2词；不带数字的adj与其有序行为需按当前指南核对。星号/美元符截词及通配规则以当前库帮助为准；不要移植Embase.com的`/exp`或`:ti,ab,kw`。

来源：[Ovid数据库指南](https://ospguides.ovid.com/cctrdb.htm)、[Ovid产品说明](https://www.wolterskluwer.com/en/solutions/ovid/platforms-products/databases)、上节Cochrane技术附录。访问指南受限时使用高级检索字段选择器并保存生成式，不猜未知字段。

## 6. SinoMed（明确具体子库）

**依据：中国医学科学院官方帮助已核对；未在机构账户运行。**

AND/OR/NOT；高级检索使用大写并留空格。官方优先级NOT>AND>OR，但仍显式分组。通配符`?`为一个字符，`%`为任意个字符；不要换成PubMed星号。主题检索与自由词检索分别建立，再在历史中合并，记录扩展/副主题词设置。

高级检索“常用字段”中的概念草案：
```text
(睡眠 OR 失眠) AND (糖尿病 OR 高血糖)
```
选择哪个字段、哪个子库以及是否词表扩展都属于检索式的一部分。“常用字段”须记录该子库实际覆盖字段；英文空格、连字符或短语处理未确认时用界面构造器分组并保存生成式。命中数未执行前不填写。

来源：[布尔组合](https://analysis.sinomed.ac.cn/help/content/3.1.html)、[通配符](https://www.sinomed.ac.cn/help/content/3.2.html)、[官方使用手册](https://www.sinomed.ac.cn/help/content/download/shiyongshouce.pdf)。

## 7. CNKI / KNS专业检索

**依据：2026-10-19实际读取CNKI官方公开手册1.2.5；账户内未跑查询。**

字段间AND/OR/NOT，半角括号控制顺序。常见SU主题、TI题名、KY关键词、AB摘要、FT全文、YE年。匹配符随字段不同：SU推荐`%=`相关匹配；TI/AB的`=`表示含完整词串，`%`可分词；不能宣称“=在所有字段都完全相同”。SU不是MeSH。

```text
(SU %= '睡眠' OR SU %= '失眠') AND SU %= '糖尿病'
```
字段内`*`、`+`、`-`可分别表达与、或、非，**星号不是通用截词符**。优先展开成完整字段条件，减少歧义。

位置检索如`AB = '睡眠 /NEAR 3 代谢'`；TI/AB/FT中两词限定，半角单引号包住整个表达式。不是`NEAR/3`。不把专业式贴进普通搜索框。

来源：[CNKI官方使用手册](https://piccache.cnki.net/index/helper/manual.html)。KNS版本、总库/子库、匹配方式、中文/外文以及自动扩展都要记录。

## 8. 万方医学网 与 万方智搜：两张配置

### 万方医学网 med.wanfangdata.com.cn

**依据：当前官方帮助已读；未完成实际查询。**

已明确的规则：字段`=`，AND/OR，半角括号；精确词串用双引号；`?`可替代单字符，不放词首。字段有主题/THEME、题名/TI、摘要/AB、关键词/KW等。

```text
(主题=睡眠 OR 主题=失眠) AND 主题=糖尿病
```
本次官方帮助页未说明NOT与通用星号截词，不默认生成这些写法；要排除时先核对当前高级界面支持的“非”及其生成式。不把`主题=(...)`改成未经核实的冒号语法。
来源：[医学网专业检索语法](https://med.wanfangdata.com.cn/Paper/Help)。

### 万方智搜 s.wanfangdata.com.cn

**状态：已列入口，现行专业语法本次未确认。**

进入当前高级检索，逐行选“主题/题名/摘要”等字段、匹配方式、与/或/非；保存系统实际生成式与中英文/主题词扩展开关。旧培训材料存在符号和版本差异，不能凭医学网帮助推断智搜语法，也不默认使用旧`* + ^`或某种冒号表达式。无法读取帮助时交付字段/概念组草案，明确“待平台验证”，不称可直接执行。

## 9. Web of Science Core Collection

**依据：Clarivate官方索引摘要；帮助页面已迁移，运行前复核当前帮助。**

常见高级式`TS=(sleep* OR insomnia*) AND TS=(diabet*)`。AND/OR/NOT；双引号、星号、NEAR/n按当前平台说明使用。`NEAR/0`表示相邻；距离不要照抄Embase的数值。TS是Topic字段，不能称为MeSH词表。记Core Collection实际索引/年限，不把“所有数据库”与Core Collection混记。

来源：[运算符原官方入口](https://webofscience.help.clarivate.com/Content/search-operators.html)、[当前帮助中心](https://webofscience.zendesk.com/hc/en-us)、[字段](https://webofscience.help.clarivate.com/en-us/Content/wos-core-collection/woscc-search-field-tags.htm)。本节不承诺所有当前界面语法完全一致。

## 10. Scopus / Advanced Search

**依据：Elsevier当前官方支持页。**

布尔为AND、OR、AND NOT，排除不是单独的NOT。字段`TITLE-ABS-KEY(...)`；`W/n`无序、`PRE/n`有序，n=0相邻。用括号明确分组；其默认优先级不是PubMed的从左至右。双引号是宽松短语，花括号是更精确短语，混用需按当前帮助核对。

```text
TITLE-ABS-KEY((sleep* OR insomnia*) AND diabet*)
```
邻近算符两侧不能塞进包含AND/AND NOT的任意表达式。出现语法错误就逐组测试，不把错误响应当零结果。
来源：[Advanced Search](https://www.elsevier.support/scopus/answer/how-can-i-best-use-the-advanced-search)、[邻近规则](https://cn.service.elsevier.com/app/answers/detail/a_id/15933/supporthub/scopus/)。

## 11. CINAHL / EBSCO、PsycINFO / EBSCO

**依据：Cochrane技术附录提供平台对照；本机未实测当前EBSCO界面。**

高级字段构造器与布尔AND/OR/NOT起步；CINAHL受控词用其Headings，PsycINFO用APA词表。常见邻近Nn无序、Wn有序；具体N含义、通配和字段（如TI/AB/MH）先查当前EBSCO帮助，不把Ovid字段后缀搬来。本包不提供未经当前平台确认的完整机器执行式。
来源：[EBSCO官方帮助入口](https://connect.ebsco.com/s/article/Searching-with-Boolean-Operators?language=en_US)、Cochrane技术附录。

## 12. 注册、元数据和其他源

ClinicalTrials.gov用其专用query参数；Crossref/DOI主要核身份，不能把PubMed语法直接塞进DOI接口。Europe PMC字段亦不同，查当前API帮助。详见 [公共接口](api-tools.md)。

维普与其他未列完整语法的数据库：先打开官方帮助/当前高级构造器，增加本次任务的语法卡，记录依据和验证时间；不靠记忆补齐。不支持复杂布尔的平台可拆成多条简单搜索，日志保留合并方式，标注覆盖限制。

## 13. 检索式交付检查

每条式附：数据库+平台/版本+子库、可直接运行或概念草案、实际字段、词表核对状态、括号、短语/通配/邻近、日期字段、语言与扩展开关、文献类型、排序、执行时间、解释/警告、总数和实取数。任何“已验证”必须说明是**帮助文档核对**还是**已在目标平台执行**。

