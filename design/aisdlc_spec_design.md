---
title: Spec 级设计阶段 SOP（概要设计为核心，D1/D3 可选）
status: draft
audience: [PM, BA, SA, DEV, QA]
principles_ref: design/aisdlc.md
---
# 设计阶段流程（D1 可选 / D2 必做 / D3 可选）

## 1. 背景与目标（对齐 `design/aisdlc.md`）

本方案用于 **Spec 级** 的“需求/重构设计阶段”提效：在遵循“双层 SSOT + Spec as Code + 渐进式披露”的前提下，用 **可复用的设计SOP** 把需求/重构稳定推进到“概要设计”，必要时扩展到“大纲与研究”与“详细设计、契约”。

**结论**：
- **D2 概要设计为必做**（适用于所有规模需求/重构）。
- **D1 大纲与研究**与 **D3 详细设计、契约**为可选（小需求可跳过）。
- **设计阶段的终点**为概要设计或详细设计与契约（按需求规模选取），不包含实现/测试/发布。

---

## 2. 产物落盘与“渐进式披露”读取顺序

### 2.1 建议落盘结构（需求级 Spec Pack）

对齐 `design/aisdlc.md` 中的需求级目录（示例）：

```text
.aisdlc/specs/<DEMAND-ID>/
  index.md
  requirements/
    ...                   # 已完成的需求分析产物
  design/
    research.md           # D1 研究结论（可选）
    solution.md           # D2 概要设计（必做）
    data-model.md         # D3 数据模型（可选）
    contracts/            # D3 接口/事件契约（可选）
    detail.md             # D3 详细设计汇总（可选）
```

### 2.2 Agent 读取顺序（渐进式披露）

- **必读（项目级）**：`project/memory/*`（业务/技术/结构/术语）与 `project/contracts/`、`project/adr/` 索引。
- **按需（需求级）**：仅在明确处理某个 `<DEMAND-ID>` 时读取该需求的：
  - **需求路径**：`requirements/*` 与 `design/*`
  - **重构路径**：`refactors/*` 与 `design/*`（R2 的 DoR 作为进入 design 的前置门禁）
- **回写（入库）**：每个模块独立产出一个文件或一个章节，保持可替换与可审计。

---

## 3. 设计SOP总览（统一流程）

**流程**：`D1 大纲与研究（可选） → D2 概要设计（必做） → D3 详细设计、契约（可选）`

**最短路径（小需求）**：

`spec-init → D2 概要设计（小需求直达） → 执行`

说明：
- **仅文档约定**：允许缺少 `requirements/clarify.md` 与 `requirements/solutions.md`/`requirements/prd.md`
- **最小输入**：`requirements/raw.md`
- **门禁要求**：`design/solution.md` 中必须标注“小需求直达 D2”，并补齐最小化需求摘要、边界、未知项与追溯链接

**增强路径（中大型需求/重构）**：

`D1 大纲与研究 → D2 概要设计 → D3 详细设计、契约`

**重构路径进入 design 的前置条件**：

- 必须完成 R0~R2（见 `design/aisdlc_spec_refactor.md`）
- **R2 的 DoR 清单**作为进入 design 的硬门禁

---

## 3.1 阶段设计规范索引（design/design）

下面文档是对各模块“门禁、接口、输出结构、DoD”的硬约束规范：

- **D1 研究**：`design/design/aisdlc_spec_design_research.md`
- **D2 概要设计**：`design/design/aisdlc_spec_design_solution.md`
- **D3 详细设计、契约**：`design/design/aisdlc_spec_design_detail.md`

---

## 4. 执行步骤提示词（结构化要求）

以下步骤结构用于**具体模块的执行描述**，与 aisdlc 体系一致，但强调“门禁”和“澄清项”：

1. **设置（Setup）**：
   - 读取当前需求上下文（分支/目录），确定 `<DEMAND-ID>` 与 `specs/<DEMAND-ID>/design/` 目录。
2. **加载上下文（Load context）**：
   - 读取关键产物：
     - **需求路径**：`requirements/clarify.md`、`requirements/solutions.md` 或 `requirements/prd.md`
     - **重构路径**：`refactors/clarify.md`、`refactors/baseline.md`
   - 以及项目级 `memory/`、`contracts/`、`adr/`。
