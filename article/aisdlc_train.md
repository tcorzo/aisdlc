---
title: AI SDLC (aisdlc) team training handouts
status: draft
audience:
  - PM
  - BA
  - UX
  - DEV
  - QA
  - TL
  - SRE
repo: sdlc-dev
markdown-sharing:
  uri: 97db1123-6412-4e1a-9d9a-9362839137df
---
## AI SDLC (aisdlc) team training handout

### 1. Training goals and boundaries

#### 1.1 What you will master

- **Core Goal**: Allow the team to use AI SDLC (aisdlc) to steadily promote "requirements→design→implementation→verification closing" in this warehouse, and precipitate key knowledge into maintainable SSOT.
- **Key Abilities**:
  - **Know the process**: Know what to read/write/how to stop/how to accept at each stage.
  - **Ability to select skills**: Can choose the correct one according to the scene`skill`(And execute according to access control).
  - **Can stop losses**: No brain-braining, no guessing of paths, no scattered TODO/to-be-confirmed documents, and can stop correctly and propose evidence collection paths when encountering obstructions.

#### 1.2 What this handout does not cover

- It does not talk about specific business, nor does it replace the engineering specifications of each team (testing strategy, release strategy, etc. are still subject to the actual project).
- Do not pursue "translating all codes into documents": the project level only does **map layer + authoritative entrance + evidence chain**, not a complete list of fields.

---

### 2. Core concept (must be aligned first)

#### 2.1 Double-layer SSOT (Single Source of Truth)

- **Project Level SSOT (Long Term Asset)**:`.aisdlc/project/`Used for long-term stable facts: portals, boundaries, contract authority portals, evidence chains, operational portals (ops), ADR, etc.
- **Requirement level SSOT (Spec Pack, delivery closed loop)**:`.aisdlc/specs/{num}-{short-name}/`One package for each requirement, used for the entire process of evidence and products from clarification to delivery of the requirement; after completion, reusable assets are promoted back to the project level through **Merge-back**.

#### 2.2 Progressive Disclosure

- **Read the map first, then collect evidence as needed**: Read the project level first`memory/`and Index (Map Layer), then go to the Affected Modules page with the Minimum Necessary Files for Spec Pack.
- **Missing must be explicitly marked**: Project-level input missing/failed to read must be explicitly marked as`CONTEXT GAP`, you cannot silently skip and continue to advance with your brain.

#### 2.3 Gates and Stop Mechanism

- **The meaning of access control**: Let AI and humans "not write files in error context, not advance when SSOT is missing, and not treat the unknown as known".
- **Stop is not failure**: Stopping means that you recognize the lack of evidence/lack of input/the presence of a blockage and turn the problem into an "executable next step".

---

### 3. Two main lines

#### 3.1 Project-level Discover (reverse engineering of existing projects)

Used for "I want AI/newcomers to no longer guess entrances, boundaries, and contracts", placed on`.aisdlc/project/...`, the core is **map layer + authoritative entrance + evidence chain** and sustainable maintenance (Delta Discover/stale).

#### 3.2 Demand-level Spec Pack (delivery closed loop)

Used for "I want to deliver a requirement/change", placed in`.aisdlc/specs/{id}/...`, the core is **traceable delivery closed loop**.

#### 3.3 Recommended implementation order (team level: project level first, then demand level)

Before the team uses aisdlc on a large scale, it is recommended to implement it in the following order (to avoid "guessing the entrance/guessing the boundary/guessing the contract" for every subsequent requirement):

- **Do project-level Discover (MVP) first**: at least`.aisdlc/project/memory/*`、`components/index.md`Create with 1–3 P0 module pages (containing contract paragraphs and evidence chains).
- **Run the demand level Spec Pack again**: At this time, R1/D2/I1 can "look at the map first, and then obtain evidence as needed", and the impact analysis/design alignment/implementation plan will be significantly more stable.

---

### 4. Project-level Discover (reverse engineering of existing projects): process and skill mapping (recommended to do first)

