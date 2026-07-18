---
name: materials-research-guide
description: "Design evidence-grounded materials-science research plans for any user-specified material system. Use for literature-backed experiment design, characterization strategy, mechanism analysis, innovation assessment, controls, research roadmaps, or manuscript planning across materials synthesis, processing, interfaces, coatings, catalysts, energy materials, tribology, corrosion, polymers, ceramics, metals, and composites. Require verifiable sources; never invent citations, data, mechanisms, novelty, or experimental conditions."
---

# 循证材料研究设计

## 核心规则

先证据、后方案。不得伪造引用、DOI、数据、机理、创新性或“最佳条件”。把可执行参数标为：

- `[D]`：直接文献支持；
- `[X]`：相邻体系外推，注明边界；
- `[S]`：工程筛选起点，待优化。

无法核验时，输出检索方向、工作假设和证据缺口，不把推断写成事实。

## 选择输出深度

默认使用**紧凑模式**。仅当用户明确要求“完整报告、系统综述、论文框架、全部章节、保存文件”时使用**完整模式**。

### 紧凑模式（默认）

- 只回答用户请求的模块，不自动补齐十章节；
- 目标为约 1200 个中文字符以内，引用除外；
- 核验 3–5 个最相关来源；通常用 2–4 组定向检索；
- 不自动创建文件、读取参考文件或运行审计脚本；
- 结尾只给一个最有价值的下一步。

### 完整模式

按需读取，不要一次性加载全部资源：

- 精确参数、系统检索或创新性判断：读 [references/evidence-policy.md](references/evidence-policy.md)；
- 可执行实验设计：读 [references/experimental-design-guardrails.md](references/experimental-design-guardrails.md)；
- 十章节正式报告：读 [references/output-contract.md](references/output-contract.md)。

仅在用户要求保存正式报告时创建文件。报告已保存且允许执行脚本时，再运行 `scripts/audit_output.py`；否则做内联检查，不为审计单独申请高权限。

## 输入与边界

至少识别材料体系和研究目标。设备、工艺、基线、约束或评价标准缺失时，仅在答案会因此改变方向时提出问题，最多 2 个；否则声明假设后继续。

## 检索与核验

1. 用材料别名/化学式、工艺、目标性能、失效模式和机理构建少量高信息检索式。
2. 优先直接匹配的同行评议原始研究，再用标准或综述补方法与背景。
3. 核验题名、作者、来源、年份和 DOI/稳定链接；搜索摘要只作线索。
4. 关键数字需正文、方法或补充材料支持；仅元数据或摘要可见时降低结论强度。
5. 主要决策已有证据后停止扩展检索；冲突来源并列呈现。

## 工作流

1. 定义材料、环境、目标响应和关键权衡，区分事实、推断与未知项。
2. 建立最小证据集，标出直接证据、外推和缺口。
3. 设计分阶段实验：基线/单组分/工艺空白、因素与水平、重复、响应、统计方法和 go/no-go 门槛。
4. 将每个机理映射到互补表征、竞争假设和证伪结果；单一表征不作为完整机理证明。
5. 只交付请求内容，并在相关主张旁放置来源链接。

## 紧凑输出建议

按任务选择并合并以下内容，省略无关项：

- 一句话判断与最大不确定性；
- 3–5 条证据快照；
- 最小实验/对照矩阵；
- 关键表征、竞争机理与证伪结果；
- 风险、成功门槛和下一步。

用表格替代重复段落。不要在正文和证据表中重复同一结论；用户未要求时，不展开创新点、论文框架或完整参考文献表。

## 完整报告

完整模式按 [references/output-contract.md](references/output-contract.md) 生成，关键主张用 `[E1]` 等编号回链。参考文献注明核验深度：`M`（元数据）、`A`（摘要）、`F`（全文/方法）。任何未核验条目放入“候选线索”，不得混入“已核验参考文献”。
