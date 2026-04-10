---
title: Spec level implementation phase SOP (plan/execution)
status: draft
audience: [PM, BA, DEV, QA]
principles_ref: design/aisdlc.md
---
# Implementation phase process (I1 planning / I2 execution)

## 1. Background and target (alignment`design/aisdlc.md`)

This solution is used to improve efficiency in the "implementation phase" of **Spec level**: on the premise of following "double-layer SSOT + Spec as Code + progressive disclosure", use **reusable implementation SOP** to steadily advance requirements to a "directly executable implementation plan (including task list and status)", and complete the delivery closed loop with batch execution and checkpoint reporting.

**Conclusion**:
- **I1 It is necessary to implement the plan**: Output`{FEATURE_DIR}/implementation/plan.md`, and use it as the only execution list with status SSOT (including tasks`- [ ]/- [x]`, each step command, expected output, submission point and audit information).
- **I2 execution is a must**: with`{FEATURE_DIR}/implementation/plan.md`For input, execute in batches and report at checkpoints; stop immediately if blocked, and do not make assumptions.
- This phase **does not include** the formal products of verification / release (the corresponding outputs of each phase); but each task in the implementation plan must declare its minimum verification method.

---

## 2. Product placement and “progressive disclosure” reading sequence

### 2.1 Recommended placement structure (demand level Spec Pack)

Alignment`design/aisdlc.md`Requirements level directory in (example):```text
.aisdlc/specs/<DEMAND-ID>/
  index.md
  requirements/
    ...                   # 已完成的需求分析产物
  design/
    ...                   # 已完成的设计产物
  implementation/
    plan.md               # I1 实现计划（必做；唯一执行清单与状态 SSOT）
```> Description: This SOP embeds "task decomposition" into`implementation/plan.md`(Write directly to the executable by writing the plan), therefore`implementation/tasks.md`It is no longer a must-have product for access control.

### 2.2 Agent reading order (progressive disclosure)

- **Required Reading (project-level, mandatory, aligned context injection protocol)**:
  -`project/memory/*`(Business/Technology/Structure/Terminology)
  - of the affected modules`project/components/{module}.md`API/Data contract paragraph + Evidence entry (from`requirements/solution.md#impact-analysis`Get a list of affected modules)
  - Relevant ADRs (obtained from impact analysis)
  -`.gitmodules`(If present; used to identify submodule static lists and paths that can participate in implementation)
  - Mark when reading fails`CONTEXT GAP`- **On demand (requirement level)**: Only process a certain`<DEMAND-ID>`When reading this requirement:
  - **Impact Analysis (required reading)**:`specs/{id}/requirements/solution.md#impact-analysis`(R1.5 output, get affected modules and invariants)
  - **Requirement Path**:`requirements/*`(Include`solution.md`or`prd.md`)
  - **Design Path**:`design/*`(Include`design.md`or`solution.md`)
- **Implementation Phase SSOT**:`implementation/plan.md`(The only source of execution list and status)
- **Write back (into the library)**: Each module produces a file independently, keeping it replaceable and auditable

### 2.3 Automatic context recognition mechanism

Alignment`design/aisdlc_spec_init.md`The "context automatic identification mechanism" in requires that all spec-level commands must first obtain the current spec-related context information before execution:

- Call script function`Get-SpecContext`(lie in`skills/spec-context/scripts/spec-common.ps1`)
- get`REPO_ROOT`、`CURRENT_BRANCH`、`FEATURE_DIR`、`SPEC_NUMBER`、`SHORT_NAME`- If the warehouse exists`.gitmodules`, additionally output submodule status snapshot (such as`SUBMODULE_SET_JSON`), used to implement phase verification of the branch/HEAD/dirty workspace status of the affected sub-repository
- Based on`FEATURE_DIR`Automatically locate input/output paths, for example:
  -`implementation/plan.md` → `{FEATURE_DIR}/implementation/plan.md`> Constraints:`FEATURE_DIR`It is still only parsed from the root project branch; submodule only provides the code workspace status during the implementation period and does not host Spec documents.

---

## 3. Implement SOP overview (unified process)

**Process**:`I1 实现计划（必做） → I2 执行（必做）`**Shortest Path (Small Requirement)**:`I1 实现计划 → I2 执行`Description:
- **MINIMUM INPUT**:`requirements/solution.md`or`requirements/prd.md`(at least one of them)
- **Access Control Requirements**: If the input is insufficient, it must be`plan.md`Mark "NEEDS CLARIFICATION" and block access to I2
- **Routing Authority**: The "next step" of this stage is given by`using-aisdlc`Determined as the only router; I1/I2 are worker skills, and will return to`using-aisdlc`Reroute (usually I1→I2→Finish).

---