#### 4.1 The goal of Discover (not a complete list of fields)

Create`.aisdlc/project/`Project-level SSOT allows AI/newcomers to guess less about entrances, boundaries, and contracts:

- **Map Layer**: Index navigation only (no double-writing details)
- **Authoritative Entry**: Module page single page SSOT (fixed anchor)
- **Evidence Chain**: Each key conclusion points to locatable evidence or structured gaps (Evidence Gaps)

#### 4.2 Discover sub-skill link (four-stage)

| What are you going to do now | Which skill to use | Main output |
|---|---|---|
| Step0+1: Inventory evidence entrance + P0/P1/P2 stop loss |`project-discover-preflight-scope` | `.aisdlc/project/components/index.md`(Navigation only) + Entry list is moved to subsequent memory/ops |
| Step2+3: North Star (memory) + index skeleton |`project-discover-memory-index` | `.aisdlc/project/memory/*` + `components/index.md` + `products/index.md`|
| Step4: Module page + contract paragraph + evidence chain |`project-discover-modules-contracts` | `.aisdlc/project/components/{module}.md`|
| Step5+6+7+11: Products convergence + Ops entry + DoD + incremental maintenance |`project-discover-products-ops-dod` | `.aisdlc/project/products/*` + `.aisdlc/project/ops/*`+ DoD/Delta/stale rules |

#### 4.3 Hard rules of Discover (the team must memorize them)

- Prohibited`.aisdlc/project/contracts/**`(API/Data contract merged into module page fixed section).
- Index navigation only:`components/index.md`、`products/index.md`Do not write invariants/fields/processes/"to be filled".
- P0 module page must contain fixed title (anchor stable):`## TL;DR`、`## API Contract`、`## Data Contract`、`## Evidence`、`## Evidence Gaps`.
- Write if there is lack of evidence`Evidence Gaps`(Structured: gap/expected granularity/candidate evidence location/impact), prohibiting "to be filled/not found/TODO" scattered in the text.
- Scope stop loss first: first make 1–3 P0 modules a traceable three-piece set, and then expand.
- Products converges to<= 6（否则地图失效；无法收敛要写明原因与治理建议入口）。

#### 4.4 Discover MVP：做到什么程度，才“值得大规模跑 Spec Pack”

建议把以下内容视为“项目级知识库最小可用交付”（达到后，需求侧 Skill 的上下文注入才有稳定输入）：

- **Level-0（北极星）**：`.aisdlc/project/memory/structure.md`、`tech.md`、`product.md`、`glossary.md`（短、可导航、入口可定位；缺口进 Evidence Gaps）
- **Level-1（地图层）**：`.aisdlc/project/components/index.md`（只导航 + 依赖图 + 进度复选框）
- **P0 模块 1–3 个先做深**：`.aisdlc/project/components/{module}.md`（含 `TL;DR` + `API/Data Contract` + `Evidence/Evidence Gaps`）

>If the project-level knowledge base has not reached MVP: the demand side can still run Spec Pack, but must accept "`CONTEXT GAP`multiple, weak impact analysis, and design/implementation more prone to drift” reality, and make the Discover MVP a near-term priority.

---

### 5. Requirement-level Spec Pack: End-to-end process (R → D → I → Finish)

#### 4.1 Overview (one node = one skill = one product)

**Demand Link (optional R0–R4)**:

- R0：`raw.md`(Original input placement)
- R1:`solution.md`(Recommended plan + verification checklist will be produced after the clarification is completed)
- R2:`prd.md`(Optional, freeze delivery specifications)
- R3:`prototype.md`(optional, ASCII prototype, to disambiguate interactions)
- R4: Demo (optional, interactive walkthrough)

**Design decision link (optional D0–D2, the whole can be skipped)**:

- D0: Diversion (determine whether to skip design; when skipping`plan.md`Complete the minimum decision information)
-D1:`design/research.md`(Optional, research conclusion + verification checklist)
-D2:`design/design.md`(Required if not skipped, decision document/RFC)

**Develop execution link (must do I1–I2 + Finish)**:

