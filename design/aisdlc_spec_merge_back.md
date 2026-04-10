---
title: Spec-level Merge-back phase SOP (promotion to Project SSOT + archiving evidence)
status: draft
audience: [PM, BA, SA, DEV, QA]
principles_ref: design/aisdlc.md
---
## 1. Background and target (alignment`design/aisdlc.md`)

Merge-back (return/promotion) is the final stage of the Spec Pack life cycle: the "reusable, manageable, and binding future requirements" information in the **Requirement-level Spec Pack** is promoted to the **Project-level SSOT (Project SSOT / project/)**, and the remaining content remains in the Spec Pack as delivery evidence and audit materials.

### 1.1 Construction goals of Project SSOT (deciding “what should be upgraded / what should not be upgraded”)

The value of Project SSOT is not to "summarize all the requirements details", but to provide long-term stability:

- **Map layer (clear entrance)**: where is the authoritative entrance, where are the boundaries, and where to view the contract/ADR/Runbook.
- **Guardrail layer (clear invariants)**: Key invariants of API/Data, component boundary cutting, permissions/auditing/idempotence/version compatibility and other long-term constraints.
- **Evidence chain (traceable/executable)**: points to the authoritative evidence in the warehouse (OpenAPI/Schema/DDL/script/CI job/monitoring entry), rather than an unverifiable description.
- **Progressive Disclosure (Low Noise)**: Project layers are kept short and stable; one-time delivery details stay in Spec Pack (avoiding long-term assets being polluted by noise).

Therefore, the focus of Merge-back is to precipitate the content in this Spec Pack that will affect future collaboration and subsequent needs into the "entrance + guardrail + evidence chain" of the project layer.

### 1.2 Minimum output of Merge-back

- **Requirements level output (evidence list)**:`{FEATURE_DIR}/merge_back.md`- Record the Done/Not Done status of this promotion list
  - Each item must provide project-level target placement and evidence entry
- **Project Level Output (Long Term Assets)**: Updated`.aisdlc/project/`The following related assets:
  - ADR:`.aisdlc/project/adr/`- Contract:`.aisdlc/project/components/{module}.md#api-contract` / `#data-contract`
  - Ops：`.aisdlc/project/ops/`
  - NFR：`.aisdlc/project/nfr.md`(if applicable)
  - Registry:`.aisdlc/project/index.md`(Requirement status and index)

---

## 2. Input / Precondition / Contextual Access Control

### 2.1 Contextual access control (mandatory)

Before reading or writing Spec Pack and project-level assets, you must first locate`{FEATURE_DIR}`, it is forbidden to guess the path.

