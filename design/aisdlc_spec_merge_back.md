---
title: Spec 级 Merge-back 阶段 SOP（晋升到 Project SSOT + 归档证据）
status: draft
audience: [PM, BA, SA, DEV, QA]
principles_ref: design/aisdlc.md
---

## 1. 背景与目标（对齐 `design/aisdlc.md`）

Merge-back（回档/晋升）是 Spec Pack 生命周期的最后阶段：将**需求级 Spec Pack**中“可复用、可治理、会约束未来需求”的信息晋升到**项目级 SSOT（Project SSOT / project/）**，其余内容仍保留在 Spec Pack 作为交付证据与审计材料。

### 1.1 Project SSOT 的建设目标（决定“该升什么 / 不该升什么”）

Project SSOT 的价值不是“汇总所有需求细节”，而是长期稳定地提供：

- **地图层（入口清晰）**：哪里是权威入口、边界在哪、从哪里看契约/ADR/Runbook。
- **护栏层（不变量清晰）**：API/Data 的关键不变量、组件边界裁切、权限/审计/幂等/版本兼容等长期约束。
- **证据链（可追溯/可执行）**：指向仓库内的权威证据（OpenAPI/Schema/DDL/脚本/CI job/监控入口），而不是不可验证的描述。
- **渐进式披露（低噪音）**：项目层保持短、稳定；一次性交付细节留在 Spec Pack（避免长期资产被噪音污染）。

因此，Merge-back 的重点是：把本次 Spec Pack 里**会影响未来协作与后续需求**的内容，沉淀为 project 层的“入口 + 护栏 + 证据链”。

### 1.2 Merge-back 的最小输出

- **需求级输出（证据清单）**：`{FEATURE_DIR}/merge_back.md`
  - 记录本次晋升清单的 Done/Not Done 状态
  - 每项必须给出 project 级目标落点与证据入口
- **项目级输出（长期资产）**：更新 `.aisdlc/project/` 下相关资产：
  - ADR：`.aisdlc/project/adr/`
  - 契约：`.aisdlc/project/components/{module}.md#api-contract` / `#data-contract`
  - Ops：`.aisdlc/project/ops/`
  - NFR：`.aisdlc/project/nfr.md`（如适用）
  - Registry：`.aisdlc/project/index.md`（需求状态与索引）

---

## 2. 输入 / 前置条件 / 上下文门禁

### 2.1 上下文门禁（强制）

凡读写 Spec Pack 与 project 级资产，必须先定位 `{FEATURE_DIR}`，禁止猜路径。

PowerShell（必须回显 `FEATURE_DIR=...`）：

```powershell
. ".\skills\spec-context\scripts\spec-common.ps1"
$context = Get-SpecContext
$FEATURE_DIR = $context.FEATURE_DIR
Write-Host "FEATURE_DIR=$FEATURE_DIR"
```

> 失败即停止：`Get-SpecContext` 报错（例如缺少 `.aisdlc`、不在 spec 分支、Spec 目录结构不完整）必须停止，先修复上下文。

### 2.2 前置条件（建议作为 Merge-back 的进入门槛）

- `{FEATURE_DIR}/implementation/plan.md` 已存在，并且其中的任务清单已完成或明确阻塞（执行期证据与审计已回写）。
- 若存在对外承诺/契约变更，已在 Spec Pack 内完成草拟与证据链接（I2 阶段只允许记录待办，不直接更新 project）。
- `.aisdlc/project/` 已存在且可写（若不存在：`CONTEXT GAP`，需先完成 project 层初始化/Discover/骨架搭建）。

### 2.3 Merge-back 待办的“唯一收集入口”（推荐）

实现阶段产物模板已要求在 `{FEATURE_DIR}/implementation/plan.md` 中维护：

- `## Merge-back 待办清单（仅记录，不在本阶段执行）`

Merge-back 阶段应以该段落作为**主要输入**，再补充来自 `design/*`、`release/*`、`verification/*` 的差量。

---

## 3. 渐进式披露：读取顺序（Merge-back 阶段）

### 3.1 必读（项目级，强制）

- `.aisdlc/project/index.md`（Registry：需求状态、索引入口）
- `.aisdlc/project/adr/index.md`（ADR 索引）
- `.aisdlc/project/components/index.md`（组件地图与模块页入口）
- `.aisdlc/project/ops/`（如存在：运行资产入口）
- `.aisdlc/project/nfr.md`（如存在：NFR 预算入口）