- I1:`implementation/plan.md`(**Only execution list and status SSOT**)
- I2: Press`plan.md`Execute in batches and write back status/audit information (status only writes back`plan.md`)
- Finish: only perform verification and generate a completion confirmation report (all green is considered complete)

#### 4.2 Demand-level hard access control: positioning first`FEATURE_DIR`(Guessing the path is prohibited)

As long as you can read and write any Spec Pack file (`requirements/*`、`design/*`、`implementation/*`Or R4 to write demo), you must first use **`spec-context`** Get and echo:

-`FEATURE_DIR=...`(Requirement package root directory)
- (still needed for R4)`CURRENT_BRANCH`、`REPO_ROOT`Corresponding skills:

-`skills/spec-context/SKILL.md`：`spec-context`#### 4.3 Shortest closed loop (recommended path for simple requirements)

Applicable: Single scope, low risk, acceptance criteria can be within`solution.md`Write clearly.

-`spec-init` → `spec-context` → `spec-product-clarify` → `spec-plan` → `spec-execute` → `finishing-development`#### 4.4 Regular closed loop (when specification/interaction alignment is required)

-`spec-init` → `spec-context` → R1 `spec-product-clarify`- Execute on demand: R2`spec-product-prd` → R3 `spec-product-prototype` → R4 `spec-product-demo`- Enter design on demand: D1`spec-design-research`(optional) → D2`spec-design`- Must-do implementation: I1`spec-plan` → I2 `spec-execute` → Finish `finishing-development`---

### 6. Demand link (R0–R4): Applicable scenarios and skills

#### 5.1 R0: Initializing Spec Pack (starting work on new requirements)

- **Applicable Scenarios**: Not legal yet`{num}-{short-name}`branch with`.aisdlc/specs/...`Table of contents.
- **Skill**:`spec-init`（`skills/spec-init/SKILL.md`)
- **Output**:`{FEATURE_DIR}/requirements/raw.md`(UTF-8 with BOM)
- **Key Note**:
  -`spec-init`Force the original requirement to be passed in as "file path" (to avoid Chinese parameter encoding issues).
  - The script will delete the incoming source files (which need to be backed up first).

#### 5.2 R1: Clarification + Solution Decision (raw → solution)

- **Applicable scenarios**: vague requirements, unstable scope, unclear constraints, and easy to make up.
- **Skill**:`spec-product-clarify`（`skills/spec-product-clarify/SKILL.md`)
- **Output**:`{FEATURE_DIR}/requirements/solution.md`- **Key Disciplines**:
  - ** Clarification not completed, writing prohibited`solution.md`**.
  - Only **1 highest leverage multiple-choice question** will be asked in each round, and "questions/recommendations/answers/conclusions/remaining ambiguities/unclarified points/whether completed" will be written back to`raw.md/## 澄清记录`.
  - Uncertainty prohibits writing the "List of Issues to be Confirmed" and uniformly enters the **Verification List** (Owner/Deadline/Signal/Action).

#### 5.3 R2: PRD (solution → prd, optional)

- **Applicable scenarios**: Delivery specifications need to be frozen, QA needs testable AC, and R&D needs specifications for detachable tasks.
- **Skill**:`spec-product-prd`（`skills/spec-product-prd/SKILL.md`)
- **Enter Access**: must exist`{FEATURE_DIR}/requirements/solution.md`.
- **Output**:`{FEATURE_DIR}/requirements/prd.md`- **Diversion**: If it is a "simple need", it does not necessarily need to be independent`prd.md`, available at`solution.md`After adding Mini-PRD, it enters the subsequent stage.

#### 5.4 R3: prototype (prd → prototype, optional)

- **Applicable scenarios**: There are new/changed interactions, or the interactions are not clear enough, and "text prototype + wireframe" needs to be used to eliminate ambiguity.
- **Skill**:`spec-product-prototype`（`skills/spec-product-prototype/SKILL.md`)
- **Enter Access**: must exist`{FEATURE_DIR}/requirements/prd.md`.
- **Output**:`{FEATURE_DIR}/requirements/prototype.md`- **hard requirements**:
  - Must be **Pure ASCII wireframe**.
  - Must include: task flow (T-xxx), page/pop-up list (P/D/W-xxx), page-by-page description, AC→node mapping, walkthrough script.