PowerShell (must echo`FEATURE_DIR=...`）：

```powershell
. ".\skills\spec-context\scripts\spec-common.ps1"
$context = Get-SpecContext
$FEATURE_DIR = $context.FEATURE_DIR
Write-Host "FEATURE_DIR=$FEATURE_DIR"
```> Stop on failure:`Get-SpecContext`Report an error (e.g. missing`.aisdlc`, not in the spec branch, the Spec directory structure is incomplete) must be stopped and the context repaired first.

### 2.2 Preconditions (recommended as the entry threshold for Merge-back)

-`{FEATURE_DIR}/implementation/plan.md`Exists, and the task list in it is completed or explicitly blocked (execution period evidence and audit have been written back).
- If there are external commitment/contract changes, the drafting and evidence linking have been completed in the Spec Pack (the I2 phase only allows recording to-do, and does not directly update the project).
-`.aisdlc/project/`Exists and writable (if it does not exist:`CONTEXT GAP`, you need to complete the project layer initialization/Discover/skeleton construction first).

### 2.3 Merge-back "The only collection entrance" to be done (recommended)

The implementation phase product template has been required to be in`{FEATURE_DIR}/implementation/plan.md`Medium maintenance:

-`## Merge-back 待办清单（仅记录，不在本阶段执行）`The Merge-back stage should use this paragraph as the **main input**, supplemented by`design/*`、`release/*`、`verification/*`The difference.

---

## 3. Progressive disclosure: reading order (Merge-back phase)

### 3.1 Required reading (project level, mandatory)

-`.aisdlc/project/index.md`(Registry: demand status, index entry)
-`.aisdlc/project/adr/index.md`(ADR index)
-`.aisdlc/project/components/index.md`(Component map and module page entrance)
-`.aisdlc/project/ops/`(If exists: run the asset portal)
-`.aisdlc/project/nfr.md`(If present: NFR budget entry)

Must be explicitly marked when the read fails or does not exist`CONTEXT GAP`, cannot be skipped silently.

### 3.2 On demand (demand level, minimum necessary)

-`{FEATURE_DIR}/implementation/plan.md`(Merge-back to-do and evidence entry)
-`{FEATURE_DIR}/design/*`(If exists: evidence entry for decision/contract drafting)
-`{FEATURE_DIR}/release/*`(If exists: runbook/monitoring/rollback)
-`{FEATURE_DIR}/verification/*`(If existing: reusable verification strategy, quality access control caliber)

---

## 4. “What should be promoted/what should not be promoted”: promotion judgment criteria (written into the core of the process)

For each piece of information in the Spec Pack, judge whether to be promoted to project according to the following questions:

- **Cross-requirement reuse**: Will similar requirements still be used/asked repeatedly next time?
- **Long-term guardrails/external commitments**: Does it constrain callers, data calibers, component boundaries, permission auditing, exponentiation, etc. invariants?
- **Need to be retrieved and navigated**: Will "quickly locate authoritative portals" be needed in the future to reduce guesswork?

Hit any one: should be promoted to project layer assets (entry + invariant + evidence chain).

### 4.1 Must be promoted (default)

Alignment`design/aisdlc.md`:

- **ADR (Key Decision)**: Any critical trade-off must be entered into`.aisdlc/project/adr/`and summarized in the index.
- **External contract (merged into component page by default)**
  - API: updated`.aisdlc/project/components/{module}.md#api-contract`- Data: Update`.aisdlc/project/components/{module}.md#data-contract`- **Running Assets**: Runbook/monitoring alarm/rollback policy updated to`.aisdlc/project/ops/`- **NFR Budget and Baseline**: Update if there is an impact on performance/stability/cost/security`.aisdlc/project/nfr.md`- **Registry Status**: Updated`.aisdlc/project/index.md`(Status: Released / Merged, etc.)

### 4.2 Optional promotion (high ROI, but depends on team habits)

- **Reusable testing strategies/access control standards**: such as general regression suite division, quality access control constraints (promoted when multiple requirements are reused)
- **Universal design specifications**: specifications that will be followed by multiple modules for a long time (not a single implementation detail)

### 4.3 Prohibition of promotion (to avoid contaminating the project)

- Details of one-time delivery process: task splitting, scheduling, temporary workaround, single troubleshooting record
- Large details at the field level/timing level: only put the "authoritative entry" at the project level, and the necessary details are left in the Spec Pack or pointed to schema / OpenAPI / code evidence
- Execution steps that are only valid for this release window: project layer writing port and guardrails, this execution details are still archived in Spec Pack

---

## 5. Execution steps (Merge-back operation manual that can be followed)

> Convention: Command examples are for PowerShell by default; multiple commands on the same line are used`;`separated (do not use`&&`).

### Step 0: Locate the context and perform pre-checking

1. Run`spec-context`，Return`FEATURE_DIR=...`.
2. Check whether the project layer exists:`.aisdlc/project/`.
3. Open`{FEATURE_DIR}/implementation/plan.md`,position`## Merge-back 待办清单`, as the main source of this "promotion job list".

like`.aisdlc/project/`Does not exist: mark`CONTEXT GAP`and stop (project layer initialization/Discover/skeleton construction needs to be completed first).

### Step 1: Summarize the "Promotion List" (from To-Do → Category)

put`{FEATURE_DIR}/implementation/plan.md`Merge-back to-dos in , filed under the following categories:`{FEATURE_DIR}/merge_back.md`:

- ADR
- API Contract (by module)
- Data Contract (by module)
- Ops (runbook/monitoring/rollback)
- NFR (if applicable)
- Registry (requirement status)
- Optional promotions (testing strategies/access control caliber, etc.)

Each to-do item contains at least:

- **Promotion target path** (project layer landing point)
- **Evidence Entry** (evidence in Spec Pack, authoritative evidence in warehouse)
- **Invariant summary (3–7 items)** (only required when promoted to component page contract paragraph)
- **Gap (if not completed)**: What is missing, location of candidate evidence, impact

### Step 2: ADR promotion (key decision)

For each ADR:

- in`.aisdlc/project/adr/`Add or update the corresponding ADR file (the numbering and naming are according to the project agreement).
- renew`.aisdlc/project/adr/index.md`，确保可导航。
- 在 `{FEATURE_DIR}/merge_back.md` 中将该项标记为 Done，并附上链接与证据入口（例如：Spec 中的决策段落、相关 commit/PR）。

### Step 3：API Contract 晋升（按模块更新组件页）

对每个受影响模块，更新 `.aisdlc/project/components/{module}.md#api-contract`：

- **权威入口**：OpenAPI/Proto/路由入口文件路径 + 生成命令/CI job（若存在）
- **不变量摘要**：鉴权/幂等/错误码族/版本策略/审计要求等（3–7 条，长期有效）
- **证据入口**：关键 handler/路由文件、代表性测试入口、CI 门禁入口
- **Evidence Gaps**：缺什么、候选位置、影响（缺口未补齐则不应宣称“完成”）

> 禁止：把字段大全抄到 project；字段级细节用“权威入口链接”承载。

### Step 4：Data Contract 晋升（按模块更新组件页）

对每个受影响模块，更新 `.aisdlc/project/components/{module}.md#data-contract`：

- **Ownership**：主写/只读/同步来源与边界
- **核心对象与主键**：对象名 + 主键/唯一标识 + 生命周期一句话
- **权威入口**：Schema/DDL/迁移脚本/ORM model 的路径与入口
- **不变量摘要**：口径/约束/状态机规则（3–7 条）
- **证据入口**：repository/mapper、代表性读写服务、测试入口、CI 门禁入口

### Step 5：Ops 资产晋升（运行入口）

将 `{FEATURE_DIR}/release/*` 中“长期可复用”的运行资产晋升到 `.aisdlc/project/ops/`（入口式写法）：

- Runbook 入口（不要重复单次发布执行细节）
- Monitoring/Alerts 入口（看板与告警链接、关键指标口径入口）
- Rollback 入口（策略与触发条件、关键风险点）

### Step 6：NFR 晋升（如适用）

若本次变更影响性能/稳定性/成本/安全合规护栏：

- 更新 `.aisdlc/project/nfr.md`：预算、现状、目标、验证入口（例如压测脚本/看板/门禁）

### Step 7：Registry 状态回填

更新 `.aisdlc/project/index.md` 中该 Spec 的状态到目标状态（例如 `Merged & Archived`），并确保：

- 需求级入口（Spec Pack）可追溯
- project 级资产入口可导航（ADR/组件页/ops/nfr 等）

### Step 8：回填 `{FEATURE_DIR}/merge_back.md` 并做自检

在 `{FEATURE_DIR}/merge_back.md` 中逐项标记 Done/Not Done，并完成以下自检：

- 所有 Done 项都有可点击的 project 落点链接与证据入口
- 组件页锚点可稳定跳转（`#api-contract` / `#data-contract`）
- project 层未引入“一次性交付细节双写”
- 缺口集中写在缺口清单中（结构化：缺什么/候选位置/影响/计划）

---

## 6. Merge-back 阶段 DoD（完成标准）

- `{FEATURE_DIR}/merge_back.md` 已落盘，并覆盖本次需要晋升的全部类别（ADR/API/Data/Ops/NFR/Registry）。
- project 层已完成必要更新：
  - ADR 与索引可导航；
  - 组件页契约段落具备“权威入口 + 不变量摘要 + 证据入口 + 缺口清单”；
  - ops/nfr/registry 的入口清晰可追溯。
- 若存在未完成项：必须是显式 Not Done，且写明缺口与计划；不得“静默跳过”。

---

## 7. `spec-merge-back`（worker skill）设计文档

> 本节定义 Merge-back 的 worker skill 设计，供后续实现技能时作为约束 SSOT；skill 本身不得做“下一步路由决策”，仅输出结构化摘要供 Router（`using-aisdlc`）判断。

### 7.1 技能定位与职责边界

- **技能名（建议）**：`spec-merge-back`
- **类型**：worker skill
- **职责**：
  - 门禁：必须先定位 `FEATURE_DIR`，并验证 `.aisdlc/project/` 存在
  - 收集：从 `{FEATURE_DIR}/implementation/plan.md## Merge-back 待办清单` 汇总晋升清单
  - 落盘：更新 project 级资产（ADR / components / ops / nfr / registry）
  - 回填：生成/更新 `{FEATURE_DIR}/merge_back.md`（Done/Not Done + 证据入口）
  - DoD 自检：锚点稳定、入口可达、缺口结构化
- **禁止**：
  - 在 `.aisdlc` 缺失、或不在 spec 分支时继续执行（必须停止）
  - 把一次性交付细节复制到 project（应留在 Spec Pack）
  - 在 skill 内决定“下一步做什么”（必须回到 `using-aisdlc`）

### 7.2 输入（最小）

- `spec-context` 的输出：`FEATURE_DIR`、`CURRENT_BRANCH`、`REPO_ROOT`
- `{FEATURE_DIR}/implementation/plan.md`
- `.aisdlc/project/index.md`、`.aisdlc/project/components/index.md`、`.aisdlc/project/adr/index.md`

可选输入（如存在则读取，不存在则 `CONTEXT GAP`）：

- `{FEATURE_DIR}/design/*`
- `{FEATURE_DIR}/release/*`
- `{FEATURE_DIR}/verification/*`
- `.aisdlc/project/ops/`、`.aisdlc/project/nfr.md`

### 7.3 输出（落盘）

- `{FEATURE_DIR}/merge_back.md`
- `.aisdlc/project/adr/*` 与 `.aisdlc/project/adr/index.md`
- `.aisdlc/project/components/{module}.md`（契约段落）
- `.aisdlc/project/ops/*`（入口式）
- `.aisdlc/project/nfr.md`（如适用）
- `.aisdlc/project/index.md`（Registry 状态与入口）

### 7.4 失败即停（阻断条件）

- `spec-context` 失败（不在合法 spec 分支、Spec 目录不完整、缺少 `.aisdlc`）
- `.aisdlc/project/` 不存在或不可写（`CONTEXT GAP`）
- `{FEATURE_DIR}/implementation/plan.md` 不存在（无法获得 Merge-back 待办入口）

### 7.5 结束输出：回到 Router（`using-aisdlc`）

worker skill 完成后必须输出两段：

1) 「本阶段产物已落盘。请回到 `using-aisdlc` 进行下一步路由（如未触发人工门禁，Router 可自动续跑）。」

