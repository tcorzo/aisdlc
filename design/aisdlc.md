---
markdown-sharing:
  uri: 7ac73b2a-67cd-46a2-866c-93cc56503720
---
# AI SDLC project knowledge base (project-level SSOT + requirements execution Spec Pack + progressive disclosure) solution

This document defines an **AI project knowledge base** for the entire SDLC process: using **project-level SSOT** as a long-term, stable single source of truth (SSOT), and supporting **AI Progressive Disclosure (Progressive Disclosure)**, allowing agents at each stage to "see the map first, and then obtain evidence on demand."
At the same time, each requirement has an independent **Requirement-level Spec Pack (SSOT)**, which is used for specification precipitation, evidence retention and traceable delivery during the execution of the requirement; **Requirement-level Spec Pack is not used as an information source for progressive disclosure of the AI ​​knowledge base**. After the requirement is completed, reusable information will be merged back into project-level assets through Merge-back, and the remaining content will be archived and saved for audit and review.

---

## Project background

The company is promoting a new R&D paradigm upgrade**. The core direction is to engineer and standardize the "knowledge organization method" and "R&D process methodology", and achieve stable efficiency improvement and continuous evolution through AI. This project is an important part of the upgrade and mainly undertakes two types of construction goals:

- **Establish an AI SDLC project knowledge base**: Center around the project-level SSOT and index system to form sustainably maintained knowledge assets to support the effective organization, retrieval, citation and tracing of information, and reduce communication costs and rework risks caused by information dispersion and context loss.
- **Establish SOPs for each node and use AI to assist efficiency improvement at each stage**: Solidify the process of "what to read/what to write/how to accept" at each stage into workflows and templates, and combine best practices with mechanisms such as SKILL to precipitate reusable tools and automation capabilities, making delivery quality, efficiency and consistency measurable, replicable and iterable.

---

## Core concept: project-level SSOT + demand-level Spec Pack

### SSOT (Single Source of Truth) principle

- **Project-level SSOT (Project Spec Set)**: The long-term source of truth in the project dimension, including product business information, module information, code structure, etc. Ensure that documents and code evolve simultaneously through version control and code review to avoid document obsolescence.
  - **Long life cycle, strong governance** (centered on assets and operations): Form long-term knowledge assets of the project through continuous updates and version management
  - Includes: Roadmap, architecture, external contract, data caliber, operation manual, NFR budget, risk list, etc.

- **Requirement-level SSOT (Spec Pack)**: Each requirement has its own "Spec Pack", covering the closed-loop products and evidence of the requirement from PRD to release, **only takes effect during the execution of the requirement**.
  - **Short life cycle, strong timeliness** (delivery-centered): closed loop around delivery, documents evolve together with the code, avoiding the disconnect between documentation and implementation
  - **Not used as a progressive disclosure information source**: Does not participate in cross-requirement knowledge accumulation; cross-requirement reusable information must be merged to the project level through Merge-back
  - After the requirements are completed, the reusable assets are "promoted" from the requirements layer to the project layer according to the rules; the rest are archived and retained as delivery evidence, and the complete evolution history is recorded through version control

### Spec as Code Concept

Treat and maintain Spec documents like project code, and follow engineering practices such as version control, code review, and continuous updates.

### SOP: Use "workflow + template" to turn best practices into AI

Use workflow to define "what to read/write/how to accept each step", and use templates to solidify "how to write", making best practices the default path.

- **Workflow**: step arrangement of input/output/access control/evidence (machine readable)
- **Template**: fixed skeleton of atomic Spec (Frontmatter + text minimum closed loop)
- **Gates**: DoR/DoD, complete structure, complete references/traceability, contract/test/release verification

### Orchestration layer (Router) and execution layer (Worker Skills)

In the Spec Pack scenario, two types of abilities must be distinguished to avoid "each skill independently determines the next step" causing the distribution caliber to be scattered and fight with each other:

- **Arrangement Layer (Router)**: Only responsible for "next step judgment/diversion" and output the only next step instruction.  
  - This warehouse is based on`skills/using-aisdlc/SKILL.md`As the **only router** for the Spec Pack process.
