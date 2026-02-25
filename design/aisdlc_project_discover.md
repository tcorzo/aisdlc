# AI SDLC：从设计出发的“反向 Discover（正向工程）”方案

> 目标：在充分遵循 `design/aisdlc.md` 的“双层 SSOT + 渐进式披露 + Merge-back”原则下，基于 `commands/discover-level*.md` 系列的结构，整理一套**反向流程**：不再“从代码反推文档”，而是“从设计资产（SSOT）出发，驱动索引/模块文档/契约先行，再落地实现并保持可追溯”。

---

## 1. 概念对齐：Discover（逆向）与 Design（正向）

- **Discover（逆向工程）**：面向“已有代码的存量项目”，以仓库事实为证据，反推 `.aisdlc/project/` 的 Level-0/Level-1 资产（见 `commands/discover-level0-memory.md` 与 `commands/discover-level1-*.md`）。
- **Design（正向工程，本文）**：面向“绿地项目/重构项目/新模块落地”，以设计资产为 SSOT，先产出 `.aisdlc/project/` 的 Level-0/Level-1（地图层），再驱动需求级 `specs/<DEMAND-ID>/` 与代码实现；实现完成后用 Merge-back 把可复用资产晋升回项目级。

> **核心差异**：Discover 的“证据”来自现有仓库；Design 的“证据”来自**设计决策与契约**（ADR、Contracts、评审记录）并在实现后补齐“代码证据入口”。

---

## 2. 适用场景与边界

### 2.1 适用场景

- **绿地项目**：没有可逆向的代码事实，必须设计先行。
- **存量重构/迁移**：以目标架构与目标契约为 SSOT，再逐步让实现追齐（过程中允许“双轨”，但必须显式标注）。
- **新增业务域/新增应用组件**：先补齐项目级地图层与契约，再进入需求级 Spec Pack。

### 2.2 边界约束（继承 `design/aisdlc.md`）

- **项目级（`.aisdlc/project/`）只承载长期稳定资产**：边界、承诺、入口、权威契约、NFR 预算与运行入口；不写一次性交付细节。
- **需求级（`.aisdlc/specs/<DEMAND-ID>/`）承载交付细节**：详细时序、字段级约束、迁移步骤、测试用例、发布回滚、验证证据等。
- **渐进式披露**：地图层只做导航入口；细节按需读取需求级。

---

## 3. 模板与落盘位置约定（本仓库实际路径）

`discover*` 文档中引用的模板路径是 `.aisdlc-cli/templates/project/*`；在本仓库中对应为：

- **Level-0 模板**（北极星 / 根上下文）：
  - `templates/project/structure-template.md` → `.aisdlc/project/memory/structure.md`
  - `templates/project/tech-template.md` → `.aisdlc/project/memory/tech.md`
  - `templates/project/product-template.md` → `.aisdlc/project/memory/product.md`
  - `design/aisdlc.md` 中的 `glossary.md` 结构约定 → `.aisdlc/project/memory/glossary.md`
- **Level-1 模板**（地图层）：
  - `templates/project/components-index-template.md` → `.aisdlc/project/components/index.md`
  - `templates/project/components-module-template.md` → `.aisdlc/project/components/{module}.md`
  - `templates/project/products-index-template.md` → `.aisdlc/project/products/index.md`
  - `templates/project/products-module-template.md` → `.aisdlc/project/products/{module}.md`
  - `templates/project/contracts-index-template.md` → `.aisdlc/project/contracts/index.md`
  - `templates/project/contracts-api-index-template.md` → `.aisdlc/project/contracts/api/index.md`
  - `templates/project/contracts-data-index-template.md` → `.aisdlc/project/contracts/data/index.md`
  - `templates/project/contracts-api-module-template.md` → `.aisdlc/project/contracts/api/{module}.md`
  - `templates/project/contracts-data-module-template.md` → `.aisdlc/project/contracts/data/{module}.md`

---

## 4. 反向流程总览（从设计到落地）

### 4.1 总体执行顺序（建议）

1. **Level-0 先行（北极星）**：先把“去哪找/怎么引用/边界在哪里”写清楚。
2. **Level-1 骨架（地图层）**：生成索引骨架 + 任务清单（复选框），明确待回填位置。
3. **组件与契约先行（Components + Contracts）**：用模块级契约文件作为“权威入口”，再回填索引。
4. **业务聚合与业务模块（Products）**：先聚合收敛（<= 6），再逐模块补齐明细并回填索引。
5. **需求级 Spec Pack**：按需求落细到 `specs/<DEMAND-ID>/`，并引用项目级资产（CAP/BP/BO 编号、Contracts、ADR）。
6. **实现/测试/发布**：代码与测试追溯到 Spec；上线后生成运维资产。
7. **Merge-back**：将可复用资产（ADR、契约、运行资产、NFR 基线等）晋升回项目级。