读取失败或不存在时必须显式标注 `CONTEXT GAP`，不得静默跳过。

### 3.2 按需（需求级，最小必要）

- `{FEATURE_DIR}/implementation/plan.md`（Merge-back 待办与证据入口）
- `{FEATURE_DIR}/design/*`（如存在：决策/契约草拟的证据入口）
- `{FEATURE_DIR}/release/*`（如存在：runbook/monitoring/rollback）
- `{FEATURE_DIR}/verification/*`（如存在：可复用验证策略、质量门禁口径）

---

## 4. “该升什么 / 不该升什么”：晋升判定口径（写进流程的核心）

对 Spec Pack 中每条信息，按以下问题判断是否晋升到 project：

- **跨需求复用**：下次类似需求仍会用到/会重复被问到吗？
- **长期护栏/对外承诺**：它是否约束调用方、数据口径、组件边界、权限审计、幂等等不变量？
- **需要被检索与导航**：未来是否需要“快速定位权威入口”来减少猜测？

命中任意一条：应晋升为 project 层资产（入口 + 不变量 + 证据链）。

### 4.1 必须晋升（默认）

对齐 `design/aisdlc.md`：

- **ADR（关键决策）**：任何关键取舍必须进入 `.aisdlc/project/adr/` 并在索引汇总。
- **对外契约（默认合并到组件页）**
  - API：更新 `.aisdlc/project/components/{module}.md#api-contract`
  - Data：更新 `.aisdlc/project/components/{module}.md#data-contract`
- **运行资产**：Runbook/监控告警/回滚策略更新到 `.aisdlc/project/ops/`
- **NFR 预算与基线**：如对性能/稳定性/成本/安全产生影响，更新 `.aisdlc/project/nfr.md`
- **Registry 状态**：更新 `.aisdlc/project/index.md`（状态：Released / Merged 等）

### 4.2 可选晋升（高 ROI，但视团队习惯）

- **可复用测试策略/门禁口径**：例如通用回归套件划分、质量门禁约束（当多次需求重复复用时晋升）
- **通用设计规范**：会被多个模块长期遵循的规范（而非单次实现细节）

### 4.3 禁止晋升（避免污染 project）

- 一次性交付过程细节：任务拆分、排期、临时 workaround、单次排障记录
- 字段级/时序级大段细节：项目层只放“权威入口”，必要细节留在 Spec Pack 或指向 schema / OpenAPI / 代码证据
- 仅对本次发布窗口有效的执行步骤：项目层写入口与护栏，本次执行细节仍归档在 Spec Pack

---

## 5. 执行步骤（可照做的 Merge-back 操作手册）

> 约定：命令示例默认面向 PowerShell；同一行多命令用 `;` 分隔（不要用 `&&`）。

### Step 0：定位上下文并进行前置检查

1. 运行 `spec-context`，回显 `FEATURE_DIR=...`。
2. 检查 project 层是否存在：`.aisdlc/project/`。
3. 打开 `{FEATURE_DIR}/implementation/plan.md`，定位 `## Merge-back 待办清单`，作为本次“晋升工作清单”的主来源。

若 `.aisdlc/project/` 不存在：标注 `CONTEXT GAP` 并停止（需要先完成 project 层初始化/Discover/骨架搭建）。

### Step 1：汇总“晋升清单”（从待办 → 分类）

把 `{FEATURE_DIR}/implementation/plan.md` 中的 Merge-back 待办，按下列类别归档到 `{FEATURE_DIR}/merge_back.md`：

- ADR
- API Contract（按模块）
- Data Contract（按模块）
- Ops（runbook / monitoring / rollback）
- NFR（如适用）
- Registry（需求状态）
- 可选晋升（测试策略/门禁口径等）

每条待办至少包含：

- **晋升目标路径**（project 层落点）
- **证据入口**（Spec Pack 内证据、仓库内权威证据）
- **不变量摘要（3–7 条）**（仅当晋升到组件页契约段落时需要）
- **缺口（如未完成）**：缺什么、候选证据位置、影响

### Step 2：ADR 晋升（关键决策）

对每条 ADR：

- 在 `.aisdlc/project/adr/` 新增或更新对应 ADR 文件（编号与命名按项目约定）。
- 更新 `.aisdlc/project/adr/index.md`，确保可导航。
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

