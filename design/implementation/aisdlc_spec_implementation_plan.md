---
title: I1 实现计划（Plan）— 实现范围与里程碑设计规范
status: draft
stage: implementation
module: I1
principles_ref: design/aisdlc.md
source_refs:
  - design/aisdlc_spec_implementation.md
---

## 0. 目标与定位

本设计文档用于定义 Implementation 阶段模块 I1「实现计划」的**框架性规则、硬约束与验收标准**，用于约束后续可能的命令/模板实现，以及指导人工/AI 产物生成。

I1 的目标是把需求/设计稳定落到**可执行的实现计划**：明确范围、里程碑、依赖、风险与验收口径，为 I2 任务分解提供稳定输入。

输出稳定落盘到：

- `{FEATURE_DIR}/implementation/plan.md`

---

## 1. 术语与接口

### 1.1 上下文与路径

- **FEATURE_DIR**：由 `Get-SpecContext` 自动获取，定位到 `.aisdlc/specs/{num}-{short-name}/`
- **必读输入**：
  - **需求路径**：`{FEATURE_DIR}/requirements/clarify.md`
  - **重构路径**：`{FEATURE_DIR}/refactors/clarify.md` + `{FEATURE_DIR}/refactors/baseline.md`
  - `{FEATURE_DIR}/requirements/solutions.md` 或 `requirements/prd.md`
  - `{FEATURE_DIR}/design/solution.md`（如存在）
- **输出**：`{FEATURE_DIR}/implementation/plan.md`

### 1.2 必读材料（最小必要读取）

- **标准路径输入**：
  - `{FEATURE_DIR}/requirements/clarify.md`
  - `{FEATURE_DIR}/requirements/solutions.md` 或 `requirements/prd.md`
  - `{FEATURE_DIR}/design/solution.md`（若存在）
- **重构路径输入**：
  - `{FEATURE_DIR}/refactors/clarify.md`
  - `{FEATURE_DIR}/refactors/baseline.md`
- 项目级 `project/memory/*`
- 相关 `project/contracts/` 与 `project/adr/` 索引

---

## 2. 强制门禁（MUST）

- **标准路径**：必须有 `requirements/clarify.md` 与 `requirements/solutions.md`/`requirements/prd.md`，缺失则不得生成。
- **重构路径**：必须有 `refactors/clarify.md` 与 `refactors/baseline.md`，缺失则不得生成。
- **设计输入缺失处理**：
  - 若 `design/solution.md` 缺失，必须在 `plan.md` 标注原因与影响，并列为 “NEEDS CLARIFICATION”。
- **必须覆盖范围/里程碑/依赖/风险/验收口径**，与需求与设计保持一致。
- **未知项必须标注 "NEEDS CLARIFICATION"**，且影响需明确。
- **门禁未通过则报错**（ERROR）。
- **全程使用中文**。

---

## 3. 输出结构（`plan.md` 最小骨架）

建议至少包含：

- **TL;DR**：计划目标与范围摘要
- **范围与边界**：In/Out（对齐需求与设计）
- **里程碑与节奏**：阶段拆分、时间预估、交付物清单
- **依赖与资源**：外部系统/团队/权限/环境/数据依赖
- **风险与验证**：风险清单、验证方式、Owner
- **验收口径**：关键 AC 与验收人/验收方式
- **待确认项**：统一标注为 “NEEDS CLARIFICATION”
- **追溯链接**：requirements/、design/、ADR、contracts 入口

---

## 4. 进入 I2 的 DoR 清单

DoR 的目标是让“是否可以进入任务分解”可检查：

- **范围与边界明确**：In/Out 无歧义
- **里程碑可验收**：每一项有对应产物或可验证标准
- **依赖与风险可处理**：至少有最小缓解/验证动作

---

## 5. 质量门槛（I1-DoD）

- 计划可执行、可评审，并能回答“为什么这样排期/拆分”。
- 评审者能判断是否可以进入 I2。