- **Execution layer (Worker Skills)**: only responsible for access control + product placement + DoD self-inspection at this stage, **not making next diversion decisions**.  
  - After any worker skill is completed, return to`using-aisdlc`Reroute; if you find "this step should not be entered", stop and prompt to return`using-aisdlc`Correct routing rather than rewriting processes within skills.

**Landing location (catalogue agreement)**:

-`.aisdlc/workflows/`: Workflow definition (YAML/JSON)
-`templates/`:Template (Markdown)

**Minimum execution closed loop**: Generate template → Complete key information → Self-check access control → Review (ADR if necessary) → Write back to the library/merge-back

---

## Goals and Principles

- **Double-tier SSOT**: project-level long-term assets + demand-level delivery closed loop to ensure information consistency and traceability
- **Progressive Disclosure**: Agent only loads **project-level** global specifications and indexes (maps) by default; when the task clearly points to a requirement, it only reads the minimum necessary atomic Spec file in the Spec Pack of the requirement (the requirement level is not used as a global disclosure information source)
- **Traceability**: Spec ↔ Code ↔ Test ↔ Release/Operation and Maintenance documents are linked to each other through IDs and references
- **Machine readable first**: Markdown + YAML Frontmatter + Mermaid + OpenAPI/SQL/JSON Schema and other structured fragments to reduce ambiguity

---

## 6 stages of Spec (top-level planning: only define core output)

> Description:
> - The "phase" here refers to the closed-loop execution phase of the **Requirement-level Spec Pack** (**excluding** the daily governance of project-level long-term assets).
> - Only "**core output**" is defined at each stage to avoid writing detailed SOPs in top-level planning; SOPs/access control are completed by special documents at each stage.

| Phase | Core Goal | Core Output (Spec Pack Product) |
|---|---|---|
| 1. Requirements clarification (clarify) | Clarify "what to do/why to do/what the current situation is/how to do it" |`requirements/raw.md`(original demand) +`requirements/solution.md`(Core plan: goal/scope/process/acceptance criteria/risk) |
| 2. Requirements decision-making (design) | Produce a decision document (Decision Doc/RFC) for human review consensus as the authoritative input of the execution plan (SSOT) |`design/design.md`(Problem definition, solution options/tradeoffs, architecture diagram, data/interface points) + (on demand)`design/research.md`, Contract/Data Model, ADR Entry |
| 3. Demand execution (implementation) | Produce an execution plan (Execution Plan / Prompt Context) that can be directly fed to AI and complete changes |`implementation/plan.md`(Scope/Milestones/Risk/Acceptance) +`implementation/tasks.md`(File path, scaffolding, test points, verification steps) + Code changes and traceability links (Spec ↔ PR/Submit) |
| 4. Requirements testing (verification) | Verify that functions and non-functions meet the acceptance criteria |`verification/plan.md`(Testing Strategy/Scope) + Use Cases/Regression Sets +`verification/report.md`(Test Report and Conclusion) |
| 5. Release | Controllable rollout, observable operation, and rollback |`release/plan.md`(Release plan) +`release/runbook.md`(Operation manual)＋`release/monitoring.md`(monitoring alarm) +`release/rollback.md`(Rollback scenario) |
| 6. Merge-back | Promote "reusable assets" back to project-level SSOT, and archive the rest to retain certificates |`merge_back.md`(List and evidence): Whether ADR/contract/operation and maintenance assets/NFR baseline, etc. have been synchronized`project/`;and update Registry status |

> Two-tier document strategy:`design/`Corresponds to **Layer 1 (Decision Doc/RFC)**;`implementation/`Corresponds to **Layer 2 (Requirement Execution/Execution Plan/Prompt Context)**.  
> For requirements with clear boundaries, low risks, and no critical uncertainties, **Layer 1 is optional**: you can skip "requirements decision-making (design)" and go directly to "requirements implementation (implementation)". But when entering execution,`implementation/plan.md`The minimum decision-making information (goals, scope and boundaries, key constraints, acceptance criteria, and items to be confirmed) must be completed, and brainstorming is not allowed.

---

## Two-tier SSOT directory structure (Progressive Disclosure is based on project level)

Core layering: **Project-level Memory (Constitution) → Project-level Index/Map Layer (entrance) → (On-demand) Requirement-level Spec Pack (SSOT) → Deliverables Layer (Code/Testing/Operation and Maintenance)**.