3. **执行工作流（Execute workflow）**：
   - 依据模块模板执行，**将未知项标记为“NEEDS CLARIFICATION”**。
   - **门禁未通过则报错**（ERROR），不得落盘下一阶段产物。
4. **停止并报告（Stop and report）**：
   - 报告执行到哪一阶段、产物路径与未解决澄清项。

---

## 5. 模块 D1：研究（可选）

### 5.1 目标

把“需求/重构问题域”快速固化为设计输入：现状、约束、风险、未知项与研究结论，为 D2 做准备。

### 5.2 输入

- **需求路径**：`requirements/` 关键产物（如 `clarify.md` / `solutions.md` / `prd.md`）
- **重构路径**：`refactors/clarify.md` + `refactors/baseline.md`
- 项目级 `memory/` 与相关 `contracts/`、`adr/` 索引

### 5.3 输出（落盘到 `design/research.md`）

建议结构（合并大纲与研究）：

- **TL;DR**：问题域现状与最大风险
- **现状与问题域**：关键现状、痛点与影响
- **范围边界**：In/Out 与不变量
- **关键约束**：合规/性能/依赖/组织
- **风险清单**：Top 风险与影响描述
- **未知项清单**：统一标注为 "NEEDS CLARIFICATION"
- **研究结论**：
  - 决策（Decision）
  - 理由（Rationale）
  - 备选方案（Alternatives considered）

### 5.4 门禁（D1-DoD）

- 已列出所有未知项并标注为 “NEEDS CLARIFICATION”
- 研究结论可追溯，且为 D2 提供可用输入

### 5.5 小需求跳过准则

- 需求范围单一、风险低、无外部依赖或关键技术不确定性

---

## 6. 模块 D2：概要设计（必做）

### 6.1 目标

将需求/重构映射为可评审的**概要方案**：设计边界、核心流程、关键权衡与对齐关系。

### 6.2 输入

- **需求路径**：`requirements/*` 中的核心产物（`clarify.md` / `solutions.md` / `prd.md`）
- **重构路径**：`refactors/clarify.md` + `refactors/baseline.md`
- （可选）`design/research.md`
- 项目级 `memory/`、`contracts/`、`adr/`

### 6.3 输出（落盘到 `design/solution.md`）

建议结构：

- **背景与目标**（对齐需求目标与业务目标）
- **范围与边界**（In/Out 与系统边界）
- **核心方案与流程**（Mermaid 优先）
- **关键设计决策**（ADR 摘要，必要时创建 ADR）
- **约束与权衡**（性能/稳定性/成本/合规）
- **影响分析**（上下游系统、数据口径、运行影响）
- **风险与验证计划**（Owner/信号/动作）

### 6.4 门禁（D2-DoD）

- 方案能覆盖需求的目标、范围与关键约束
- 存在清晰的流程或系统边界描述
- 关键决策有记录或 ADR 入口

---

## 7. 模块 D3：详细设计、契约（可选）

### 7.1 目标

把概要方案下沉到**可实现与可契约化**的粒度：组件/接口细节、数据模型与 API/事件契约。

### 7.2 输入

- `design/solution.md`
- （可选）`design/research.md`
- 项目级 `contracts/`、`adr/` 与编码/数据规范

### 7.3 输出（落盘到 `design/`）

- **数据模型**：`design/data-model.md`（实体、字段、关系、状态）
- **契约**：`design/contracts/`（API/事件/消息）
- **详细设计**：`design/detail.md`

### 7.4 门禁（D3-DoD）

- 数据模型与契约能够支撑实现与测试追溯
- 关键接口/事件具备清晰输入输出与错误约束

### 7.5 小需求跳过准则

- 无新数据模型与契约变更
- 方案可以直接由现有组件/契约满足

---

## 8. 需求 vs 重构差异处理清单（每模块通用）

- **输入口径**：需求用 `requirements/*`；重构用 `refactors/clarify.md` + `refactors/baseline.md`
- **现状评估**：现有架构/流程/数据口径与债务清单
- **影响范围**：下游系统、数据迁移、兼容性与回滚
- **风险预算**：性能/稳定性/成本的变化区间
- **验证策略**：必须覆盖回归与对照验证

---

## 9. 追溯与 Merge-back 提示

- 设计阶段新增的关键决策应落盘到 `project/adr/`。
- 接口或数据契约的变更应更新 `project/contracts/` 对应索引与契约文件。
- 可复用的长期资产在需求完成后通过 Merge-back 晋升到项目级。