### 4.2 “复选框任务驱动”的正向用法

Discover 用复选框控制“要逆向哪些模块”；Design 可以把复选框作为**设计落地的进度控制面板**：

- `components/index.md`：`- [ ]` 表示该组件的 **组件明细 + 模块契约** 尚未补齐；完成后改为 `- [x]`。
- `products/index.md`：`- [ ]` 表示该业务模块明细尚未补齐；完成后改为 `- [x]`。

> 这样可以实现：先建“地图与任务”，再迭代补齐明细，避免“一口气写完整但不可执行/不可验证”。

---

## 5. 与 `discover*` 的一一对应：反向方案（Design 版）

下面按 `commands/` 的 Discover 链路，给出其“反向（正向工程）”等价步骤。**你可以把它理解为同一套产物结构，但输入从“仓库事实”变成“设计决策与契约”。**

### 5.1 对应 `commands/discover-level0-memory.md`：Design-Level0（北极星初始化）

**目标**：不是反推，而是“先写北极星”，为后续所有地图层与需求级产物提供锚点与约束。

- **输入（Design）**：
  - 产品愿景/边界（可来自 PRD/立项）
  - 技术栈约束（组织/平台/合规）
  - 预期工程形态（单体/多服务/Monorepo）
- **输出（同 Discover 的 Level-0）**：
  - `.aisdlc/project/memory/structure.md`
  - `.aisdlc/project/memory/tech.md`
  - `.aisdlc/project/memory/product.md`
  - `.aisdlc/project/memory/glossary.md`
- **关键写法（正向工程的“证据”口径）**：
  - 结构/技术/业务结论的证据优先指向：ADR、Contracts、模板位置约定、评审记录入口
  - 允许保留 **Assumption/TBD**，但必须写“影响面 + 后续验证方式（实现/测试/PoC）”

### 5.2 对应 `commands/discover-level1-index-scan.md`：Design-Level1-Skeleton（地图层骨架）

**目标**：用模板生成 Level-1 的索引骨架，并把“待回填”的模块清单（复选框任务）先建出来。

- **输出**（与 scan 相同，但不依赖扫描）：
  - `.aisdlc/project/components/index.md`
  - `.aisdlc/project/products/index.md`
  - `.aisdlc/project/contracts/index.md`
  - `.aisdlc/project/contracts/api/index.md`
  - `.aisdlc/project/contracts/data/index.md`
- **关键动作（Design 版）**：
  - 组件候选不是“扫出来”，而是**由架构设计定义**：先给出组件清单与边界假设，写入 `components/index.md` 的表格与任务清单。
  - Contracts 索引骨架先固化“权威入口位置约定”，并标注“由模块契约文件回填”。

### 5.3 对应 `commands/discover-level1-components-detail.md`：Design-Component-&-Contracts（组件与契约先行）

**目标**：对每个组件 `{module}`，先把“承诺与边界”写清楚，并落盘模块级契约文件，随后回填索引。

- **输入（Design）**：
  - `.aisdlc/project/components/index.md` 的任务清单（未勾选的模块）
  - Level-0 约束（结构/技术/业务/术语）
- **输出（同 discover-level1-components-detail）**：
  - `.aisdlc/project/components/{module}.md`
  - `.aisdlc/project/contracts/api/{module}.md`
  - `.aisdlc/project/contracts/data/{module}.md`
  - 回填更新：`components/index.md` + contracts 三个索引
- **正向工程的关键约束**：
  - **契约先行**：`contracts/*/{module}.md` 在 Design 阶段就是 SSOT；实现后补齐“代码证据入口”（OpenAPI 文件、Proto、Schema、路由/handler 等）。
  - **索引只做导航**：详细条目以模块级契约文件为准，避免双写漂移。

### 5.4 对应 `commands/discover-level1-products-aggregate.md`：Design-Products-Aggregation（业务聚合与收敛）

**目标**：基于 `product.md + glossary + contracts/data 主责`，把业务域/模块聚合收敛到 **<= 6**，并把任务清单写入 `products/index.md`。

- **输入**：
  - `.aisdlc/project/memory/*.md`
  - `.aisdlc/project/products/index.md`（骨架）
  -（可选）已产出的模块级契约文件（用于“以契约/对象主责聚合”）
- **输出**：
  - `.aisdlc/project/products/index.md`（写入：聚合方案选择 + 业务模块清单任务）