### Directory structure (can be implemented directly)```text
.aisdlc
  project                          # 项目级 SSOT（长期资产）
    memory                         # 项目级 Memory（链接文件，提供全局上下文）
      product.md                   # 业务信息
      tech.md                      # 技术信息
      structure.md                 # 项目结构
      glossary.md                  # 术语表
    adr                            # 架构决策记录
      index.md
      0001-xxx.md
      ...
    products                       # 业务架构层（Business Architecture，可选）：业务域/业务模块资产（索引 + 模块文件）
      index.md
      a.md
      ...
    components                     # 应用架构层（Application Architecture，可选）：承载业务能力的应用组件资产（索引 + 模块文件）
      index.md                     # 应用组件地图（索引 + 跨模块依赖关系图）
      a.md
      ...
  specs                          # 需求级 SSOT（交付闭环）
    001-demo                      # 需求 ID（格式：{num}-{domain-name}，num 为三位数字编号）
      merge_back.md                # Merge-back 执行时生成
      requirements                 # 需求澄清（clarify）阶段（原始需求/方案/PRD等）
        raw.md                     # 原始需求（用户/业务输入）
        solution.md                # 解决方案（澄清后的核心产出：目标/范围/流程/验收口径/风险）
        prd.md                     # 产品需求文档（可选）
      design                       # 需求决策阶段（Decision Doc / RFC）
        research.md                # 调研、竞品分析
        design.md                  # 决策文档（问题定义/方案选项/权衡/架构图、ADR 入口）
      implementation               # 需求执行阶段（Execution Plan / Prompt Context）
        plan.md                    # 实现计划
        tasks.md                   # 任务分解
      verification                 # 测试验证阶段
        test-plan.md               # 测试计划
        usecase.md                 # 测试用例
        report.md                  # 测试报告
      release                      # 发布运维阶段
        plan.md                    # 发布计划
        runbook.md                 # 运行手册
        monitoring.md              # 监控告警
        rollback.md                # 回滚方案
        postmortem.md              # 复盘报告
        ...
    002-demo
      ...