## 3.1 Skill responsibility boundary (I1/I2 is worker skill)

In the implementation phase, SOP uses "skill" as the execution unit; the skill definition file serves as the SSOT of execution constraints. This document only clarifies the responsibility boundaries and link relationships of I1/I2 to avoid inventing "next routing" calibers in multiple technologies.

### 3.1.1 Skill List

- **`spec-plan`**:generate`{FEATURE_DIR}/implementation/plan.md`(SSOT only; contains task list and status).
  - **Reverse source (reference only)**:`skills/writing-plans/SKILL.md`
- **`spec-execute`**:according to`{FEATURE_DIR}/implementation/plan.md`Execute in batches and report at checkpoints; stop when blocked.
  - **Reverse source (reference only)**:`skills/executing-plans/SKILL.md`### 3.1.2 Skill Link (Concept Map)```mermaid
flowchart TD
  specContext[spec-context_Get-SpecContext] --> planDoc[implementation_plan_md_SSOT]
  planDoc --> implPlan[spec-plan]
  planDoc --> implExec[spec-execute]
```---

## 4. Prompt words for execution steps (structured requirements)

The following step structure is used for the execution description of specific modules, with emphasis on "access control" and "clarification items":

1. **Setup**:
   - Read the current requirement context (branch/directory) and determine`<DEMAND-ID>`and`specs/<DEMAND-ID>/implementation/`Directory
   - Must be used first`spec-context`run`Get-SpecContext`and echo`FEATURE_DIR=...`;Stop on failure (path guessing is prohibited)
2. **Load context**:
   - Read key products (minimum read on demand):
     - **Requirement Path**:`requirements/solution.md`、`requirements/prd.md`- **Design Path**:`design/design.md`(if exists)
   - and project level`memory/`、`components/`、`adr/`3. **Execute workflow**:
   - Execute according to the module template, **mark unknown items as "NEEDS CLARIFICATION"**
   - **If the access control fails, an error message** (ERROR) will be reported, and the next stage of product is not allowed to be placed.
4. **Stop and report**:
   - Report on the stage of execution, product path and unresolved clarification items

---

## 5. Module I1: Implementation plan (required)

### 5.1 Goals

Convert requirements/design into a **directly executable implementation plan (SSOT)**: In addition to scope/milestones/dependencies/risks/acceptance, it must also include "task list (checkbox) + executable steps for each task (including commands and expected output) + submission points + audit information" so that it can be executed in batches without ambiguity.

### 5.2 Input

- **Requirement Path**:`requirements/solution.md` / `requirements/prd.md`- **Impact Analysis (required reading)**:`{FEATURE_DIR}/requirements/solution.md#impact-analysis`(R1.5 output), obtain the list of affected modules, invariants to be observed, and related ADRs
- **Design Path**:`design/design.md`(If present; include "alignment with existing systems" statement)
- **Project-level resources (enforced, aligned context injection protocol)**:
  -`project/memory/*`(Business/Technology/Structure/Terminology)
  - of the affected modules`project/components/{module}.md`(API/Data contract paragraph + Evidence entry + state machine/domain event)
  - Full text of relevant ADRs
  - Cross-module dependencies (from`components/index.md`Obtain dependency graph)
  -`.gitmodules`(If present; static fact used to establish "affected subrepositories = which submodule paths")

### 5.3 Output (drop to`{FEATURE_DIR}/implementation/plan.md`;only SSOT)

#### 5.3.1`plan.md`Head (required)

> Below are the placeholder skills`spec-plan`right`plan.md`Minimum head structure requirements (reference`writing-plans`idea, but the output location is changed to Spec Pack).```markdown
# [需求名] 实现计划（SSOT）

> **必需技能：** `spec-execute`（按批次执行本计划）
> **上下文门禁：** 必须先用 `spec-context` 定位 `{FEATURE_DIR}`，失败即停止

**目标：** [一句话描述要交付什么]
**范围：** In / Out
**架构：** [2–3 句方法说明 + 关键约束]
**验收口径：** [引用 requirements/solution.md 或 requirements/prd.md 的 AC/验收点]
**影响范围：** [引用 requirements/solution.md#impact-analysis 的受影响模块清单]
**需遵守的不变量：** [从影响分析提取的关键 API/Data 契约不变量]
**子仓范围：** [引用 `.gitmodules` + `impact-analysis`，列出本次需求涉及的 submodule；无则写“无”]

---
```#### 5.3.2 Plan text (required)

- **TL;DR**: Summarize the plan goals and scope in one sentence
- **Scope and Boundaries**: In/Out (aligning requirements and design)
- **Influence scope and constraints (based on R1.5 impact analysis, required)**:
  - List of affected modules and impact types (reference`requirements/solution.md#impact-analysis`)
  - API/Data contract invariants that need to be complied with (listed item by item, marked with source modules)
  - State machine/domain event constraints to be adhered to (if involved)
  - Cross-module impact and coordination matters
