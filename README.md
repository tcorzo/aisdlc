---
markdown-sharing:
  uri: 9ad9e4f3-f0ac-40f2-ad7d-e4676a39dafe
---
#AI SDLC tool introduction

This tool provides a set of **Spec-level** workflows and skill sets, centered around **dual-layer SSOT (project-level SSOT + requirement-level Spec Pack)**, **Spec as Code**, and **progressive disclosure**, to advance a requirement from "original input" to "reviewable decision-making (optional)" and "directly executable implementation plan + batch execution".

---

## Install/Update```

# powershell
npx skills add https://github.com/zixun-github/aisdlc --skill * --agent claude-code cursor --yes --copy --global

# bash
npx skills add https://github.com/zixun-github/aisdlc --skill '*' --agent claude-code cursor --yes --copy --global

```## Create project-level index library```
/project-discover
```## Requirements Development```
# 开始新的需求或BUG修复(会自动创建开发分支)
/spec-init 输入新的需求内容...（自动进行澄清）
# 创建执行计划
/spec-plan 
# 执行计划
/spec-execute
# 测试验证（可选）
/spec-test
```---
## Small requirements (lightweight) Spec Pack: shortest closed-loop steps (recommended)

Suitable for requirements with **small scope, controllable impact, and no obvious interaction uncertainty** (for example: small fixes, small enhancements, script/configuration adjustments, one-time migration). The goal is **minimum placement + traceability + executability** to avoid turning small requirements into "heavy processes".

- **CHECKLIST OF STEPS (ZERO TO DONE)**
  - **R0: Initialization**:`spec-init`→ Generate branches and Spec Pack, and release them to disk`raw.md`- **R1: Minimal clarification**:`spec-product-clarify`→ Streamline output`solution.md`(Write clear boundaries and acceptance)
    - If the requirements are already clear: it is also recommended to complete them in a minimalist way`solution.md`, ensuring there is an anchor point for subsequent review and review
  - **I1: Implementation Plan**:`spec-plan`→ output`implementation/plan.md`- **I2: Execution in batches**:`spec-execute`→ Press`plan.md`Implement in batches with minimal verification and write back audit information
---

## Quick overview of steps (purpose & output)

> The following steps are organized according to "shortest path first, expand on demand": R0-R4 are used for clarification and product-side products; D0-D2 are the design phase (can be skipped entirely); I1-I2 are the implementation phase (must be done); V1-V4 are the verification phase (on-demand).

- **R0:`spec-init`(Initialize new requirements)**
  - **Purpose**: Create a Spec workspace (branch + Spec Pack directory), and record the original requirements as traceable input
  - **Output**: new branch`{num}-{short-name}` + `.aisdlc/specs/{branch}/...` + `requirements/raw.md`

- **R1：`spec-product-clarify`(clarification + program decision)**
  - **Use**: put`raw.md`The fuzzy requirements are converged into reviewable recommended solutions, and 2–3 alternatives and verification lists are given
  - **Output**:`requirements/solution.md`

- **R2：`spec-product-prd`(Optional: PRD/delivery specifications)**
  - **Purpose**: Convert R1 decisions into deliverable, acceptable, and testable specifications (scope/scenario/AC/risk and dependency)
  - **Output**:`requirements/prd.md`

- **R3：`spec-product-prototype`(optional: prototype description)**
  - **Purpose**: When there is new/changed interaction or the interaction is not clear enough, use task flow + page structure + status description to eliminate understanding deviations
  - **Output**:`requirements/prototype.md`

- **R4：`spec-product-demo`(Optional: Interactive Demo)**
  - **Use**: put`prototype.md`The page list and interaction instructions are implemented into a runnable demo for walkthrough/verification/alignment and support reflow
  - **Output**: Demo project directory (default`demo/prototypes/{CURRENT_BRANCH}/`)

- **D0–D2: Design phase (whole can be skipped)**
  - **D0 (diversion)**: Determine whether to skip design; if skipped, implementation`plan.md`Minimum decision information (objectives/boundaries/constraints/acceptance/verification checklist) must be completed
  - **D1：`spec-design-research`(optional research)**
    - **Output**:`design/research.md`
  - **D2：`spec-design`(RFC/Decision Doc; required if not skipped)**
    - **Output**:`design/design.md`- **I1–I2: Implementation phase (required)**
  - **I1：`spec-plan`(Implementation Plan/SSOT)**
    - **Output**:`implementation/plan.md`(Only execution list and status SSOT)
  - **I2:`spec-execute`(Batch execution + write-back audit)**
    - **Output**: Code and configuration changes; and task status/audit information **only written back** to`implementation/plan.md`

- **`spec-test`(Verification phase, on demand)**
  - **Purpose**: Generation and placement of test plans, use cases, suites, reports and defects
  - **Output**:`verification/*`Related products
  - **Sub-skills**:`spec-test-plan`(Test Plan) →`spec-test-usecase`(use case) →`spec-test-suites`(Kit, optional) →`spec-test-execute`(Report);`spec-test-bug`(Defect report, insertable)

- **Shortcuts**
  - Not sure what to choose next:`using-aisdlc`, automatically interpret the progress of the spec pack and the next step.

---

## Spec Pack (what will you end up placing)

- **Branch (Context Anchor)**:`{num}-{short-name}`- **Root Directory (Requirement Level SSOT)**:`.aisdlc/specs/{num}-{short-name}/`- **Commonly used products (progressively generated in stages)**
  - **Clarify/requirements/**
    -`requirements/raw.md`: Original input (evidence entry)
    -`requirements/solution.md`: Clarification + Solution Decision (Demand Side SSOT)
    -`requirements/prd.md`: (optional) delivery specification (fine AC/scope/dependency)
    -`requirements/prototype.md`: (optional) prototype description (task flow/page/state/AC mapping)
  - **Design / design/** (the whole can be skipped; when not skipped`design.md`for SSOT)
    -`design/research.md`: (optional) Research conclusion (risk/assumption → verification checklist)
    -`design/design.md`: (Optional) Decision document/RFC (SSOT in the design phase, writing decisions but not implementation)
  - **Implementation/implementation/**
    -`implementation/plan.md`: Implementation plan (I1 must do; **Unique execution list and status SSOT**, including task checkbox, steps, minimum verification, submission point and audit information)
  - **Verification / verification/** (on demand)
    -`verification/test-plan.md`: Test Plan (V1; Scope/Strategy/Environment/Access and Access)
    -`verification/usecase.md`: Test case (V2; AC traceable)
    -`verification/suites.md`: (optional) test suite (V3; smoke/regression/targeted)
    -`verification/report-{date}-{version}.md`:Test Report (V4; Conclusion + Defect Reference)

---

## Project contains multiple Git repository working methods

- Create a new project root repository project_root
- Use git submodule to add each sub-repository to project_root, the command is`git submodule add <repo-url> [<path>]`When the project uses`git submodule`(exist`.gitmodules`), the Spec Pack process will adapt to multi-warehouse collaboration in the following ways:

- **Spec Pack is always in the root project**: requirements/design/implementation documents are unified in the root project`.aisdlc/specs/{branch}/`, the sub-repository is only used as a code workspace and does not host Spec documents.
- **spec-init**: Only initialize the Spec branch of the root project; sub-warehouse branches are processed by subsequent I1/I2 access control.
- **spec-context**: will additionally expose the submodule status snapshot (branch/HEAD/dirty workspace) for verification during the implementation phase.
- **I1(spec-plan)**: in`plan.md`Declare the "sub-warehouse scope" and "code workspace list" (path, whether it is affected, whether it is required, and desired branches); task audits are recorded according to repo.
- **I2 (spec-execute)**: The affected items must be verified before execution`required`Whether the sub-repository has been cut to the Spec branch with the same name as the root project (such as`001-xxx`); if not satisfied, block and report. Press repo to write back after execution`branch/commit/pr/changed_files`, do not compress the long position results into single positions.
- **spec-merge-back**: When promoting assets, it is necessary to distinguish whether the evidence comes from the root project or the sub-warehouse path.

**Brief process**:`spec-init`(Nekura) → Clarification/Design →`spec-plan`(Declare sub-repository) → Manually or script to cut the sub-repository to the branch with the same name →`spec-execute`(verification + audit by repo).

---

## Use best practices

Recommended practices for users of this tool to reduce context drift, rework, and non-traceability issues:

- **Project level first, then demand level**: It is recommended to use it before large-scale use by the team`project-discover`Establish`.aisdlc/project/`Knowledge base (at least memory + 1–3 P0 module pages), and then running Spec Pack can reduce`CONTEXT GAP`Analyze drift with the impact.
- **Use using-aisdlc when you are not sure about the next step**: Let the Router automatically determine the next skill based on the current product and intention to avoid manually selecting the wrong stage.
- **important! ** Prioritize the use of skills at all times, especially during the execution phase, if there are any adjustments to the plan and code, the spec-plan skill will be used first to ensure the consistency of spec pack information.
---