#### 5.5 R4: Interactive Demo (prototype → demo, optional)

- **Applicable scenarios**: Higher fidelity walkthroughs are required (usability verification/stakeholder alignment/development and testing understanding consistency verification).
- **Skill**:`spec-product-demo`（`skills/spec-product-demo/SKILL.md`)
- **Enter Access**: must exist`{FEATURE_DIR}/requirements/prototype.md`.
- **Output**: Default`{REPO_ROOT}/demo/prototypes/{CURRENT_BRANCH}/`- **Hard Ban**:
  - When the root directory of the runnable Demo project cannot be found, it is **prohibited** to initialize the new front-end project by itself to pollute the warehouse; it must be stopped and requested`DEMO_PROJECT_ROOT`.
  - **No self-created pages**: Page lists can only come from`prototype.md`.

---

### 7. Design link (D0–D2): Applicable scenarios and skills

#### 6.1 D0 diversion: whether the design can be skipped

In the design link of this repository, "skipping design" is not laziness, but a clear decision:
If skipped, it must be in`implementation/plan.md`Complete the minimum decision-making information and keep it traceable and verifiable.

#### 6.2 D1: Research (optional research)

- **Applicable scenarios**: Key uncertainties/high risk points need to be verified first; multiple options lack evidence to support the choice.
- **Skill**:`spec-design-research`（`skills/spec-design-research/SKILL.md`)
- **Output**:`{FEATURE_DIR}/design/research.md`- **Key Constraints**:
  - Research products do not write implementation specifications (task/field/DDL/script), only conclusions and verification lists that can be referenced by D2.
  - TODO/to-be-confirmed list is prohibited, and unknown items are uniformly entered into the verification list (Owner/deadline/signal/action).

#### 6.3 D2: Decision Doc/RFC (Design Decision Document)

- **Applicable scenarios**: Involves changes in external contracts/permissions/data standards; has a large cross-system impact; requires consensus review and frozen standards.
- **Skill**:`spec-design`（`skills/spec-design/SKILL.md`)
- **Output**:`{FEATURE_DIR}/design/design.md`- **Writing Boundary**: Write "key points of decision-making and external commitments + traceability links", do not write implementation steps and task splits.

---

### 8. Implementing links (I1–I2): Applicable scenarios and skills

#### 7.1 I1: Implementation Plan (plan.md = unique SSOT)

- **Applicable Scenarios**: Any need to enter development execution (must be done).
- **Skill**:`spec-plan`（`skills/spec-plan/SKILL.md`)
- **Output**:`{FEATURE_DIR}/implementation/plan.md`- **Key Requirements**:
  -`plan.md`There must be checkable tasks (`- [ ]/- [x]`), and each task contains: precise file path, executable steps, minimum verification commands and expected signals, submission points and audit information.
  -Uncertainty written in`plan.md/NEEDS CLARIFICATION`, and **block access to I2**.
  - **Commit message must be in Chinese** (it must also be reflected in the plan).

#### 7.2 I2: Execute in batches as planned and write back

- **Applicable scenarios**: Executable`plan.md`, it is necessary to implement it in batches and make checkpoint reports.
- **Skill**:`spec-execute`（`skills/spec-execute/SKILL.md`)
- **Output**:
  - Code and configuration changes
  - **Only Status Writeback**: Only writeback to`{FEATURE_DIR}/implementation/plan.md`(checkbox + commit/pr/changed_files + verification result summary)
- **Key Disciplines**:
  - By default, the first 3 unfinished tasks are executed in each batch, and only reporting and waiting for feedback between batches are performed.
  - Stop immediately on blocked/clarified items (seek clarification, no guesswork to advance).
  - If ADR/contract changes occur during execution: only`{FEATURE_DIR}`drafted within the`plan.md`Record Merge-back pending; I2 does not change directly`project/*`.

