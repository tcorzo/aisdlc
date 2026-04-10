---
title: Spec-level design phase SOP (decision document/RFC; research optional; overall can be skipped)
status: draft
audience: [PM, BA, SA, DEV, QA]
principles_ref: design/aisdlc.md
---
## Design phase process (Design: research optional/design required; overall can be skipped)

### 1. Background and target (alignment`design/aisdlc.md`)

This document defines a **Spec-level** unified SOP for the "design phase": the core output is a **Decision Doc/RFC** for human review and consensus, answering "why do this/how to cut the boundaries/what options and trade-offs/what are the external commitments", rather than pursuing detailed design at the implementation level.

**Conclusion**:

- **The entire stage can be skipped**: When the demand boundary is clear, the risk is low, and there are no critical uncertainties, you can directly enter implementation.
- **If not skipped: only two paragraphs**:
  - **research (optional)**: Conduct research and analysis for specific technologies/fields to supplement the context and reduce design uncertainty.
  - **design (required)**: output`design/design.md`(design phase SSOT).
- **No "Detailed Design" sub-stage**: Contracts/data models, etc. belong to "On-demand attachments/External commitment placement"; implementation details are included in implementation`plan.md/tasks.md`.

> **Routing Authoritative Description (Important)**: D0 (whether to skip design), D1 (whether research is required), D2 (whether to enter RFC) and other "next step judgment/diversion" are determined by`skills/using-aisdlc/SKILL.md`As the only router to determine; this SOP is responsible for giving the caliber and DoD, and the routing will select the corresponding worker skill during specific execution:\n
>-D1:`spec-design-research` → `{FEATURE_DIR}/design/research.md`\n
> - D2：`spec-design` → `{FEATURE_DIR}/design/design.md`\n

---

### 2. Product placement and “progressive disclosure” reading sequence

#### 2.1 Recommended placement structure (demand level Spec Pack)

Alignment`design/aisdlc.md`Requirements level directory in (example):```text
.aisdlc/specs/<DEMAND-ID>/
  index.md
  requirements/
    ...                   # 已完成的需求澄清产物（solution/prd/prototype 等）
  design/
    research.md           # D1：research（可选）：研究/分析结论
    design.md             # D2：design（必做；仅当未跳过）：决策文档（Decision Doc / RFC）
```#### 2.2 Agent reading order (progressive disclosure)

- **Required Reading (project-level, mandatory, aligned context injection protocol)**:
  -`project/memory/*`(Business/Technology/Structure/Terminology)
  -`project/components/index.md`(Application component map + cross-module dependency graph)
  -`project/adr/index.md`(Architectural Decision Index)
  - **Full content of affected modules**: From`specs/{id}/requirements/solution.md#impact-analysis`(R1.5 output) Get the list of affected modules and read the corresponding`project/components/{module}.md`**All content** (including TL;DR, API/Data Contract invariants, state machine/domain events, evidence) - D2 must explicitly declare the relationship with the existing contracts of these modules
  - **Relevant ADR full text**: Get the relevant ADR number from the impact analysis, read`project/adr/{adr-id}.md`Full article – Ensuring designs don’t violate historical decisions
  - Explicitly marked as when read fails or does not exist`CONTEXT GAP`(Instead of silently skipping)
- **On demand (requirement level)**: Only process a certain`<DEMAND-ID>`When reading the minimum necessary materials for this requirement:
  - **Requirement Path**:`requirements/solution.md`、`requirements/prd.md`(optional),`requirements/prototype.md`(optional)
  - **Impact Analysis**:`specs/{id}/requirements/solution.md#impact-analysis`(R1.5 output, must read)
  - **Design Path**:`design/design.md`(if already exists) and`design/research.md`(optional)
- **Write back (into the library)**: Each module independently produces a file (or a chapter), keeping it replaceable and auditable.

#### 2.3 Context automatic recognition mechanism (access control)

Alignment`design/aisdlc_spec_init.md`"Context automatic recognition mechanism": **Anyone who can read and write`specs/<DEMAND-ID>/design/*.md`, you must first locate the current Spec Pack`{FEATURE_DIR}`**, it is forbidden to guess the path.

