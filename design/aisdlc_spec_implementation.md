---
title: Spec 级实现阶段 SOP（计划 / 任务分解 / 执行）
status: draft
audience: [PM, BA, DEV, QA]
principles_ref: design/aisdlc.md
---
# 实现阶段流程（I1 计划 / I2 任务分解 / I3 执行）

## 1. 背景与目标（对齐 `design/aisdlc.md`）

本方案用于 **Spec 级** 的“实现阶段”提效：在遵循“双层 SSOT + Spec as Code + 渐进式披露”的前提下，用 **可复用的实现SOP** 把需求稳定推进到“可执行的实现计划与任务分解”。

**结论**：
- **I1 实现计划为必做**（所有需求/重构进入实现前必须完成）
- **I2 任务分解为必做**（实现任务必须可执行、可追溯、可拆解）
- **I3 执行为必做**（必须解析并执行 `tasks.md` 中定义的所有任务，并回写执行状态）
- 本阶段 **不包含** 测试与发布产物（分别在 verification / release 阶段完成）

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
    ...                   # 已完成的设计产物
  implementation/
    plan.md               # I1 实现计划（必做）
    tasks.md              # I2 任务分解（必做）
```

### 2.2 Agent 读取顺序（渐进式披露）

- **必读（项目级）**：`project/memory/*`（业务/技术/结构/术语）与 `project/contracts/`、`project/adr/` 索引
- **按需（需求级）**：仅在明确处理某个 `<DEMAND-ID>` 时读取该需求的：
  - **需求路径**：`requirements/*`（至少 `clarify.md` / `solutions.md` / `prd.md` 之一）
  - **重构路径**：`refactors/*`（如为重构需求）
  - **设计路径**：`design/*`（至少 `design/solution.md`，如存在）
- **回写（入库）**：每个模块独立产出一个文件，保持可替换与可审计

### 2.3 上下文自动识别机制

对齐 `design/aisdlc_spec_init.md` 中的“上下文自动识别机制”要求，所有 spec 级命令在执行前必须先获取当前 spec 相关上下文信息：

- 调用脚本函数 `Get-SpecContext`（位于 `.aisdlc-cli/scirpts/spec-common.ps1`）
- 获取 `REPO_ROOT`、`CURRENT_BRANCH`、`FEATURE_DIR`、`SPEC_NUMBER`、`SHORT_NAME`
- 基于 `FEATURE_DIR` 自动定位输入/输出路径，例如：
  - `implementation/plan.md` → `{FEATURE_DIR}/implementation/plan.md`
  - `implementation/tasks.md` → `{FEATURE_DIR}/implementation/tasks.md`

---

## 3. 实现SOP总览（统一流程）

**流程**：`I1 实现计划（必做） → I2 任务分解（必做） → I3 执行（必做）`

**最短路径（小需求）**：

`I1 实现计划 → I2 任务分解 → I3 执行`

说明：
- **最小输入**：`requirements/raw.md` 或 `requirements/prd.md`（至少其一）
- **门禁要求**：若输入不足，必须在 `plan.md` 中标注“待确认项”，并阻断进入 I2

---

## 3.1 阶段设计规范索引（design/implementation）

下面文档是对各模块“门禁、接口、输出结构、DoD”的**硬约束规范**：

- **I1 实现计划**：`design/implementation/aisdlc_spec_implementation_plan.md`
- **I2 任务分解**：`design/implementation/aisdlc_spec_implementation_tasks.md`
- **I3 执行**：`design/implementation/aisdlc_spec_implementation_implement.md`

---

## 4. 执行步骤提示词（结构化要求）

以下步骤结构用于**具体模块的执行描述**，强调“门禁”和“澄清项”：

1. **设置（Setup）**：
   - 读取当前需求上下文（分支/目录），确定 `<DEMAND-ID>` 与 `specs/<DEMAND-ID>/implementation/` 目录
2. **加载上下文（Load context）**：
   - 读取关键产物（按需最少读取）：
     - **需求路径**：`requirements/clarify.md`、`requirements/solutions.md`、`requirements/prd.md`
     - **重构路径**：`refactors/clarify.md`、`refactors/baseline.md`
     - **设计路径**：`design/solution.md`（如存在）
   - 以及项目级 `memory/`、`contracts/`、`adr/`
3. **执行工作流（Execute workflow）**：
   - 依据模块模板执行，**将未知项标记为“NEEDS CLARIFICATION”**
   - **门禁未通过则报错**（ERROR），不得落盘下一阶段产物
4. **停止并报告（Stop and report）**：
   - 报告执行到哪一阶段、产物路径与未解决澄清项

---

## 5. 模块 I1：实现计划（必做）

### 5.1 目标

把需求/设计转化为**可执行的实现计划**：明确实现范围、里程碑、依赖、风险与验收口径，为任务分解提供稳定输入。

### 5.2 输入

- **需求路径**：`requirements/clarify.md` / `requirements/solutions.md` / `requirements/prd.md`
- **重构路径**：`refactors/clarify.md`、`refactors/baseline.md`（如为重构需求）
- **设计路径**：`design/solution.md`（如存在）
- **项目级资源**：`project/memory/*` 与 `project/contracts/`、`project/adr/`

### 5.3 输出（落盘到 `implementation/plan.md`）

建议结构（最小闭环）：

- **TL;DR**：一句话概括计划目标与范围
- **范围与边界**：In/Out（对齐需求与设计）
- **里程碑与节奏**：阶段拆分、时间预估、交付物清单
- **依赖与资源**：外部系统/团队/权限/环境/数据依赖
- **风险与验证**：风险清单、验证方式、Owner
- **验收口径**：对应 PRD/方案的关键 AC 与验收人
- **待确认项**：统一标注为 “NEEDS CLARIFICATION”

### 5.4 门禁（I1-DoD）

- 计划范围与 `requirements/*`、`design/*` **一致**
- 里程碑明确且可验收（每一项有对应产物或可验证标准）
- 依赖与风险已列出，并有最小验证/缓解动作
- 关键验收口径可追溯（至少引用 `prd.md` 或 `solutions.md`）
- 任何不确定项均标注为 “NEEDS CLARIFICATION”

---

## 6. 模块 I2：任务分解（必做）

### 6.1 目标

把实现计划拆成**可执行、可追溯、可并行**的任务清单，确保任务粒度可落地并能对应验收标准。

### 6.2 输入

- `implementation/plan.md`（必须）
- **需求路径**：`requirements/prd.md` 或 `requirements/solutions.md`
- **重构路径**：`refactors/clarify.md`、`refactors/baseline.md`（如为重构需求）
- **设计路径**：`design/solution.md`（如存在）
- 项目级 `contracts/`、`adr/`（如涉及契约/决策）

### 6.3 输出（落盘到 `implementation/tasks.md`）

建议结构（最小闭环）：

- **任务拆分原则**：粒度标准、并行策略、风险优先级
- **任务清单**（逐条任务包含）：
  - 任务 ID / 标题 / Owner
  - 关联需求/设计链接（Spec ID 或文件路径）
  - 前置依赖与阻塞条件
  - 预计工作量与优先级
  - 交付物与验收点（与 AC 对齐）
  - 相关代码范围（建议路径/模块）
  - 测试点提示（如需）
- **里程碑映射**：任务与计划里程碑的对应关系

### 6.4 门禁（I2-DoD）

- 任务清单覆盖 `plan.md` 的范围与里程碑
- 任务粒度可执行（不出现“过大/不可验证”的任务）
- 每个任务至少能追溯到一个需求/设计输入
- 关键依赖与阻塞条件明确，且可处理
- 交付物与验收点可验证（可与 AC 对齐）

---

## 7. 模块 I3：执行（必做）

### 7.1 目标

将 `implementation/tasks.md` 中定义的任务**解析为可执行序列**，并按依赖/优先级/阶段顺序逐条实施，最终形成“任务清单已完成 + 代码与文档已落盘 + 关键决策/契约变更已在 Spec 内落盘并具备 merge-back 证据”的可审计闭环。

### 7.2 输入

- `implementation/tasks.md`（必须，I2 产物）
- `implementation/plan.md`（必须，用于校验范围、里程碑与技术约束）
- `requirements/*`、`refactors/*`、`design/*`（按 `tasks.md` 中引用路径按需读取）
- 项目级 `project/memory/*`、`project/contracts/`、`project/adr/` **索引（只读）**（如任务涉及契约/决策/术语）

### 7.3 输出（执行过程回写）

- **代码与配置变更**：在仓库中完成实现（按任务中指明的路径/模块）
- **任务状态回写**：更新 `{FEATURE_DIR}/implementation/tasks.md`
  - 将已完成任务从 `- [ ]` 标记为 `- [x]`
  - 对每个任务补充最小可审计信息（建议：提交号/PR 链接/变更文件路径）
- **决策与契约草拟（Spec 内落盘，禁止直接更新 project/）**（如任务要求）：
  - **ADR 草案**：优先记录在 `{FEATURE_DIR}/design/solution.md` 的“决策/权衡”段落；如需独立文件，可新增 `{FEATURE_DIR}/design/adr/` 下的 ADR 草案（仅需求级资产）
  - **契约草案**：在 `{FEATURE_DIR}/design/contracts/` 下草拟/更新（对齐“需求开发过程中，契约可先在 `specs/<DEMAND-ID>/design/` 里草拟”的约定）
  - **晋升说明**：在 `{FEATURE_DIR}/implementation/tasks.md` 中保留对应“Merge-back 待办”任务（或在 `{FEATURE_DIR}/merge_back.md` 中列为待晋升项），待 merge-back 时再同步到 `project/adr/` 与 `project/contracts/`

> 说明：I3 不强制新增额外执行日志文件；如需要更细的执行审计，可在 `implementation/` 下增补 `execution-log.md`，但必须保证 `tasks.md` 仍是唯一的执行清单与状态来源。

### 7.4 执行步骤（I3 Workflow）

1. **设置（Setup）**
   - 调用 `Get-SpecContext`（`.aisdlc-cli/scirpts/spec-common.ps1`）获取 `FEATURE_DIR`
   - 定位并读取：
     - `{FEATURE_DIR}/implementation/tasks.md`（必须）
     - `{FEATURE_DIR}/implementation/plan.md`（必须）
   - 建立执行约束：全程仅基于输入材料推进；不确定信息必须标注为“未知/待确认”，不得脑补。

2. **解析 tasks.md（Parse）**
   - 解析 `tasks.md` 中所有任务条目（必须是严格清单格式 `- [ ]` / `- [x]`）
   - 提取每条任务的最小字段（若缺失则视为门禁失败）：
     - 任务 ID、标题、Owner（如有）、文件路径/代码范围、验收点/交付物
     - 前置依赖与阻塞条件（如声明）
   - 识别所有标注为 “NEEDS CLARIFICATION” 的任务或前置条件，并将其作为**阻塞项**记录。

3. **构建执行序列（Plan execution order）**
   - 按 `tasks.md` 的阶段（阶段 1/2/3+）为主顺序执行；阶段内遵循：
     - **依赖优先**：先执行被依赖项（必要时进行拓扑排序）
     - **风险优先**：先处理高风险/高不确定任务（以尽早暴露阻塞）
     - **并行提示**：若 `tasks.md` 给出并行示例，则按 Owner/模块拆分为可并行队列（I3 执行者可串行落地，但必须保持依赖关系正确）

4. **逐条执行任务（Execute tasks）**
   - 对每个任务执行统一循环：
     - **前置检查**：依赖任务是否已完成？所需输入/权限/环境是否满足？
     - **阻塞处理**：若阻塞项为 “NEEDS CLARIFICATION”，则停止该任务并记录：缺什么、如何补齐、向谁取证/从哪里取证。
     - **实施变更**：按任务指明的路径与交付物完成实现（代码/配置/文档/脚本等）。
     - **自检校验**：对照任务验收点执行最小验证（例如：构建通过、单测通过、静态检查通过、契约示例可运行等，具体以任务定义为准）。
     - **回写状态**：将任务勾选为完成 `- [x]`，并补充可审计信息（提交号/PR/关键文件）。

5. **收敛与横切关注点（Closeout）**
   - 执行 `tasks.md` 中的“打磨/横切关注点”任务（如：一致性、性能、可观测性、错误处理、文档补齐）
   - 若引入关键决策/契约变更：**只在 Spec 目录内落盘草案**，并在 `tasks.md`（或 merge_back.md）中明确 merge-back 的晋升清单与证据入口（禁止在 Spec 阶段直接修改 `project/*`）

6. **停止并报告（Stop and report）**
   - 输出执行报告：完成了哪些任务、剩余哪些任务、阻塞项清单与下一步建议
   - 若存在阻塞项，必须明确“阻塞影响范围”与“最短解阻路径”

### 7.5 门禁（I3-DoD）

- `tasks.md` 中所有“计划内任务”已处理：
  - 能完成的已标记为 `- [x]`
  - 因澄清阻塞无法继续的，必须在任务处标注阻塞原因与取证路径（不得静默跳过）
- 产出与 `plan.md` 的范围/里程碑一致，无越界实现
- 每个任务的交付物与验收点可追溯（最少链接到变更文件/提交/PR）
- 若产生关键决策/契约变更：已在 `{FEATURE_DIR}` 内完成草拟，并在 `tasks.md`（或 `merge_back.md`）中明确 **merge-back 晋升待办**（Spec 阶段不直接更新 `project/*`）

---

## 8. 追溯与回写提示

- `implementation/plan.md` 与 `implementation/tasks.md` 应引用对应 `requirements/*` 与 `design/*`
- 实现过程中产生的关键决策/契约变更：**在 Spec 目录内落盘草案**，并在 merge-back 阶段晋升/同步到 `project/adr/` 与 `project/contracts/`
- 任务完成后，建议在 PR/变更记录中回链到任务 ID 与 Spec 产物