- **Code workspace list (required, if there is a submodule)**:
  - The submodule involved in this requirement (from`.gitmodules`Reference path in)
  - Whether each sub-warehouse`required`- Whether it is required to keep the Spec branch with the same name as the root project
  - If exceptions exist, log them`exception_reason`- **Milestones and Rhythm**: Phase split, time estimate, deliverable list
- **Dependencies and Resources**: External systems/teams/permissions/environments/data dependencies
- **Risk and Verification**: Risk List, Verification Method, Owner
- **Acceptance Caliber**: Key AC and Acceptor corresponding to PRD/Program
- **Item to be confirmed**: All marked as "NEEDS CLARIFICATION" (Do not enter I2 before elimination)

#### 5.3.3 Task List (required; SSOT)`plan.md`Must contain a "checkable" task list as the only execution list and status source (`- [ ]/- [x]`). Each task must be split into executable steps with an action granularity of 2–5 minutes, emphasizing: **TDD, DRY, YAGNI, frequent submission**.

Task template (sample skeleton):```markdown
## 任务清单（SSOT）

### Task T1: [任务标题]

- [ ] **状态**：未开始 / 进行中 / 完成 / 阻塞（阻塞必须写明取证路径）

**代码仓范围：**
- 根项目：`<root repo path or module>`
- 子仓：`<submodule path>`（`required=true|false`，默认分支=`{CURRENT_BRANCH}`）

**文件：**
- 创建：`exact/path/to/new.file`
- 修改：`exact/path/to/existing.file`（可选：精确到段落/函数）
- 测试：`tests/exact/path/to/test.file`（如适用）

**验收点：**
- [可验证条件 1]
- [可验证条件 2]

**步骤 1：写失败测试（如适用）**
- Run: `[精确命令]`
- Expected: FAIL（写出期望看到的关键失败信号）

**步骤 2：写最少实现**
- 修改点：`path/to/file`

**步骤 3：运行验证**
- Run: `[精确命令]`
- Expected: PASS（写出期望看到的关键通过信号）

**步骤 4：提交（频繁提交；commit message 必须中文）**
- Commit message: `[一句话说明 why]`
- 审计信息：
  - repo: `root`
    branch: `<CURRENT_BRANCH>`
    commit: `<TBD>`
    pr: `<TBD>`
    changed_files: `<TBD>`
  - repo: `<submodule path>`（如适用）
    branch: `<CURRENT_BRANCH>`
    commit: `<TBD>`
    pr: `<TBD>`
    changed_files: `<TBD>`
```### 5.4 Access Control (I1-DoD)

- Plan scope and`requirements/*`、`design/*`**Consistent**
- Milestones are clear and acceptable (each item has a corresponding product or verifiable standard)
- Dependencies and risks are listed with minimal verification/mitigation actions
- Key acceptance criteria are traceable (at least cited`prd.md`or`solution.md`)
- **Influence scope and constraints injected**:`plan.md`Contains the "Scope of Influence and Constraints" paragraph, the affected modules and the invariants that need to be observed have been changed from`requirements/solution.md#impact-analysis`Extract and itemize
- If`.gitmodules`Exists and affects the analysis hit sub-bin:`plan.md`Affected sub-warehouses have been listed,`required`Tags, default branch requirements with the same name, and exception reasons
-`plan.md`The memory is in the "Task List (SSOT)", and each task includes: file path, acceptance point, minimum verification method, submission point and audit information
- Any uncertainties are marked as "NEEDS CLARIFICATION" and must not be entered into I2 until cleared

---

## 6. Module I2: Execution (required)

### 6.1 Objectives

will`{FEATURE_DIR}/implementation/plan.md`Tasks defined in are executed in batches, with review checkpoints set between each batch; blockages are immediately stopped and asked for clarification, rather than guessing ahead.

### 6.2 Input

-`{FEATURE_DIR}/implementation/plan.md`(Required; SSOT, including the "scope of influence and constraints" paragraph)
-`requirements/*`、`design/*`(according to`plan.md`The reference path in the reference path is read on demand)
-`{FEATURE_DIR}/requirements/solution.md#impact-analysis`(R1.5 output, review affected modules and invariants as needed)
- Project level of affected modules`project/components/{module}.md`(API/Data contract section, **read-only**, used to verify invariant compliance during implementation)
-`.gitmodules`(If it exists; used to identify whether the sub-warehouse path declared in the plan actually exists)
-`spec-context`Returned submodule status snapshot (if exists; used to verify branch consistency, detached HEAD, dirty workspace)

