---
title: D2 概要设计（Solution）— 方案边界与关键权衡设计规范
status: draft
stage: design
module: D2
principles_ref: design/aisdlc.md
source_refs:
  - design/aisdlc_spec_design.md
---

## 0. 目标与定位

本设计文档用于定义 Design 阶段模块 D2「概要设计」的**框架性规则、硬约束与验收标准**，用于约束后续可能的命令/模板实现，以及指导人工/AI 产物生成。

D2 的目标是把需求/重构稳定落到**可评审的方案**：明确系统边界、核心流程、关键决策与权衡，并为 D3 详细设计提供清晰输入。

输出稳定落盘到：

- `{FEATURE_DIR}/design/solution.md`

---

## 1. 术语与接口

### 1.1 上下文与路径

- **FEATURE_DIR**：由 `Get-SpecContext` 自动获取，定位到 `.aisdlc/specs/{num}-{short-name}/`
- **必读输入**：
  - **需求路径**：`{FEATURE_DIR}/requirements/clarify.md`
  - **重构路径**：`{FEATURE_DIR}/refactors/clarify.md` + `{FEATURE_DIR}/refactors/baseline.md`
  - `{FEATURE_DIR}/requirements/solutions.md` 或 `requirements/prd.md`
  - `{FEATURE_DIR}/design/research.md`（若存在）
- **输出**：`{FEATURE_DIR}/design/solution.md`

### 1.2 必读材料（最小必要读取）

- **标准路径输入**：
  - `{FEATURE_DIR}/requirements/clarify.md`
  - `{FEATURE_DIR}/requirements/solutions.md` 或 `requirements/prd.md`
- **重构路径输入**：
  - `{FEATURE_DIR}/refactors/clarify.md`
  - `{FEATURE_DIR}/refactors/baseline.md`
- **小需求直达 D2（仅文档约定）**：
  - `{FEATURE_DIR}/requirements/raw.md`
- 项目级 `project/memory/*`
- 相关 `project/contracts/` 与 `project/adr/` 索引

---

## 2. 强制门禁（MUST）

- **标准路径**：必须有 `requirements/clarify.md` 与 `requirements/solutions.md`/`requirements/prd.md`，缺失则不得生成。
- **重构路径**：必须有 `refactors/clarify.md` 与 `refactors/baseline.md`，缺失则不得生成。
- **小需求直达 D2（仅文档约定）**：
  - 允许缺少 `clarify.md` 与 `solutions.md`/`prd.md`
  - **必须**读取 `requirements/raw.md`
  - **必须**在 `solution.md` 显式标注“小需求直达 D2”，并补齐最小化需求摘要、边界、未知项与追溯链接
- **必须覆盖目标/范围/边界**，与需求分析保持一致。
- **必须给出核心流程或系统边界图**（Mermaid 优先）。
- **必须记录关键设计决策**（若涉及新决策，需创建或引用 ADR）。
- **未知项必须标注 "NEEDS CLARIFICATION"**，且影响需明确。
- **门禁未通过则报错**（ERROR）。
- **全程使用中文**。

---

## 3. 输出结构（`solution.md` 最小骨架）

建议至少包含：

- **TL;DR**：方案核心结论与最大权衡
- **背景与目标**：对齐需求目标/业务目标
- **范围与边界**：In/Out + 系统边界
- **核心方案与流程**：主流程与关键分支（图优先）
- **关键设计决策**：ADR 摘要或链接
- **约束与权衡**：性能/成本/合规/体验
- **影响分析**：上下游系统、数据口径、运行影响
- **风险与验证计划**：Owner/信号/动作
- **追溯链接**：requirements/、ADR、contracts 入口

---

## 4. 进入 D3 的 DoR 清单（可选阶段的进入条件）

DoR 的目标是让“是否需要进入详细设计与契约”可检查：

- **核心方案明确**：流程/边界可复现
- **关键决策可追溯**：ADR 已记录或可引用
- **需要新契约/数据模型**：明确哪些变更需下沉到 D3

---

## 5. 质量门槛（D2-DoD）

- 方案可评审、可落地，并能回答“为什么这样做”。
- 评审者能判断是否需要进入 D3。