#### 7.3 Finish: Development closing confirmation (only verification)

- **Applicable scenario**: The implementation has been completed, and it is necessary to prove "full green" and generate a reproducible completion confirmation report.
- **Skill**:`finishing-development`（`skills/finishing-development/SKILL.md`)
- **Output**: Completion confirmation report (including actual running commands and results).

---

---

### 9. Scenario → Skill Selection Quick Check

#### 9.1 Am I currently working on “requirements” or “project knowledge base”?

- **Deliver a requirement**: Go`using-aisdlc`Navigation Spec Pack (R/D/I/Finish).
  - Skill:`using-aisdlc`（`skills/using-aisdlc/SKILL.md`)
- **Make AI/newcomers stop guessing the entrance**: Go`project-discover`Discover.
  - Skill:`project-discover`（`skills/project-discover/SKILL.md`)

#### 9.2 Typical scene table

| Typical scenarios | Recommended skill links | The core products you want to get |
|---|---|---|
| New requirements have just arrived and there are no branches/directories |`spec-init` → `spec-context` | `requirements/raw.md`+ Targetable`FEATURE_DIR`|
| The needs are vague, controversial, and easy to figure out |`spec-context` → `spec-product-clarify` | `solution.md`(Including verification checklist)+`raw.md/澄清记录`|
| Need to freeze specifications for review/R&D teardown/QA use cases |`spec-context` → `spec-product-prd` | `prd.md`(Scenario + AC testable) |
| The interaction is ambiguous and requires text prototype alignment |`spec-context` → `spec-product-prototype` | `prototype.md`(ASCII wireframe + AC mapping + walkthrough script) |
| Stakeholders can click and run to check if needed |`spec-context` → `spec-product-demo`| Demo (strictly according to the prototype page list) |
| RFC decision document required/involving changes in external commitments |`spec-context` → `spec-design`(As needed first`spec-design-research`） | `design/design.md`(Decision and Verification Checklist) |
| To enter development execution, but there is no executable plan |`spec-context` → `spec-plan` | `implementation/plan.md`(SSOT ONLY) |
| Implement as planned and require audits and checkpoints |`spec-context` → `spec-execute`| Code changes +`plan.md`Writeback (sole status source) |
| Development completed, “full green” certification required |`finishing-development`| Completion confirmation report (command + results can be reproduced) |
| Existing projects: entrance/boundary/contract is always guessing |`project-discover`(Segmented by sub-skills) |`.aisdlc/project/*`(memory+index+module page+ops+DoD) |

---

### 10. Training drill (it is recommended to run through it in two hours)

#### 10.1 Exercise A: Stock project Discover (minimum available delivery, recommended to be done first)

Goal: First deliver a "consumable project-level knowledge base MVP": memory + components index + 1–3 P0 module pages (including contract paragraphs and evidence chains).

-`project-discover-preflight-scope`
- `project-discover-memory-index`
- `project-discover-modules-contracts`(Select 1–3 P0 modules)
-`project-discover-products-ops-dod`(Only do necessary convergence with DoD)

#### 10.2 Exercise B: Shortest closed loop (simple requirement)

Goal: Let students experience the rhythm of “one node, one product”, and`plan.md`As the only way SSOT is performed.

- R0：`spec-init`generate`raw.md`- Access control:`spec-context`Encyclopedia`FEATURE_DIR=...`
- R1：`spec-product-clarify`(Required: Clarification Record Writeback + Output`solution.md`）
- I1：`spec-plan`(The task list is executable and contains minimal verification commands)
-I2:`spec-execute`(Execute in batches, write back audit to`plan.md`）
- Finish：`finishing-development`(Output completion confirmation report)

#### 10.3 Exercise C: Complex interaction requirements (R2+R3+R4)

Goal: Experience the closed-loop and backflow mechanism of "PRD (testable) → prototype (available for review) → Demo (clickable and runable)".

- R2:`spec-product-prd`(AC testable)
- R3:`spec-product-prototype`(ASCII wireframe + AC→node mapping + walkthrough script)
- R4:`spec-product-demo`(Generated strictly according to prototype page list)
- Found problems: reflow updates according to rules`solution/prd/prototype`(Instead of free play in the demo)

---

### 11. Common red flags (if any of them appear: correct the error on the spot)

#### 11.1 Discover Common Red Flags

- Writing details (invariants/fields/processes/to-be-filled) in the index leads to double writing and drift.
- Appear`.aisdlc/project/contracts/**`(Breaking hard rules).
- The text of the module page uses "to be filled/not found" placeholder instead of writing`Evidence Gaps`.
- The P0 module is checked in the index, but the module page is not up to standard (missing fixed title, missing authoritative entry/invariant/evidence entry, missing frontmatter metadata).

#### 11.2 Spec Pack Common Red Flags

- Didn't run`spec-context`Just start reading and writing`requirements/*` / `design/*` / `implementation/*`.
- The user verbally gives the path/branch, and you skip the gate and "believe it and keep writing".
- R1 Write before clarification is completed`solution.md`.
- Accept uncertainty with the "Open Questions/TODO" list (should be changed to verification list: Owner/Deadline/Signal/Action).
- No`implementation/plan.md`(or the plan is not executable) and start writing code directly.
- Execution status is written to chat/issue/another file instead of writing back`plan.md`(Breaking SSOT).

---

### 12. Appendix: Skills List (sorted by process)

#### 12.1 Discover (project-level knowledge base)

-`project-discover`:Discover master control (hard rule: none`contracts/**`, index navigation only, module page single page SSOT, Evidence Gaps).
-`project-discover-preflight-scope`: Evidence entry inventory + P0/P1/P2 stop loss.
-`project-discover-memory-index`:memory North Star + index skeleton (map layer).
-`project-discover-modules-contracts`: Module page + Contract paragraph + Evidence chain.
-`project-discover-products-ops-dod`: Products Convergence + Ops Portal + DoD Access Control + Delta Discover/stale.

#### 12.2 Spec Pack Navigation and Access Control

-`using-aisdlc`: Process navigation + general access control ("Next step selection skills" of R0–R4 and I1–Finish).
-`spec-context`: unique contextual positioning (`FEATURE_DIR`), it will stop if it fails.
-`spec-init`:Create new Spec Pack (branch+directory+`raw.md`, UTF-8 with BOM).

#### 12.3 Demand side (R1–R4)

-`spec-product-clarify`: Clarification loop +`solution.md`(Clarification prohibits writing before completion`solution.md`）。
- `spec-product-prd`：`solution.md` → `prd.md`(Deliverable/Acceptable/Testable).
-`spec-product-prototype`：`prd.md` → `prototype.md`(ASCII prototype + AC map + walkthrough script).
-`spec-product-demo`：`prototype.md`→ Demo (must find the root directory to run the Demo; self-created pages/projects are prohibited).

#### 12.4 Design side (D1–D2)

-`spec-design-research`: Optional research, output`design/research.md`(Conclusion + Verification Checklist).
-`spec-design`:output`design/design.md`(Decision document/RFC, write decisions but not implementation).

#### 12.5 Implementation side (I1–I2) and closing

-`spec-plan`:output`implementation/plan.md`(Only execution list with status SSOT).
-`spec-execute`:according to`plan.md`Execute in batches and write back the audit (status is only written back`plan.md`）。
- `finishing-development`: Closing confirmation (only verification, all green is considered complete).

#### 12.6 Parallelism and collaboration (optional meals)

-`dispatching-parallel-agents`: 2+ Dispatch methods for parallel processing of independent problem domains.
-`subagent-driven-development`:according to`plan.md`Each task is dispatched with sub-agents and reviewed in two stages.
-`spec-requesting-code-review` / `spec-receiving-code-review`: Code review requests and receipts (emphasis on technical verification, avoidance of performative consent).