### 6.3 Output (execution process writeback; to`plan.md`as the only source of status)

- **Code and Configuration Changes**: Completed implementation in the repository (press`plan.md`Specified path/deliverable per task).
- **Status writeback (only)**: Update`{FEATURE_DIR}/implementation/plan.md`Corresponding tasks:
  - Replace completed tasks from`- [ ]`marked as`- [x]`- Supplement the minimum auditable information: write back by repo`branch` / `commit` / `pr` / `changed_files`/Key verification results
  - Blocking tasks must be written clearly: what is missing, how to complete it, who to obtain evidence from/where to obtain evidence from
- **Decision and Contract Drafting (Spec is placed in the disk, direct updates to project/ are prohibited)** (if generated during execution):
  - **Draft ADR**: Priority recorded in`{FEATURE_DIR}/design/design.md`"Decision/Weighing" paragraph; if you need a separate document, you can add`{FEATURE_DIR}/design/adr/`ADR draft under (Demand level assets only)
  - **Draft Contract**: In`{FEATURE_DIR}/design/`Internal Draft/Update (requirement level assets; available`design/contract-delta.md`or in`design/design.md`Record the contract difference and evidence entry)
  - **Merge-back to-do (only recorded, not executed at this stage)**: in`plan.md`Add a "Merge-back to-do list" section to record the ADR/contract/operation and maintenance/NFR changes and evidence entries that need to be promoted; subsequent processing will be handled by an independent Merge-back process (see`design/aisdlc.md`)

> Note: This SOP does not force the addition of additional execution log files; if you need more detailed auditing, you can`implementation/`Supplement`execution-log.md`,but`plan.md`Still the only source of execution list and status.

### 6.4 Execution rhythm (batch + checkpoint; corresponding placeholder skills`spec-execute`)

1. **Load and rigorously review the plan (Review)**
   - read`{FEATURE_DIR}/implementation/plan.md`- Identify plan flaws: unclear commands/missing validation/out of bounds/missing dependencies/existence NEEDS CLARIFICATION
   - If`.gitmodules`exist and`plan.md`The statement involves sub-repositories: Check whether these sub-repositories have created Spec branches with the same name as the root project; if the branches are inconsistent, in detached HEAD, or there are undeclared exceptions, **Stop and report before starting**
   - If there is a critical concern: **Stop and report before you start** (no guesswork)

2. **Batch execute**
   - Default: execute the first 3 unfinished tasks in each batch (can be adjusted according to risks and dependencies)
   - Follow the steps strictly for each task:
     - Pre-check (whether dependencies/permissions/environment/input are met)
     - Implement changes
     - Run a minimal validation of the mission statement and log key outputs
     - Write back status to`plan.md`(checkbox + audit information)

3. **Batch checkpoint report (Report checkpoint)**
   - Must report after each batch is completed: completed tasks, summary of verification results, unfinished tasks, list of blocked items
   - **Wait for feedback** before entering the next batch

4. **Stop on block**
   - Immediately stop and report situations: missing dependencies, repeated verification failures, unclear instructions, critical flaws in the plan, and NEEDS CLARIFICATION blocking.
   - Principle: **Seek clarification, not speculation**

### 6.5 Access Control (I2-DoD)

-`plan.md`All "planned tasks" in have been processed:
  - Those that can be completed are marked as`- [x]`and contain minimal audit information
  - If you cannot continue due to clarification obstruction, you must write down the reason for the obstruction and the evidence collection path at the task (no silent skipping)
- Output vs.`plan.md`Consistent scope/milestones, no out-of-bounds implementation
- If`plan.md`declare existence`required`Subrepositories: These subrepositories have maintained the Spec branch with the same name as the root project at execution time, or exceptions have been explicitly left
- If key decisions/contract changes occur: Already in`{FEATURE_DIR}`Complete the draft within`plan.md`The promotion list and evidence entry are included in the "Merge-back to-do list" (the Spec stage is not directly updated`project/*`)

## 7. Traceability and writeback tips

-`{FEATURE_DIR}/implementation/plan.md`Must quote the corresponding`requirements/*`and`design/*`(maintain traceability)
- Status written back to`plan.md`As the only source (checkbox + audit information);
- When submodule is involved, audit information must retain the repo dimension (root project/subrepository path/branch/commit/pr/changed_files)
- Key decisions/contract changes generated during the implementation process: **Only drafts are placed in the Spec directory**; Merge-back to-do and evidence entries are recorded in`plan.md`, and subsequently promoted/synchronized to`project/adr/`corresponding to`project/components/{module}.md`contract paragraph
- It is recommended to link back to the task ID and Spec product path in the PR/commit message (for example:`specs/<DEMAND-ID>/implementation/plan.md#Task-T1`）