- **Design 建议**：
  - 不必强制“输出 3 个候选方案再交互选择”（这是 Discover 为避免误判的交互策略）；Design 可以直接记录“为什么按此边界划分”的理由与替代方案（ADR 风格亦可）。

### 5.5 对应 `commands/discover-level1-products-detail.md`：Design-Product-Detail（业务模块明细与回填）

**目标**：为每个业务模块 `{module}` 生成 `products/{module}.md`，并把入口/协作/契约回链回填到 `products/index.md`。

- **输入**：
  - `.aisdlc/project/products/index.md` 的任务清单（未勾选的模块）
  - contracts 入口（优先模块级契约，其次索引入口）
- **输出**：
  - `.aisdlc/project/products/{module}.md`
  - 回填更新：`.aisdlc/project/products/index.md`

---

## 6. Discover ↔ Design：输入/输出“反向对照表”

| 主题 | Discover（逆向）输入 | Design（正向）输入 | 共同输出（SSOT 位置不变） |
|---|---|---|---|
| Level-0 | 仓库事实（目录/脚本/CI/配置/契约文件） | 立项/PRD/架构约束/目标形态/ADR 草案 | `.aisdlc/project/memory/*.md` |
| Level-1 骨架 | Level-0 + 扫描仓库 | Level-0 + 设计的组件/模块清单 | `.aisdlc/project/*/index.md` |
| Components 明细 | 代码入口 + 证据回链 | 组件边界/服务承诺/契约先行（实现后补证据） | `.aisdlc/project/components/{module}.md` |
| Contracts | 从代码/文件汇总契约入口 | 先定义 SSOT 契约（后续实现对齐） | `.aisdlc/project/contracts/*` |
| Products 聚合 | 从现状线索收敛并交互选择 | 基于目标业务边界直接定稿（记录理由/替代方案） | `.aisdlc/project/products/*` |

---

## 7. 质量与可追溯（Design 版 DoD）

### 7.1 设计阶段的“证据”两类

- **设计证据（先于实现）**：
  - ADR（`project/adr/` 或需求级 `specs/<DEMAND-ID>/design/design.md` 中的决策段落）
  - Contracts（`project/contracts/*` 的权威入口与约束）
  - 评审记录入口（会议纪要/文档链接/审批单号等）
- **实现证据（实现后补齐）**：
  - 代码入口：路由/handler/consumer/job/cli、模块目录、关键类型定义
  - 自动化证据：CI job、lint/test 命令、发布流水线、监控告警

### 7.2 最小自检清单（建议纳入 DoD）

- [ ] Level-0 四份北极星已生成，且能指导“如何定位/如何引用/边界是什么”
- [ ] Level-1 索引骨架已生成，且明确“待回填位置/由谁回填”
- [ ] 每个已勾选完成的组件 `{module}`：同时具备
  - [ ] `components/{module}.md`
  - [ ] `contracts/api/{module}.md`
  - [ ] `contracts/data/{module}.md`
  - [ ] contracts/components 索引已回填并可导航到上述文件
- [ ] products 数量已收敛到 <= 6；若无法收敛，已记录不可合并理由与治理建议
- [ ] 项目级资产保持“短 + 入口清晰 + 可追溯”，一次性交付细节下沉到 `specs/<DEMAND-ID>/`

---

## 8. 建议的落地节奏（避免“文档先行但落不了地”）

- **第 1 周**：Level-0 完整 + Level-1 索引骨架 + 1 个组件样板（含模块契约）+ 1 个业务模块样板。
- **第 2~N 周（迭代）**：按复选框任务逐模块补齐；每完成一个模块就补齐“实现证据入口”（代码/CI/监控）并 Merge-back。
- **每次需求交付后**：执行 `specs/<DEMAND-ID>/merge_back.md`，把 ADR/Contracts/Runbook/NFR 基线晋升回项目级。

---

## 9. 常见陷阱与规避

- **陷阱：把需求级细节写进项目级地图层**  
  - **规避**：项目级只写边界/承诺/入口；详细流程、字段级约束、迁移细节下沉需求级。

- **陷阱：索引与模块双写，导致漂移**  
  - **规避**：索引只做导航；详情以模块文档与模块级契约文件为准；索引仅回填摘要与入口链接。

- **陷阱：契约不权威，最后实现各写各的**  
  - **规避**：Design 阶段把 `project/contracts/*` 定义为 SSOT；实现必须对齐并在 PR 中更新契约与证据入口。

- **陷阱：模块数量失控（>6）导致治理失败**  
  - **规避**：强制聚合收敛；无法收敛必须写明原因（合规隔离/数据主责分裂/组织边界等）并给出治理路线。

