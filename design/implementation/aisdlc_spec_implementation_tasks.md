---
title: I2 任务分解（Tasks）— 可执行任务与验收对齐设计规范
status: draft
stage: implementation
module: I2
principles_ref: design/aisdlc.md
source_refs:
  - design/aisdlc_spec_implementation.md
---

## 0. 目标与定位

本设计文档用于定义 Implementation 阶段模块 I2「任务分解」的**框架性规则、硬约束与验收标准**，用于约束后续可能的命令/模板实现，以及指导人工/AI 产物生成。

I2 的目标是把实现计划拆解成**可执行、可追溯、可并行**的任务清单，确保任务粒度可落地并能对应验收标准。

输出稳定落盘到：

- `{FEATURE_DIR}/implementation/tasks.md`

---

## 1. 术语与接口

### 1.1 上下文与路径

- **FEATURE_DIR**：由 `Get-SpecContext` 自动获取，定位到 `.aisdlc/specs/{num}-{short-name}/`
- **必读输入**：
  - `{FEATURE_DIR}/implementation/plan.md`
  - **需求路径**：`{FEATURE_DIR}/requirements/prd.md` 或 `requirements/solutions.md`
  - **重构路径**：`{FEATURE_DIR}/refactors/clarify.md` + `{FEATURE_DIR}/refactors/baseline.md`
  - `{FEATURE_DIR}/design/solution.md`（如存在）
- **输出**：`{FEATURE_DIR}/implementation/tasks.md`

### 1.2 必读材料（最小必要读取）

- **标准路径输入**：
  - `{FEATURE_DIR}/implementation/plan.md`
  - `{FEATURE_DIR}/requirements/prd.md` 或 `requirements/solutions.md`
  - `{FEATURE_DIR}/design/solution.md`（若存在）
- **重构路径输入**：
  - `{FEATURE_DIR}/refactors/clarify.md`
  - `{FEATURE_DIR}/refactors/baseline.md`
- 项目级 `project/contracts/` 与 `project/adr/` 索引（如涉及契约/决策）

---

## 2. 强制门禁（MUST）

- **必须先有 `implementation/plan.md`**，缺失则不得生成。
- **标准路径**：必须有 `requirements/prd.md` 或 `requirements/solutions.md`，缺失则不得生成。
- **重构路径**：必须有 `refactors/clarify.md` 与 `refactors/baseline.md`，缺失则不得生成。
- **任务必须覆盖 `plan.md` 的范围与里程碑**，并能追溯到需求/设计输入。
- **未知项必须标注 "NEEDS CLARIFICATION"**，且影响需明确。
- **门禁未通过则报错**（ERROR）。
- **全程使用中文**。

---

## 3. 任务生成策略（执行步骤）

> 说明：以下流程参考通用任务生成规则，并按本项目文档结构做适配。

### 3.1 设置（Setup）

- 在仓库根目录运行 `{SCRIPT}`，解析 **FEATURE_DIR** 与 **AVAILABLE_DOCS**（可用文档列表）。
- 所有路径必须是绝对路径。
- 参数包含单引号时，优先使用双引号；若必须用单引号，按 PowerShell 转义写法处理。

### 3.2 加载设计文档（Load design documents）

从 `FEATURE_DIR` 读取：

- **必须**：
  - `implementation/plan.md`（技术栈、库、结构）
  - `requirements/prd.md` 或 `requirements/solutions.md`（作为“带优先级的用户故事/需求规格”来源）
- **可选**（按可用文档决定）：
  - `design/data-model.md`（实体/数据模型）
  - `design/contracts/`（API/事件契约）
  - `design/research.md`（关键决策与权衡）
  - `quickstart.md`（若项目存在自定义测试场景入口）

### 3.3 执行任务生成工作流（Execute task generation workflow）

- 加载 `plan.md` 并提取技术栈、库、项目结构
- 加载 `prd.md` 或 `solutions.md` 并提取用户故事及其优先级（P1/P2/P3 等）
- 如果 `design/data-model.md` 存在：提取实体并映射到用户故事
- 如果 `design/contracts/` 存在：将端点映射到用户故事
- 如果 `design/research.md` 存在：提取设置任务的决策
- 按用户故事组织生成任务（参见下方“任务生成规则”）
- 生成显示用户故事完成顺序的依赖图
- 为每个用户故事创建并行执行示例
- 验证任务完整性（每个用户故事都包含所有必需任务，且可独立测试）

### 3.4 生成 `tasks.md`（Generate tasks.md）

- 使用 `templates/tasks-template.md` 作为结构（按项目约定可替换为实际模板路径）
- 填充以下内容：
  - 来自 `plan.md` 的正确功能名称
  - 阶段 1：设置任务（项目初始化）
  - 阶段 2：基础任务（所有用户故事的阻塞性先决条件）
  - 阶段 3+：每个用户故事一个阶段（按优先级顺序）
  - 每个阶段包含：故事目标、独立测试标准、测试（如要求）、实施任务
  - 最终阶段：打磨与横切关注点（Polish & cross-cutting concerns）
  - 所有任务必须遵循严格清单格式（`- [ ]`）
  - 每个任务必须包含清晰的文件路径
  - 显示故事完成顺序的依赖关系部分
  - 每个故事的并行执行示例
  - 实施策略部分（MVP 优先、增量交付）

---

## 4. 输出结构（`tasks.md` 最小骨架）

建议至少包含：

- **任务拆分原则**：粒度标准、并行策略、风险优先级
- **任务清单**（逐条任务包含）：
  - 任务 ID / 标题 / Owner
  - 关联需求/设计链接（Spec ID 或文件路径）
  - 前置依赖与阻塞条件
  - 预计工作量与优先级
  - 交付物与验收点（与 AC 对齐）
  - 相关代码范围（建议路径/模块）
  - 测试点提示（如需）
- **故事依赖关系**：用户故事完成顺序依赖图（可用 Mermaid）
- **并行执行示例**：每个用户故事至少 1 个并行执行示例
- **实施策略**：MVP 优先与增量交付策略
- **里程碑映射**：任务与计划里程碑的对应关系
- **追溯链接**：plan、requirements、design、ADR、contracts 入口

---

## 5. 质量门槛（I2-DoD）

- 任务清单可执行、可追溯，并能回答“为什么这样拆分”。
- 评审者能判断任务是否可并行、可验收、可交付。