- **Public Skill**:`spec-context`(For definition see`skills/spec-context/SKILL.md`)
- **Hard rules (must be followed)**:
  - **Locate first then read and write**: any read/write`design/*.md`must be obtained before`FEATURE_DIR=...`- **Stop on failure**: If the context positioning fails, it must be stopped immediately and no further generation/writing of file content is allowed.
  - **Only use FEATURE_DIR to spell the path**: subsequent paths start with`FEATURE_DIR`as a prefix (e.g.`{FEATURE_DIR}/design/design.md`)

---

### 3. Distributed process overview (modular pipeline)

Goal: Each step can be executed, reviewed, and replaced independently; clear input/output alignment between steps avoids duplication of effort and context drift.

#### 3.1 Module List

| Module ID | Module name | Main goal | Key output (drop) |
|---|---|---|---|
| D0 | Diversion: whether to skip the design stage | Use a clear caliber to determine whether to "enter implementation directly" or "enter research/design", and declare that the implementation must be completed when skipping | (The routing conclusion is output by using-aisdlc; no forced placement) |
| D1 | research (optional) | Provide context for key uncertainties: status quo, constraints, risks, unknowns, and research conclusions |`design/research.md`(Depend on`spec-design-research`Placement) |
| D2 | design (required; only if not skipped) | Produce a reviewable decision document (RFC), freeze boundaries and key decisions, and provide authoritative input for implementation |`design/design.md`(Depend on`spec-design`Placement) |

#### 3.2 Shortest path (it is recommended to run through it first)

- **Skip path**: D0 (judgment skip) → enter implementation (and in`plan.md`Complete the minimum decision information)
- **General path**: D0 (not skipped) → (optional) D1 → D2 → implementation

#### 3.3 General access control and convergence rules (D0–D2)

- **Access Control**: Anyone can read and write`design/*.md`, execute first`spec-context`Get`FEATURE_DIR`; Stop on failure (see 2.3).
- **Writing Principles**: Conclusion first (conclusion → basis → verification); only retain the minimum information to support decision-making/implementation/acceptance; key caliber can be traced back`requirements/solution.md`(or`prd.md/prototype.md`).
- **Convergence Rules**:`design.md/research.md`There is no "list of issues to be confirmed"; unknowns are accepted with "hypothesis + verification list (Owner/cutoff/signal/action)".

---

### 4. Module D0: Diversion - whether to skip the design stage (key diversion)

#### 4.1 Objectives

Clarify whether this requirement needs to enter the design phase; if it is skipped, also clarify "why it was skipped" and the minimum information that must be completed in the implementation phase to avoid hiding key decisions in the implementation.

#### 4.2 Input

-`{FEATURE_DIR}/requirements/solution.md`(required)
- (optional)`{FEATURE_DIR}/requirements/prd.md`、`{FEATURE_DIR}/requirements/prototype.md`- Project level`project/memory/*`、`project/components/index.md`、`project/adr/`Index (on demand)

#### 4.3 Output

- **Conclusion to skip or not to skip**: reasons (within 3–7 items) + key basis (traceable to constraints/evidence entry)
- **Complete list when skipping**:implementation`plan.md`The "minimum decision information" that must be completed (see 4.5)

#### 4.4 Skip the judgment criteria (you can skip if one of them is met)

- **Single scope and clear boundaries**: almost no cross-module collaboration and systemic risks involved
- **No changes in external commitments**: No new/changed external contracts (API/events/permissions/data calibers), and no data migration
- **No key technology uncertainty**: No need for research verification first
- **Acceptance caliber is sufficient**: Acceptance is within`solution.md`(or`prd.md`) has become clear, testable, and traceable

#### 4.5 Implementation must be completed when skipping (minimum decision information)

> Constraint reminder: Once the design phase is skipped, the implementation`plan.md`The minimum decision-making information (goals, scope and boundaries, key constraints, acceptance criteria, verification list) must be completed, and no supplementary information is allowed; this rule is based on`design/aisdlc.md`The Layer1 constraints shall prevail.

#### 4.6 Next step (D0 → D1/D2 or direct implementation)

