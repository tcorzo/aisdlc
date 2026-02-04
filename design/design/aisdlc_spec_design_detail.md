---
title: D3 详细设计与契约（Detail & Contracts）— 组件/模型/接口下沉规范
status: draft
stage: design
module: D3
principles_ref: design/aisdlc.md
source_refs:
  - design/aisdlc_spec_design.md
---

## 0. 目标与定位

本设计文档用于定义 Design 阶段模块 D3「详细设计与契约」的**框架性规则、硬约束与验收标准**，用于约束后续可能的命令/模板实现，以及指导人工/AI 产物生成。

D3 的目标是把概要方案下沉到**可实现、可契约化**的粒度：组件边界、接口细节、数据模型与协议约束，形成实现与测试可追溯的设计资产。

输出稳定落盘到：

- `{FEATURE_DIR}/design/detail.md`
- `{FEATURE_DIR}/design/data-model.md`（如涉及数据模型变更）
- `{FEATURE_DIR}/design/contracts/`（如涉及接口/事件契约）

---

## 1. 术语与接口

### 1.1 上下文与路径

- **FEATURE_DIR**：由 `Get-SpecContext` 自动获取，定位到 `.aisdlc/specs/{num}-{short-name}/`
- **必读输入**：
  - `{FEATURE_DIR}/design/solution.md`
  - `{FEATURE_DIR}/design/research.md`（若存在）
- **输出**：
  - `{FEATURE_DIR}/design/detail.md`
  - `{FEATURE_DIR}/design/data-model.md`
  - `{FEATURE_DIR}/design/contracts/`

### 1.2 必读材料（最小必要读取）

- 项目级 `project/contracts/`（契约索引与规范）
- 项目级 `project/adr/`（关键决策）
- 编码规范与数据口径（如存在）

---

## 2. 强制门禁（MUST）

- **若引入新数据对象或字段**，必须输出 `data-model.md`。
- **若变更对外接口/事件**，必须落盘 `design/contracts/` 并标明版本/兼容策略。
- **接口必须包含输入/输出/错误约束**，并可追溯到需求与流程。
- **未知项必须标注 "NEEDS CLARIFICATION"**，且影响需明确。
- **门禁未通过则报错**（ERROR）。
- **全程使用中文**。

---

## 3. 输出结构（最小骨架）

### 3.1 `detail.md`

建议至少包含：

- **组件边界与职责**：模块/组件职责与协作
- **时序与关键流程**：关键链路与异常分支（图优先）
- **关键规则与状态**：幂等、权限、异常、边界
- **实现约束**：性能/成本/合规/依赖
- **追溯链接**：solution/ADR/contracts/data-model 入口

### 3.2 `data-model.md`

建议至少包含：

- **实体清单**：名称、职责、生命周期
- **字段与关系**：关键字段、约束、索引、关系
- **状态流转**：状态机或状态表（如适用）
- **验证规则**：来自需求的校验规则

### 3.3 `contracts/`

建议至少包含：

- **API/事件契约**：OpenAPI/AsyncAPI/Schema
- **版本与兼容**：向后兼容策略与弃用计划
- **错误码/异常**：统一约束与示例

---

## 4. D3-DoD（质量门槛）

- 设计细节足以支撑实现与测试追溯。
- 契约与数据模型变更可被评审与验证。