```> Description:
> -`project/products/`"Business domain/business module" assets used in **Business Architecture layer** to express business boundaries, business capabilities, value streams/core scenarios, participants/roles, business processes, business services, business objects and events, business rules and calibers, business indicators and dependencies, etc. (emphasis on business semantics, not technical implementation).
> -`project/components/`"Application component" assets used in the **Application Architecture layer** to express application component boundaries, application services/interfaces, component collaboration and data object responsibilities, etc. (emphasis on application layer commitment and collaboration boundaries, without writing specific implementation details).
> - **Contract organization mode (default)**: not maintained separately`project/contracts/**`;The **API/Data contract** of the module is unified and merged into`project/components/{module}.md`Fixed paragraph within:`## API Contract` / `## Data Contract`, and link to the authoritative evidence in the repository (OpenAPI/Proto/Schema/DDL/Migration/ORM, etc.) in the paragraph.
> - Technology infrastructure/platform capabilities (Technology Layer, such as cache, message queue, gateway, middleware) **not recommended** to be mixed in`project/components/`;If the project requires, you can create a new`project/platform/`or`project/tech/`Carrying corresponding assets (implemented on demand).

---

Note: The templates for the above files are placed in the directory templates

## Business architecture: Use enterprise architecture knowledge to describe business areas and modules (project-level long-term assets)

> Goal: Make the description of "business modules" as clear as "application components", thereby stably anchoring requirements, solutions and implementation on business semantics (and supporting cross-requirement reuse and governance).

### Business module (`project/products/`) what should be written

Use common expressions of enterprise architecture (business architecture) to write business modules as manageable and reusable long-term assets (it is recommended to at least cover them):

- **Business Boundary (In/Out)**: What this module is responsible for, what it is not responsible for, and how to cut the boundaries with adjacent modules (how to adjudicate conflicts: Contract/ADR/Caliber).
- **Business capability (Capability)**: The list of capabilities carried by the module (P0/P1/P2). The capabilities are defined by the business expression of "input→process→output".
- **Value Stream/Scenario**: The end-to-end business value link from trigger to result, helping to align demand placement with business results.
- **Actor/Role**: Who triggers/consumes the module capabilities in business, and responsibility boundaries (optional RACI).
- **Business Process**: key processes and their triggers, results, and owners; preferably expressed in diagrams (such as PlantUML).
- **Business Service**: role-oriented stable business commitment (input/output/preconditions/business constraints).
- **Information Object/Event (Business Object/Event)**: core business objects (life cycle, primary key/unique identification, key stable attributes) and business event semantics.
- **Policy/Business Rules**: triggers, conditions, actions, exceptions, calibers/data references and compliance sources (implementation details sink to the requirement level).
- **Business caliber and indicators (KPI/metric)**: Business definition and caliber entry of key indicators (pointing to data contract/dictionary), used for "observable business results".
- **Business dependency and integration (upstream and downstream)**: reasons for business dependence, interaction methods, business risks and mitigation measures.

### Mapping relationship between business modules and application components (recommended)

- **Business → Application **: The business module expresses "what to do/why to do/the business boundary", and the application component expresses "how to carry the application layer commitment and collaboration boundary of this business capability".
- **Capability/Process/Object Alignment**: Recommended in`project/products/*.md`and`project/components/*.md`Use the same Capability/Process/Object number for cross-reference to form a stable traceability (for example`CAP-001`、`BP-001`、`BO-001`).

### How does the demand-level Spec Pack fall into the business module?

- required`specs/<DEMAND-ID>/requirements/`and`design/`The corresponding business module should be referenced (`project/products/*.md`) to avoid repeatedly defining long-term stable business semantics at the requirement level.
- When a requirement introduces "new long-term business capabilities/rules/calibre", it should be promoted and updated to`project/products/`, and record the reason for the change and the associated ADR/Spec.

---

## Application architecture: Use enterprise architecture knowledge to describe application components and application services (project-level long-term assets)

> Goal: Write "application components" into manageable and reusable long-term assets, clearly expressing the application layer's stable commitment to the business, component collaboration boundaries, external interfaces and data object responsibilities; at the same time, strictly avoid mixing one-time implementation details (classes/functions/code structures) into project-level assets.

### Application components (`project/components/`) what should be written

According to common expressions of enterprise architecture (application architecture, ArchiMate Application Layer), it is recommended to cover at least:

- **TL;DR (decision-level summary, 3-5 sentences, required)**: What does the module do, what are the boundaries, and what are the key invariants - let AI use the summary to determine whether it needs to go deeper during the "map browsing" stage, reducing the consumption of invalid tokens.
- **Component positioning (In/Out + Boundary)**: What application capabilities/commitments the component provides and what it is not responsible for; how to cut the boundaries with adjacent components (based on contract/ADR).
- **Bearing business mapping**: Which business modules this component carries (`project/products/*.md`), which business capabilities/processes/objects (CAP/BP/BO numbers), and which consumers (people/systems/other components).
- **Change Frequency**: The change frequency (high/medium/low) based on git log statistics allows AI to predict which modules are more likely to be affected and require careful design during the demand analysis stage. Record in frontmatter`change_frequency: high|medium|low`and`last_verified_at: <date>`.
- **Application Service Catalog**: Stable "application layer service commitment", describing input/output, preconditions/constraints (business/compliance), SLA/SLO/NFR key points (do not write implementation).
- **Application Interface and Contract Entry (Application Interface)**:
  - API: The authoritative entrance is written in`project/components/{module}.md#api-contract`, and link to the OpenAPI/Proto product/source file and build command (or CI job) in the warehouse
  - Event/Message: business semantics and contract entry of topic/event (if applicable)
  - UI/Batch: Entry and constraints (if applicable)
- **Key collaboration relationships (Interaction/Collaboration)**: Pick 1-2 representative scenarios to illustrate the cross-component call chain/collaboration relationships and key boundaries (detailed timing down to the requirement level).
- **Data Object & Ownership**: Which data objects (Owner/main writer/read-only), primary key/unique identifier and life cycle summary the component is responsible for; the authoritative entry is written in`project/components/{module}.md#data-contract`, and link to Schema/DDL/migration/ORM and other evidence in the warehouse.
- **Key state machines and domain events (State Machines & Domain Events)**: The key state machines (enum/status fields + state transition logic) and domain events (event publish/subscribe) identified from the code are precipitated into a summary - this is the most commonly "guessed" part in the requirements analysis phase.
- **Non-Functional Requirements Allocation (NFR Allocation)**: The allocation and boundaries of "guardrails/budgets" such as performance, availability, security compliance, cost, etc. at the component layer; operational operation details point to`project/ops/`.
- **Integration and dependencies (upstream and downstream lists)**: dependency reasons, interaction methods, risks and mitigation measures (technical implementation details are not written here).
- **Run Entrance (Lightweight)**: Entry links for monitoring/alarm, runbook, rollback, etc. (no repeated steps).

### The boundary between application architecture and business architecture/technical architecture (recommendation)

- **Business Architecture**: Answer "What to do/Why to do/Business boundaries and semantics" (capabilities, processes, objects, rules, calibers, KPIs).
- **Application Architecture (Application)**: Answer "Which application components carry business capabilities, and what stable application services/interfaces and collaboration boundaries are provided externally" (components, services, interfaces, data object responsibilities, collaboration relationships, NFR allocation).
- **Technology/Platform**: Answer "Which infrastructure/platform capabilities are used to support application operation" (gateway, messaging, caching, observability, security, release, etc.), in principle, no mixing`project/components/`.

### How does the demand-level Spec Pack fall into application components?

- required`specs/<DEMAND-ID>/design/`Should **reference** the corresponding application component (`project/components/*.md`) in the application service/interface/data object number and contract entry to avoid repeatedly defining long-term stable application layer commitments at the demand level.
- The requirement level should carry details "born for delivery": detailed timing, error codes, field-level constraints, migration scripts, specific implementation plans, etc.; among them, reusable interfaces/data contracts and key ADRs must be merge-backed`project/components/`(contract paragraph) and`project/adr/`.
- When requirements introduce "new long-term application services/interface contracts/data object responsibility boundaries", they should be promoted and updated to`project/components/`, and record the reason for the change and the associated ADR/Spec.

### Multi-level structure description

**Project-level Memory(`project/memory/`)**:
- Project snapshot, including product business information, module information, code structure, etc.
- Stable assets linked to project-level SSOT (`project/adr/`、`project/components/`、`project/ops/`etc.)
- Each time the Agent performs a task, it should be loaded first to provide global context.

**Demand Level Memory (`specs/<DEMAND-ID>/index.md`)**:
- A contextual summary of current requirements and relevant references
- On-demand loading, only used when handling specific needs
- Contains project-level asset references related to the requirement to avoid repeated loading
 - Progressively disclosed information sources that do not enter the project-level knowledge base (if they need to be precipitated into general knowledge, they must be merged back to`project/`)

> **Requirement number naming rules**:`<DEMAND-ID>`The format is`{num}-{domain-name}`,in`num`is a three-digit number (e.g.`001`、`002`），`domain-name`is the name of the requirement field (e.g.`demo`、`user-auth`). Example:`001-demo`、`002-user-auth`.

### Information layered reading order (Agent’s default strategy)

1. **Required Reading (Project Level Global Context)**:
   -`project/memory/product.md`(Business information)
   -`project/memory/tech.md`(technical information)
   -`project/memory/structure.md`(project structure)
   -`project/memory/glossary.md`(Glossary)
   -`project/index.md`(Spec Registry, understand the global status of the project)

2. **Entrance (map layer)**:
   -`project/index.md`(Spec Registry, requirement list and status)
   -`project/products/index.md`(Business architecture index: business domain/business module map, optional)
   -`project/components/index.md`(Application architecture index: application component map, optional)
   - Contract entrance: Pass`project/components/index.md`jump to`project/components/{module}.md#api-contract` / `#data-contract`
   - `project/adr/index.md`(Architectural Decision Index)

3. **Impact analysis (requirement placement point, automatically executed after R1 is completed)**:
   - Based on`requirements/solution.md`target/scope, from`products/index.md`and`components/index.md`Match affected modules
   - Extract TL;DR summary, API/Data invariants, relevant ADRs of affected modules
   - Output impact report writing`specs/<DEMAND-ID>/requirements/solution.md#impact-analysis`- Use this as constraint input in subsequent D2/I1/I2 stages to avoid missing key dependencies and invariants

4. **On demand (demand level Spec Pack)**:
   - Only when the task clearly points to a requirement, read the corresponding requirement`specs/<DEMAND-ID>/index.md`- Then read the specific documents in the requirement Spec Pack as needed (requirements/, design/, implementation/, verification/, release/, etc.)
   - Do not include other requirements`specs/`Content is used as a universal knowledge source; content that needs to be reused across requirements must be Merge-back to`project/`5. **Write back (output into the database)**:
   - Requirement level output: write the corresponding requirements`specs/<DEMAND-ID>/`Directory
   - Project-level update: Promote reusable assets to`project/`Directory

---

## Knowledge consumption mechanism: Let the project knowledge base become the "standard input" of AI workflow

> Goal: Open the closed loop of "knowledge production → knowledge consumption → knowledge evolution". The value of the project knowledge base does not lie in the document itself, but in the fact that the AI ​​Agent at each requirement stage can stably obtain the minimum necessary context required to make decisions.

### Context Injection Protocol

**Problem**: The current progressive disclosure relies on "Agent actively reading according to rules". In practice, Agent often forgets to read, does not use it after reading, or does not know what to read.

**Mechanism**: Define "context slices that must be injected" for each Spec stage - instead of letting the Agent decide what to read, the workflow automatically assembles the context based on the modules involved in the requirement before starting the Agent.

| Spec phase | Project-level context that must be injected | Injection purpose |
|---|---|---|
| R1 Requirements Clarification |`memory/product.md` + `products/index.md`(if any) + TL;DR summary of modules involved | Avoid asking "the project already has an answer" question; align business boundaries and terminology |
| D0 diversion determination | Same as above + Summary of API/Data invariants of modules involved | Accurately determine whether changes in external commitments are involved |
| D2 design decisions | involving modules`components/{module}.md`Full content +`adr/index.md`+ Related ADR | Design must explicitly declare relationship to existing contracts |
| I1 implementation plan | API/Data contract paragraphs involving modules + Evidence entry + cross-module dependencies | Implementation plan must comply with existing invariants |

**Injection method (recommended, can be implemented gradually)**:

1. **Minimum Available (Current)**: In the access control of Skill at each stage, upgrade "Read project-level context" from "On demand/if exists" to **Required**. When the read fails or does not exist, it is explicitly marked as`CONTEXT GAP`(Instead of silently skipping).
2. **Advanced (recommended)**: in`spec-context`Add to output`RELATED_MODULES`Field (based on keyword matching in the requirement description`components/index.md`), automatically generate a recommended reading list to write`specs/{id}/index.md`.
3. **Forward**: Provide structured query capabilities (such as CLI:`aisdlc query --module=auth --aspect=api-contract`), return the target paragraph on demand, reducing the waste of tokens in full-text reading.

### Requirements Impact Analysis (Impact Analysis)

**Problem**: When new requirements come in, AI cannot quickly judge "what will be affected by changing something", resulting in the omission of key constraints in the requirements analysis stage, repeated reinvention of the wheel in the design stage, and violation of existing contracts in the implementation stage.

**Mechanism**: After R1 (requirements clarification) is completed and before D0/D2, a lightweight "requirements landing point analysis" step is added to automatically extract the impact report from the project knowledge base.

**Impact Analysis Inputs and Outputs**:

- **Input**:`requirements/solution.md`Goals/Scope/Key Processes in
- **Project Knowledge Base Query**:
  - from`products/index.md`Match affected business modules
  - from`components/index.md`Match affected application components
  - from matching`components/{module}.md`Extract API/Data invariants to be respected
  - from`adr/index.md`Extract historical decisions that may have been affected
- **Output**: Write`specs/{id}/requirements/solution.md#impact-analysis`:
  - List of affected modules (Products + Components)
  - Invariants to be respected (extracted from module page API/Data Contract)
  - Relevant ADR (may constrain design direction)
  - Cross-module impact (derived from dependency graph)

> This is the consumption scenario with the highest ROI for the project knowledge base: one analysis, and subsequent D2/I1/I2 benefits throughout the entire process.

### Knowledge incremental evolution (Delta Discover + Staleness Detection)

**Question**: The Discover SOP is a complete 7-step process suitable for initialization. However, projects continue to evolve, and if the knowledge base cannot be updated with code changes, it will soon become "outdated and invalid".

**Mechanism 1: Incremental Discover (Delta Discover)**

- **Trigger timing**: When Merge-back is completed, or PR involves changes in the core files of the P0/P1 module
- **Execution Scope**: Based on`git diff --stat`(or PR change file list), identify the affected modules, and only perform Step 4 (module page update) + Step 7 (DoD verification) for these modules instead of re-running the full SOP
- **Output**: Update of affected modules`components/{module}.md`, and backfill`components/index.md`Status

**Mechanism 2: Staleness Detection**

- Documented in module page frontmatter`last_verified_at`(last verification time) and`source_files`(List of key source files)
- CI can check "whether more than N submissions/N days have passed since the last verification", and the expired mark is`stale`
- `stale`When the module is hit by Impact Analysis, it automatically prompts "The knowledge of this module may be expired. It is recommended to execute Delta Discover first."

**Mechanism 3: Merge-back triggers Discover verification**

- After Merge-back is completed, a DoD quick verification will be automatically run on the module page involved to ensure that the promoted content is consistent with the module page as a whole.

### Knowledge quality measurement

| Indicators | Definition | Purpose |
|---|---|---|
| **Knowledge coverage** | Number of P0 modules on completed module pages / Total number of P0 modules × 100% | Project health index |
| **Link reachability rate** |`.aisdlc/`The number of relative links that can be reached / the total number of links × 100% | CI is automatically verified, and an error is reported when the link is broken |
| **Knowledge Utilization** | Spec Pack stages`depends_on`The proportion of project-level knowledge cited in | Guide the priority of subsequent maintenance: the most cited knowledge assets are maintained first |
| **Knowledge Freshness** | Not`stale`Number of P0 modules / Total number of P0 modules × 100% | Quantitative reflection of expiration detection |

---

## Requirements Spec Pack life cycle and Merge-back

### Requirement life cycle status flow

The complete life cycle of each requirement (Spec Pack) from creation to archiving:

- **Draft**: Create the requirements directory structure and initialize it`index.md`- **In Review**: requirements review stage, improvement`requirements/prd.md`- **Approved(DoR)**: The requirements decision review is completed and DoR is reached (scope frozen, acceptance executable, dependencies available, risks controllable)
- **In Dev**: In the development execution phase, the code and Spec documents are updated simultaneously
- **In QA**: Test verification phase, execute tests and generate reports
- **Released**: Released online, gradually increasing volume according to grayscale strategy
- **Merged & Archived**: Execute Merge-back to promote reusable assets to the project level

### Merge-back: Turn short-term deliveries into long-term assets

After the requirements are completed, all documents should not be "copied" to the project layer, but should be screened and promoted according to asset type:

#### Content that must be merged back into the project layer (default)

- **ADR**: any critical decision must be entered`project/adr/`And in`project/adr/index.md`Summary
- **External contract (merged into component page by default)**:
  - API: If there are changes, update the corresponding`project/components/{module}.md#api-contract`(authority entry + invariant summary + evidence entry + gap list)
  - Data: If there are changes, update the corresponding`project/components/{module}.md#data-contract`(Data master + authoritative entry + invariant summary + evidence entry + gap list)
- **Running Assets**: Online related runbooks/monitoring alarms/rollback strategies, updated`project/ops/`- **NFR Budget and Baseline**: Update if there is any impact on performance/stability/cost`project/nfr.md`(budget, current situation, goals)

#### How Merge-back is executed

in every need`specs/<DEMAND-ID>/merge_back.md`Maintenance checklist (Done/Not Done):
- Whether the ADR has been filed to`project/adr/`- Whether the API/Data has been updated to the corresponding`project/components/{module}.md`paragraph of the contract (and`project/components/index.md`The link can jump to the anchor point stably)
- Runbook/monitoring has been updated to`project/ops/`- Is the NFR budget updated to`project/nfr.md`- Whether the Registry updates the requirement status to Released / Merged (update`project/index.md`)

> Merge-back is part of "requirements truly completed" and is recommended for inclusion in DoD.

---

## Specification of atomic Spec (allowing AI to "read accurately and write correctly")

### File header metadata (YAML Frontmatter, recommended to be mandatory)

Each atomic Spec file is recommended to start with the following metadata for indexing, dependency and disclosure policies:```yaml
---
id: 001-user-auth                   # 全局唯一 ID（格式：{num}-{domain-name}）
demand_id: 001-user-auth             # 所属需求 ID（格式：{num}-{domain-name}）
stage: clarify                       # clarify/design/implementation/verification/release/...
title: 用户登录（短信验证码）
status: draft                        # draft/review/approved/deprecated
owners: [PM, BA, DEV, QA]
depends_on:
  - project/memory/product.md
  - project/components/auth.md#api-contract
  - specs/001-user-auth/requirements/prd.md
policy_refs:
  - project/memory/tech.md#质量门禁
  - project/memory/product.md#安全
related_code:
  - src/auth/*
related_tests:
  - tests/e2e/auth-login.spec.ts
---
```### Recommended text structure (minimum closed loop)

- **Background and Goals**: Why we do it and what we want to achieve
- **Range**: In/Out
- **Process**: Mermaid (force priority over plain text)
- **Rules and Boundaries**: exceptions, idempotence, concurrency, permissions, auditing
- **Data and Interface Contract**: OpenAPI/Schema/SQL fragment
- **Acceptance Criteria (AC)**: verifiable conditions that can be directly transferred to test cases
- **Traceback link**: related ADR, related code, related tests, related release items

---

## How to store the output of each stage into the database (writing location agreement)

### Project level output (long-term assets)

- **Architecture evolution**:`project/memory/`（product.md、tech.md、structure.md、glossary.md）
- **Architectural Decisions**:`project/adr/`(architectural decision record)
- **Contract update (merged into component page by default)**:`project/components/{module}.md`（`## API Contract` / `## Data Contract`, and point to authoritative evidence in the warehouse in the paragraph)
- **Run Assets**:`project/ops/`（runbook.md、release.md、monitoring.md）
- **NFR 预算**：`project/nfr.md`- **Project Overview**:`project/index.md`(Spec Registry)

### Demand level output (delivery closed loop)

- **Requirements clarification**:`specs/<DEMAND-ID>/requirements/raw.md`、`requirements/solution.md`(Goal/scope/key process/acceptance criteria; replaces original product/refactor)
- **Demand decision (design)**:`specs/<DEMAND-ID>/design/`（`design.md`as the core; including research/contract/data/timing, etc. as needed)
- **Requirement implementation**:`specs/<DEMAND-ID>/implementation/`(Execution plan, task decomposition, migration and verification records; and traceability back to the code/PR)
- **Requirements testing (verification)**:`specs/<DEMAND-ID>/verification/`(test plan, use cases/regression sets, reports)
- **Release**:`specs/<DEMAND-ID>/release/`(Release plan, runbook, monitoring alarm, rollback, review)
- **Merge-back**:`specs/<DEMAND-ID>/merge_back.md`(Promotion list and evidence: sync to`project/`ADR/contract/operation and maintenance/NFR, etc.)

---

## Minimum implementation checklist (it is recommended to start here)

1. **Establish project-level structure**:
   - Create`.aisdlc/project/`Directory structure
   - Create`project/memory/`directory, complete`product.md`、`tech.md`、`structure.md`、`glossary.md`- Create`project/index.md`(Spec Registry)
   - Create`project/adr/`Catalog (architectural decision record)
   - Create`project/components/`、`project/ops/`、`project/nfr.md`infrastructure

2. **Create project-level Memory**:
   - Memory file (`product.md`、`tech.md`、`structure.md`、`glossary.md`) is located at`project/memory/`Directory
   - These files are linked to the stable assets of the project-level SSOT (`project/adr/`、`project/components/`、`project/ops/`etc.)

3. **Example of creating a requirement-level structure**:
   -Choose a real need and create`specs/001-demo/`Directory structure (requirement number format:`{num}-{domain-name}`)
   - Create`specs/001-demo/index.md`, initialize requirement meta-information
   - Write 1 copy according to metadata specifications`specs/001-demo/requirements/solution.md`4. **Improving the demand level Spec Pack**:
   - Complete this requirement`design/`(design.md, API+data+ADR) and`verification/`(use case + report template)

5. **Establish Merge-back mechanism**:
   - Create`specs/001-demo/merge_back.md`Checklist
   - After the requirements are completed, execute Merge-back to promote the reusable assets to the project level