- **SKIP**: Enter implementation (and complete by 4.5`plan.md`)
- **No skip**: Enter D1 (research) → D2 (design) as needed

---

### 5. Module D1: research (research, optional)

#### 5.1 Objectives

Conduct research and analysis in specific technologies/fields for current needs, and supplement the context required for design decisions: status quo, constraints, risks, unknowns, and research conclusions.

#### 5.2 Input

- **Access Control**: Execute first`spec-context`Get`FEATURE_DIR`(Stop on failure; see 2.3/3.3)
- **Requirement Path**:`{FEATURE_DIR}/requirements/solution.md`(required) and (optional)`prd.md/prototype.md`- **Project Level Resources**:`project/memory/*`, related`components/{module}.md`、`adr/`Index (the contract entry is located on the component page`## API Contract / ## Data Contract`)

#### 5.3 Output (drop to`design/research.md`, optional)

Recommended minimum structure (research conclusions must be reusable and directly quoted by D2):

- **Summary of Conclusions (TL;DR, lines 3–7)**: Current Situation + Maximum Risks + Recommended Directions
- **Current situation and problem domain**: Key current situation, pain points and impact
- **Scope Bounds and Invariants**: In/Out and Invariants
- **Key Constraints**: Compliance/Performance/Dependencies/Organization
- **Risk and Verification Checklist (required)**: Risk/Assumption → Verification Method → Success/Failure Signal → Owner → Cutoff → Next Action
- **Alternatives and trade-offs (optional)**: If the research has reached a preferred conclusion, provide 2–3 alternatives and key differences

#### 5.4 Quality Threshold (D1-DoD)

- Unknown items are no longer left vacant in the form of "Questions to Be Confirmed" and are uniformly entered into the "Risk and Verification List"
- Research conclusions are traceable and can provide usable input into D2’s decision-making documents (can be cited without repeated explanations)

#### 5.5 Next step (D1 → D2)

Enter D2 output`design/design.md`(Decision Document/RFC).

---

### 6. Module D2: design (decision document/RFC, required; only if not skipped)

#### 6.1 Objectives

Map requirements/refactoring into reviewable decision documents: boundaries, core solutions, key decisions and trade-offs, external commitment (contract/data) points, and provide implementation`plan.md/tasks.md`Provide authoritative input.

#### 6.2 Input

- **Access Control**: Execute first`spec-context`Get`FEATURE_DIR`(Stop on failure; see 2.3/3.3)
- **Requirement Path**:`{FEATURE_DIR}/requirements/solution.md`(required) and (optional)`prd.md/prototype.md`- **Impact Analysis (required reading)**:`{FEATURE_DIR}/requirements/solution.md#impact-analysis`(R1.5 output), get the list of affected modules and the invariants that need to be observed
- (optional)`{FEATURE_DIR}/design/research.md`- **Project level (enforced, aligned context injection protocol)**:
  -`project/memory/*`(Business/Technology/Structure/Terminology)
  - of the affected modules`project/components/{module}.md`**Full content** (including API/Data Contract invariants, state machine/domain events)
  - Full text of relevant ADR (number obtained from impact analysis)
  - Mark when reading fails`CONTEXT GAP`#### 6.3 Output (drop to`design/design.md`）

`design/design.md`It is the **Single Decision Entry (SSOT)** in the design stage: clearly write "what to do/not to do/why/how to verify/how to commit to the outside world", without writing implementation details and task splitting.

Recommended minimal structure (can be used directly as a template). Among them, the "recommended solution" must be described using the first three levels of **C4** as a unified baseline for review (only to Component, not to Code level details):