2) `ROUTER_SUMMARY`（YAML，字段固定）：

```yaml
ROUTER_SUMMARY:
  stage: MergeBack
  artifacts:
    - "{FEATURE_DIR}/merge_back.md"
  needs_human_review: true
  blocked: false
  block_reason: ""
  notes: "已按清单晋升 ADR/契约/ops/NFR/registry，并完成自检。"
```

> 说明：Merge-back 涉及 project 级长期资产更新，默认 `needs_human_review=true`（建议评审与确认）。

---

## 8. 附录：`{FEATURE_DIR}/merge_back.md`（模板骨架）

```markdown
# Merge-back（晋升清单与证据）

> 门禁：必须先 `spec-context` 获取 FEATURE_DIR；失败即停止。
> 原则：项目层只写“入口 + 护栏 + 证据链”；一次性交付细节保留在 Spec Pack。

## 概览
- Spec：{num}-{short-name}
- 目标：将可复用资产晋升到 `.aisdlc/project/`，其余归档留证

## Done / Not Done 清单

### ADR
- [ ] ADR-xxx：`../project/adr/ADR-xxx.md`
  - 证据：`implementation/plan.md#...` / `design/design.md#...` / PR/commit

### API Contract（按模块）
- [ ] module-a：`../project/components/module-a.md#api-contract`
  - 不变量摘要：...
  - 证据入口：OpenAPI/路由/handler/测试/CI

### Data Contract（按模块）
- [ ] module-a：`../project/components/module-a.md#data-contract`
  - Ownership：...
  - 不变量摘要：...
  - 证据入口：Schema/DDL/迁移/ORM/测试/CI

### Ops
- [ ] Runbook：`../project/ops/...`
- [ ] Monitoring：`../project/ops/...`
- [ ] Rollback：`../project/ops/...`

### NFR（如适用）
- [ ] `.aisdlc/project/nfr.md` 已更新
  - 证据入口：压测/门禁/看板

### Registry
- [ ] `.aisdlc/project/index.md` 已更新状态为：Merged & Archived

### 可选晋升（高 ROI）
- [ ] 通用测试策略/质量门禁口径：`../project/...`

## Evidence Gaps（缺口清单）
- Gap-001：
  - 缺什么：
  - 候选证据位置：
  - 影响：
  - 计划（Owner/截止/下一步动作）：
```