- **Summary of conclusion (required, lines 3–7)**: Objectives + In/Out + One-sentence mechanism overview of the recommended solution + 1–3 points that require priority verification (cite the verification checklist number below)
- **Scope and Boundary (required)**: System boundaries, impact areas, clear what not to do (and`requirements/solution.md`Alignment)
- **Recommended solution (required, 1; described by C4 L1–L3)**
  - **C4-L1: System Context**: users/roles, external systems, system boundaries, key interactions and main inputs and outputs; clarify invariants and constraints (with Mermaid diagrams if necessary)
  - **C4-L2: Container (container/deployment unit)**: container divisions such as application/service/function/job, database/cache/queue; responsibilities of each container, main technology selection, key data flow and external contract entry (component page contract paragraph/event/interface)
  - **C4-L3: Component**: component splitting within key containers (responsibility/interface/dependency); key data model and state flow; error handling and idempotence/consistency strategy (described to "components and interfaces", without implementation details)
  - **Key decisions and trade-offs (required, ≥3 items)**: Trade-offs in dimensions such as performance/cost/consistency/complexity/evolution, explain why you chose it
  - **Key points of external commitments (required)**: contract/authority/data caliber/compatibility/migration and rollback commitment; update the correspondence if necessary`project/components/{module}.md`contract paragraph or add ADR
- **Alternatives (required, 2–3)**: applicable prerequisites for each alternative (when would you choose it) + reasons for not choosing (1–2 key differences are enough)
- **Alignment to existing systems (required, based on R1.5 impact analysis)**:
  - **Contract Compatibility Statement**: For each affected module, explicitly declare the relationship between this design and the existing API/Data contract (compatibility/extension/destructive changes), reference`components/{module}.md#api-contract` / `#data-contract`Concrete invariants in
  - **ADR Compliance Statement**: For each relevant ADR, explicitly declare whether this design complies with it and whether new/modified ADRs need to be added
  - **State machine/event impact**: For the state machine and domain events involved, indicate whether to add new states/events and whether to change the transfer rules (refer to the module page`## State Machines & Domain Events`)
  - **Cross-module impact confirmation**: Based on the dependency graph, confirm that all affected upstream and downstream modules have been considered
- **Impact analysis (required)**: upstream and downstream systems, data caliber, operation and maintenance impact, migration/rollback key points (on demand)
- **Risk and Verification Checklist (required)**: Risk/Assumption → Verification Method → Success/Failure Signal → Owner → Cutoff → Next Action
- **Traceback link (required)**:`requirements/solution.md`(as well as`prd.md/prototype.md`If applicable),`requirements/solution.md#impact-analysis`(R1.5 output), related component page contract paragraph/ADR entry

#### 6.4 Quality Threshold (D2-DoD)

- The plan covers the goals, scope and key constraints of the requirements, and the In/Out is clear
- The recommended solution is clearly described in the three levels of C4: **L1 (Context) + L2 (Container) + L3 (Component)** (diagrams or equivalent structures are acceptable), and the levels are traceable
- Key decisions can be traced (at least it can point out "why it was chosen" and "why the alternative was not chosen")
- **Alignment to existing systems is complete**: contract compatibility for each affected module declared, relevant ADR compliance confirmed, state machine/event impact accounted for
- Uncertainty has converged: unknowns are taken over with "hypothesis + verification list" (Owner/cutoff/action clear)

#### 6.5 Next step (D2 → implementation)

Entering the implementation phase: with`design/design.md`As input, generate implementation plan and task split (`plan.md/tasks.md`) and map the validation checklist to the test/release/rollback strategy.

---

### 7. Unified processing of requirements and reconstruction

- **Unified input**: Regardless of functional requirements or reconstruction requirements, all`requirements/solution.md`As demand side SSOT.
- **Difference handling**:
  - **Functional Requirements**: Focus on describing business goals, process changes, and alignment with acceptance criteria (Quote`solution.md/prd.md`of AC).
  - **Refactoring requirements**: Focus on describing the current baseline, refactoring goals, invariants, migration/rollback and regression verification strategies.
- **Verification Strategy**: Refactoring requirements must cover regression and control verification, and`design/design.md`Traceable in the "Risk and Verification Checklist".

---

### 8. Traceback and Merge-back tips

- New key decisions added during the design phase should be put into the`project/adr/`(or in`design/design.md`ADR entry and summary are provided in ).
- Changes to the interface or data contract should be updated accordingly`project/components/{module}.md`of`## API Contract / ## Data Contract`paragraph and make sure`project/components/index.md`Stable jump to anchor point.
- Reusable long-term assets are promoted to the project level through Merge-back after the requirements are completed (to avoid knowledge assets being scattered within a single Spec Pack).