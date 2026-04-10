---
markdown-sharing:
  uri: 9d3f0083-b31b-4525-a493-fd9105927981
---
# AI SDLC: Discover (reverse) SOP for existing projects - reversely generate project knowledge base from code

> This article is **Design Guide for Project Knowledge Base Construction (Reverse Engineering Version)**: For "stock projects with existing code", use a set of executable SOP to reversely precipitate the warehouse facts (code/configuration/CI/contract/run entry) into`.aisdlc/project/`Project-level SSOT.
> The focus is not on "translating code into documents", but on establishing a **map layer + authoritative portal + evidence chain** to make subsequent AI-assisted development more stable, less guessing, and more traceable.

---

## 0. What you will get (profit) and what you will not do (stop loss line)

### 0.1 Main benefits (AI + collaboration)

- **Reduce AI's "guessing the boundary/guessing the entrance"**: The project-level map layer fixes "where is the authority, where to enter, and where the boundary is".
- **Reduce repeated scanning and context waste**: The index is only used for navigation, and details are entered into the module page (including API/Data contract paragraphs) on demand.
- **Improve consistency and traceability**: Turn API/Data contracts, key decisions (ADR), and operation portals (ops) into linkable evidence chains.
- **Reduce rework**: When changes/faults/connections occur, you can quickly locate "where to look, where to change, and how to verify".

### 0.2 Non-target (avoid maintenance cost explosion)

- Do not pursue "full field-level data dictionary"; unless required by compliance/reconciliation/KPI caliber governance, only create **authoritative entry page + invariant summary + evidence link**.
- Do not write requirement-level one-time delivery details into the project level; one-time delivery details are archived in`specs/<DEMAND-ID>/`, reusable assets are promoted back to the project level through Merge-back (for principles, see`design/aisdlc.md`).

---

## 1. Product and placement location (project-level SSOT)

> Below is the **standard placement structure** for output.

### 1.1 Level-0 (Polaris / Memory)

-`.aisdlc/project/memory/structure.md`: Warehouse structure and entrance (how to locate the module, how to run/test/release the entrance link)
-`.aisdlc/project/memory/tech.md`: Technology stack and engineering guardrails (quality access control, dependency constraints, NFR budget entrance)
-`.aisdlc/project/memory/product.md`:Business boundary and core terminology entry (only write stable semantics)
-`.aisdlc/project/memory/glossary.md`: Glossary (keep it short, link to authoritative source)

### 1.2 Level-1 (map layer index)

-`.aisdlc/project/components/index.md`and`.aisdlc/project/components/{module}.md`: Application component map and module page
-`.aisdlc/project/products/index.md`and`.aisdlc/project/products/{module}.md`: Business module map and module page (optional; but it is recommended to converge to<= 6）

>**Structural constraints**: No output`.aisdlc/project/contracts/**`.
>
> The **API and Data contract** of the module are unified and merged into`.aisdlc/project/components/{module}.md`Fixed paragraph within:
> -`## API Contract`
> - `## Data Contract`>
### 1.3 Run the portal (optional but high ROI)

-`.aisdlc/project/ops/`: Runbook/monitoring alarm/rollback and other "entry pages" (no repeated steps, only links and key points)
-`.aisdlc/project/nfr.md`: NFR budget/baseline (if the team already has a system, you can only make the entrance link)

---

## 2. SOP overview (first have a map, then gradually add evidence)```mermaid
flowchart TD
  preflight[Step0_Preflight] --> scope[Step1_Scope]
  scope --> l0[Step2_Level0_Memory]
  l0 --> l1[Step3_Level1_IndexSkeleton]
  l1 --> modules[Step4_Modules_SinglePageSSOT]
  modules --> products[Step5_Products_Aggregation]
  modules --> ops[Step6_OpsAndEvidence]
  products --> dod[Step7_DoD_Gates]
  ops --> dod
  dod --> iterate[Iterate_Maintain]
```---

## 3. Step 0: Preflight (preparation and material inventory)

**Goal**: First, clarify "what facts can be used as evidence". What is subsequently written into the knowledge base is not the opinion, but the "entry link + evidence location".
**Principle**: Prioritize quoting "executable evidence" (scripts/CI/contract files), followed by descriptive documents.

### Input

- Warehouse (directory structure, build scripts, dependency files, configuration files, CI/CD configuration)
- Running mode (local startup, environment variables, deployment entry)
- Test entrance (single test/integrated test/E2E, quality access control)
- Existing contracts and structured facts (OpenAPI/Proto/JSON Schema/SQL migrations/ORM models)
- Observability portal (monitoring, log query, alarm, runbook, rollback strategy)

### Actions (minimal list)

- Find the **only trusted entrance** (priority script/CI/README/Makefile/package.json and other executable evidence)
- Marking: Which are "long-term stable entries" (suitable for project level), which are "requirements one-time details" (suitable to stay in spec)
- Compile an "evidence entry list" (you can make a draft first, and then write it into the module page (including API/Data contract paragraphs) and ops page)

### Output

- A traceable entry list (link to: Run/Test/CI/Contract/Key Directory/Monitoring Alarm)

---

## 4. Step 1: Scope (range stop loss: P0/P1/P2)

**Goal**: The biggest risk of reverse engineering is "trying to cover all modules leading to maintenance failure". Scope's task is to first clarify: which modules must be done, which ones can be done on demand, and which ones are postponed.

### 4.1 Module classification (recommended)

- **P0 (must be reversed)**: high-frequency changes, cross-team interfaces, many external integrations, accident/fault hotspots, and high compliance risks
- **P1 (recommendation)**: Stable but often quoted/asked/relied on basic abilities
- **P2 (reverse on demand)**: low risk, low collaboration, short life cycle; only index placeholders and entries are retained

### 4.2 Reverse depth and product requirements (strong constraints)

- P0: Must have`components/{module}.md`, and the file **also contains**`API Contract` + `Data Contract` + `Evidence`(Code/Test/CI/ops entry)
- P1: Must have`components/{module}.md`, allowing a section of the API or Data to be downgraded in the **Evidence gap** way (see Step 4 template)
- P2: Only in`components/index.md`and`products/index.md`Placeholder navigation (optional)`components/{module}.md`); just keep the entry link

---

## 5. Step 2: Level-0 (Memory / Polaris)

**Goal**: Let anyone/AI know within 3 minutes: what the project is, what its boundaries are, how to run it, how to verify it, and where the authoritative entrance is.

### 5.1 Writing constraints (project level must be short)

- **Only write stable entrances and boundaries**: Directory/Command/Contract/Run Entrance/Guardrails
- **Avoid one-time delivery of details**: field-level constraints, detailed timing, and migration steps are dropped to spec
- **Links must be "clickable and locatable"**: Prioritize linking to specific files (or reproducible commands) in the warehouse, avoid using directory placeholders or writing methods that will break the link under the current relative path (such as writing only`design/`、`docs/`).
- **Gap must be structured**: avoid scattering "not found/to be filled" in the text; write them uniformly`## Evidence Gaps（缺口清单）`, and give the location and impact of candidate evidence (so that the follow-up does not rely on guessing).

### 5.2 Memory minimal template (can be copied)

####`memory/structure.md`- Project form: single/multi-service/Monorepo (use the warehouse facts as evidence)
- Entrance:
  - Local startup:`<命令/脚本路径>`- test:`<命令/脚本路径>`- Build/Release:`<CI job / pipeline 链接或脚本>`- Code Map:
  - Component index entry:`components/index.md`- Contract entrance: enter the corresponding`components/{module}.md`,exist`API Contract` / `Data Contract`Paragraph View Authoritative Entrance and Invariants
  - Run entry:`ops/`(if any)
-`## Evidence Gaps（缺口清单）`:
  - What is missing (such as coverage access control/monitoring entrance/contract generation command)
  - Candidate evidence location (specific to "File/job/Command/Platform Entry")
  - Impact (guess what requirements/collaboration scenarios will result)

####`memory/tech.md`- Technology stack: Language/Framework/Database/Message/Gateway (only stable selections are listed)
- Quality access control entrance: lint/test/security scan (command and CI job link)
- NFR Guardrail Entry: Performance/Usability/Cost/Safety (link to`nfr.md`or external specification)
-`## Evidence Gaps（缺口清单）`: Same as above (such as front-end lint, stress test entrance, security baseline entrance)

####`memory/product.md`- Business boundaries: In/Out (one sentence + evidence entry)
- Key business module entrance:`products/index.md`(if any)
- Entry of key terms:`glossary.md`- Authoritative entrance (recommended minimum set):`components/index.md`、`products/index.md`(if any),`ops/index.md`(if any)

####`memory/glossary.md`- Terminology: definition (1 sentence) + authoritative source link (priority`components/{module}.md#api-contract` / `#data-contract`, followed by ADR/code type/external document; the link must be clickable and locatable)

---

## 6. Step 3: Level-1 (index skeleton + checkbox task panel)

**Goal**: First generate a "map skeleton", and then complete it iteratively by module; the index is only used for navigation and progress panels.

### 6.1 Index writing constraints

-`index.md`**Navigation only**: The table lists the module/Owner/entry/(same page anchor) contract link/running link; module details and invariants are not copied
- Manage completion progress with checkboxes:
  -`- [ ] moduleA`Indicates that the module page/contract entry page is not completed
  -`- [x] moduleA`Indicates that the DoD for the module has been reached

#### Index hard rules (checkable)

- **Unique map index**: with`components/index.md`is the unique map index.
  - API/Data contracts are not maintained`contracts/**`Index; from`components/index.md`Just link directly to the anchor point within the module page.
- **No writing details in the index**: must not appear in the index`invariants`、`evidence`、`待补`、`未发现`Placeholder or detail fields.
  - Details must sink to`components/{module}.md`of`API Contract` / `Data Contract` / `Evidence` / `Evidence Gaps`paragraph.

####`components/index.md`Cross-module dependency graph (new, recommended)

in`components/index.md`At the end, a call relationship diagram between modules in Mermaid format is maintained, so that AI can quickly determine "if A is changed, B and C need to be paid attention to" when doing demand impact analysis:```mermaid
graph LR
  moduleA --> moduleB
  moduleA --> moduleC
  moduleB --> moduleD
```> **Maintenance Rules**: Only draw direct dependencies (first-level calls), not transitive dependencies; mark the interaction mode (API/Event/DB) on the side; and maintain it synchronously with module page updates.

####`components/index.md`Recommended columns (minimally stable)

-`module`:Module short name (recommended kebab-case)
-`priority`：P0/P1/P2
- `owner`:Team/Responsible person (can be left blank, but do not write "to be determined", leaving blank means not registered)
-`code_entry`: Minimum locatable entry (directory or key entry file)
-`api_contract`: link to`./{module}.md#api-contract`
- `data_contract`: link to`./{module}.md#data-contract`
- `ops_entry`: link to`../ops/...`(if any)
-`status`: Check box (whether it can be checked is determined by the SSOT access control in Step 7)

#### Correct/wrong example (minimal snippet)

Correct (index navigation only, contract points to same page anchor):

| module | priority | owner | code_entry | api_contract | data_contract | ops_entry | status |
|--------|----------|-------|------------|--------------|---------------|-----------|--------|
| environment-management | P0 | platform-team |`server/module/environment/`| [api](./environment-management.md#api-contract) | [data](./environment-management.md#data-contract) | [ops](../ops/index.md) | - [ ] |

Error (index write details/placeholders, resulting in double writes and drift):

| module | invariants | evidence |
|--------|----------------|----------|
| environment-management | To be added | Not found |

---

## 7. Step 4: Modules (Single-page module SSOT: establish “authority”)

**Goal**: For each selected module (priority P0), output **single module page**`components/{module}.md`, and establish the authoritative entrance and evidence chain of the API/Data contract at the same time in this page; then backfill`components/index.md`Navigation links and status.
**Key constraint**: The contract paragraph in the module page is not the "field encyclopedia", but the "authoritative entry + invariant summary + evidence entry + gap list".

### 7.1`components/{module}.md`Minimal template (copiable, single page SSOT)

> **Anchor point stability requirements**: In order to allow both AI and humans to jump stably, the module page must contain the following fixed secondary titles:
> -`## TL;DR`(anchor`#tldr`）
> - `## API Contract`(anchor`#api-contract`）
> - `## Data Contract`(anchor`#data-contract`)

**Frontmatter metadata (required)**:```yaml
---
module: <module-short-name>
priority: P0|P1|P2
change_frequency: high|medium|low    # 基于 git log 统计
last_verified_at: <YYYY-MM-DD>       # 最后校验时间
source_files:                         # 关键源文件（用于过期检测）
  - <path/to/key/file1>
  - <path/to/key/file2>
---
```- **TL;DR (decision-level summary, 3-5 sentences, required)**: What does the module do, what are the boundaries, and what are the key invariants - let AI use the summary to determine whether it needs to go deeper during the map browsing stage
- Module positioning: In/Out (clearly what is not responsible for)
- Owner: Team/system leader (can be linked to organizational address book/duty list)
- Entrance:
  - Code entry:`<目录/路由/handler/consumer/job/cli 的路径>`- Run entry:`ops/<...>`(if any)
- Bearer service mapping (if any`products/*`): CAP/BP/BO number or minimum reference
- Representative collaboration scenarios (1–2): only write “who calls whom + key boundaries”, detailed timing sinking spec
- **Key state machines and domain events**: State machines (enum/status + transition logic) and domain events (publish/subscribe) identified from the code, only write summary (object name + state enumeration + key transition rules + event name + trigger timing)
- NFR allocation summary: performance/availability/security key points (only write guardrails and entrances)

#### Recommended structure of module pages (strongly recommended in this order)

-`# <模块中文名>（<module>）`(title)
-`## TL;DR`: 3-5 sentence decision-level summary (what the module does, boundaries, key invariants)
-`## 模块定位`：In/Out
  - **In**: one sentence ability boundary
  - **Out**: One sentence is not responsible for the scope
-`## Owner`-Team/Responsible Person/Duty Entry (leave blank if not available, do not write "to be determined")
-`## 入口`- Code entry (at least the directory can be located; P0 is recommended to key files)
  - Run portal (ops page link, if available)
-`## 协作场景（1–2 个）`- Only write "who calls whom + key boundaries", and the timing details are sunk into the spec
-`## State Machines & Domain Events`- Key state machine summary (object name + state enumeration + transition rule)
  - Summary of events in key areas (event name + trigger time + consumer)
-`## API Contract`- **Authoritative entrance (must be clickable/locatable)**: OpenAPI/Proto generated product path + generated command/phase; gateway/routing entrance
  - **Invariant summary (3–7 items)**: authentication/idempotence/error code family/version policy/audit requirements, etc.
  - **Evidence entry (minimum granularity)**:
    - At least 2 key handler file paths
    - At least 1 representative test classpath (if not, write`Evidence Gaps`)
    - CI access control: specific job name or command, and specify "whether to execute tests" (for example, whether to skip tests)
-`## Data Contract`- **Data Ownership**: Primary write/read-only/synchronization source (clear boundaries)
  - **Core objects and primary keys**: object name + primary key/unique identifier + life cycle in one sentence
  - **Authoritative entrance (must be clickable/locatable)**: Schema/DDL/Migration + ORM model
  - **Invariant summary (3–7 items)**: caliber/state machine/constraints
  - **Evidence entry (minimum granularity)**:
    - At least 1 repository/mapper path
    - At least 1 representative data read and write service path (optional)
    - Test evidence (if not, write it down`Evidence Gaps`)
    - CI evidence as above
-`## Evidence（证据入口）`- Code: key directory/file entry
  - Tests: specific test entrance (class/directory)
  - CI: specific job/pipeline entry
  - Ops: dashboard/alerts/logs/runbook/rollback (if yes, it will be linked, if not, it will enter the gap list)
-`## Evidence Gaps（缺口清单）`(When "To be filled/not found" appears, it must be written as a structured gap)
  - **Gap**: What is missing (testing/monitoring/generating commands/contract authority entry...)
  - **Expected granularity**: specific to "file/class/job/command"
  - **Candidate evidence location**: which directory/CI file/platform is most likely to be in
  - **Impact**: It will cause AI/collaboration to continue guessing at which step (for example, requirements analysis cannot determine idempotent/rollback semantics)

> **Forbidden**: Write API/Data paragraphs as field encyclopedias; field-level details are only pointed to schema/code through "authoritative entry" when necessary.

### 7.2 (Optional, high ROI) Requirements Analysis Semantic Card: Feature Impact Checklist

When the module often undertakes "copy/initialization/IaC/orchestration" type requirements (such as "environment replication"), it is recommended to append a section to the module page (still keep it short):

-`## Feature Impact Checklist（<feature>）`- Data: Which objects/fields are involved (only key field names and authoritative entries are listed)
  - Asynchronous: whether to use Job/Flow, what is the idempotent key, and how to roll back if it fails
  - IaC: warehouse/template source, target path and permission constraints
  - K8s: namespace/resource boundaries, quotas and recycling strategies
  - Authentication audit: permission model, audit points, operation traces
  - Verification: How to verify replication results in CI/environment (entry link)

---

## 8. Step 5: Products (Business module aggregation and convergence<= 6）

**目标**：从存量代码推导出“可治理的业务模块地图”，并把数量收敛到 <= 6（否则认知与维护会失控）。

### 8.1 从代码反推业务模块的线索（建议优先级）

>**Optimization (compared to only aggregation and convergence)**: Step 5 not only aggregates module names, but also deduces the business capability list, business rule index and key domain events from the code to provide business semantic anchoring for the demand phase.

- Data responsibility (strongest clue): which module is responsible for writing which core objects (see`components/{module}.md`of`Data Contract`)
- External capability boundaries: which APIs are stable commitments to external/other systems (see`components/{module}.md`of`API Contract`)
- Organizational boundaries: Module groups (Owners) responsible for different teams
- Operation boundary: independent deployment/independent scaling/independent SLO unit (if any)

### 8.2 Business capability list extraction (new, recommended)

On the Products module page (`products/{module}.md`) added:

- **Business Capability Catalog**: Deducing the external business capabilities provided by the module from the API route/handler name/data object (granularity to CAP-001 level), this is the key anchor of the demand placement
- **Business Rules Index**: Extract key constraints from the validation/policy/rule logic in the code, mark the source of the rules (code file path), so that the requirements stage can answer "What constraints does the system have in this scenario now?"
- **Key Domain Events**: Extract the event list from event publish/subscribe in the code, and mark the event semantics and consumers

> **Writing Constraints**: Only write entry-level summary (capability name + one-sentence description + code entry), do not write implementation details; field-level/timing-level details point to the code through the evidence entry.

### 8.3 What to do when convergence fails

- >6 is allowed, but the reasons (compliance isolation/split of data responsibilities/organizational boundaries/historical baggage) must be stated, and governance suggestions (entry to split/merge/migration route) given.

---

## 9. Step 6: Ops & Evidence (operation entry and evidence chain)

**Goal**: Fix the entrance that can be run, verified, rolled back, and troubleshooted. This often has a higher ROI than completing the field dictionary.

### 9.1 Writing constraints of running entry page (short, executable, upgradeable)

- Runbook/alarm descriptions should be **operational**: avoid general "checking logs" and should provide specific entrances (dashboard, log query, common repairs, upgrade contacts).
  - Reference: Google SRE Workbook
    -`https://sre.google/workbook/incident-response/`
    - `https://sre.google/workbook/postmortem-culture/`### 9.2 Evidence chain (written on the entry page)

- Spec (requirements) ↔ Components (module page: API/Data/Evidence) ↔ Code (implementation entry) ↔ Tests (verification entry) ↔ CI (access control) ↔ Ops (operation entry)

---

## 10. Step 7: DoD (Completion Standard) and Access Control Recommendations

### 10.1 Project Level DoD (Minimum Self-Checklist)

- [ ] Level-0 four copies of Memory already have "clear entrance/clear boundary/navigable"
- [ ] Level-1 index skeleton generated and checkbox task list available
- [ ] Each P0 module satisfies: exists`components/{module}.md`, and the page contains`TL;DR` + `API Contract` + `Data Contract` + `Evidence`(Satisfies the minimum granularity)
- [ ] Each P0 module page contains frontmatter metadata (`change_frequency`、`last_verified_at`、`source_files`)
- [ ] products has converged to<= 6；或已记录不可收敛原因与治理建议
- [ ] `components/index.md` 包含跨模块依赖关系图（Mermaid）
- [ ] 索引只导航，细节不双写；模块页是权威入口

#### 10.1.1 状态一致性门禁（SSOT，必须遵守）

>**Sole Source of Truth**: Whether a module is "done" is determined solely by that module's`components/{module}.md`Determine whether the content meets the standards;`components/index.md`The check mark simply reflects this fact.

-`components/index.md`Allow tags in a module`- [x]`Precondition (P0):
  - The module page exists and is navigable (`components/{module}.md`reachable)
  - Module pages contain fixed titles:`## TL;DR`、`## API Contract`and`## Data Contract`- Module page frontmatter contains`change_frequency`、`last_verified_at`、`source_files`
  - `API Contract`and`Data Contract`It must have at least: authoritative entry + 3–7 invariants + evidence entry (reaching the minimum granularity of “file/class/job/command”)
  - If there is a gap (e.g. no test/no monitoring/no build command), it must be written`## Evidence Gaps`and **not allowed** to mark this module as complete
- P1's`- [x]`Downgrade conditions are allowed:
  - The module page exists; either API or Data can be missing, but it must end with`Evidence Gaps`Structured record gaps and impacts
- P2 is not recommended in`components/index.md`Tick:
  - Only placeholder navigation is sufficient; upgrade to P1/P0 when necessary

### 10.2 Access control recommendations

- **Docs-as-Code**: Documents and code are subject to the same PR and review; provide PR preview; automatically check for broken links/formats
  - Reference: Read the Docs (docs-as-code, PR previews)
    -`https://about.readthedocs.com/docs-as-code`- **Catalog Completeness**: P0 module must exist`components/{module}.md`and contains`API Contract` / `Data Contract` / `Evidence`Paragraph; enforce in CI (drawing inspiration from software catalog/service catalog governance ideas)
  - Reference: Backstage (ensure catalog integrity)
    -`https://backstage.io/docs/golden-path/adoption/full-catalog`- **Orientation can be automated (recommended)**:
  - Broken link check (relative path is reachable)
  -`components/index.md`Whitelist check (disable detail columns/placeholders)
  - Check for forbidden words: appearing in the index`待补`、`未发现`Considered a violation (must be moved down to the module page`Evidence Gaps`)
  - P0 Paragraph Completeness: Module pages must contain`## API Contract`and`## Data Contract`Title
  - Evidence minimum granularity: at least N "file-level path" evidence must appear in the P0 module page (simple rule verification available)

---

## 11. Incremental Discover and knowledge preservation (new)

> **Problem**: The full Discover SOP is suitable for initialization, but the project continues to evolve. If the knowledge base cannot be updated with code changes, it will soon become "outdated and invalid".

### 11.1 Delta Discover (Delta Discover)

**Trigger time**:
- When Merge-back is completed (requirements introduce new contracts/ADRs/capabilities)
- When PR involves changes to the core files of the P0/P1 module
- Modules are marked as`stale`(when expiration detection is triggered)

**Execution scope**:
- Based on`git diff --stat`(or PR change file list) to identify affected modules
- Only execute Step 4 (module page update) + Step 7 (DoD verification) for these modules instead of re-running the full SOP
- Update affected modules`components/{module}.md`(includes TL;DR, contract paragraphs, state machines/events, Evidence), and backfill`components/index.md`Status

**Output**: updated module page + updated`last_verified_at`+ Index status backfill

### 11.2 Staleness Detection

- Record in frontmatter of each module page`last_verified_at`(last verification time) and`source_files`(List of key source files)
- CI can check "whether more than N submissions/N days have passed since the last verification", and the expired mark is`stale`
- `stale`When the module is hit by Impact Analysis, it automatically prompts "The knowledge of this module may be expired. It is recommended to execute Delta Discover first."
- Recommended expiration threshold: P0 module ≤ 30 days or 50 submissions; P1 module ≤ 90 days

### 11.3 Knowledge Quality Measurement

| Indicators | Definition | Purpose |
|---|---|---|
| **Knowledge coverage** | Number of P0 modules on completed module pages / Total number of P0 modules × 100% | Project health index |
| **Link reachability rate** |`.aisdlc/`The number of relative links that can be reached / the total number of links × 100% | CI is automatically verified, and an error is reported when the link is broken |
| **Knowledge Freshness** | Not`stale`Number of P0 modules / Total number of P0 modules × 100% | Quantitative reflection of expiration detection |
| **Knowledge Utilization** | Spec Pack stages`depends_on`Proportion of project-level knowledge cited in | Guiding subsequent maintenance priorities |

---

## 12. Common pitfalls and avoidance (reverse engineering version)

- **Trap: Trying to write it all in one go**
  - **Evasion**: Scope classification first; P0 lands first, then iteratively completes P1/P2
- **Trap: Writing one-time delivery details into the project level**
  - **Avoidance**: Only write entries/boundaries/guardrails at the project level; field-level and timing-level details are sunk into spec, and reused assets are then merge-backed.
- **Trap: Index and module double writing**
  - **Circumvention**: Index only navigation; module page is authoritative; index only backfills summary + link
- **Trap: The contract is not authoritative**
  - **Circumvention**: in module page`API Contract` / `Data Contract`The paragraph must have at least "authoritative entry link + invariant summary + evidence entry"; use ADR to record trade-offs if necessary

### 12.1 Number of files and merge strategy (for AI-assisted stop loss lines)

- **Document Organization**: One page per module`components/{module}.md`.
- **BANNED**: Merge multiple modules into one large file.
- **Scale control**: Downgrade via Scope; P2 only in`components/index.md`Placeholder, no module page is generated; upgrade to P1/P0 when necessary.

---

## Appendix A: Key differences between Discover and Design

- **Source of evidence**: Discover uses warehouse facts as evidence; Design uses design assets such as ADR/component page contract paragraphs as evidence and completes the code entry after implementation.
- **How ​​to start**: Discover first Preflight + Scope, then add the map layer; Design first defines the map layer and contract, and then drives the implementation.
- **Risk**: The biggest risk for Discover is "loss of coverage"; the biggest risk for Design is "contract failure/implementation drift". Both use "gate control + evidence chain + merge-back" to reduce risks.
- **Contract form**: Discover tends to "link to the existing schema/code entry first"; Design tends to "define the authoritative contract first and then implement alignment". Common principles: Contracts must be authoritative, traceable, and verifiable.
- **Output Position**: Common outputs are located on`.aisdlc/project/`;requirement level details still`.aisdlc/specs/<DEMAND-ID>/`.

---

## Appendix B: References

- Document Information Architecture (Diátaxis: Tutorial/How-to/Reference/Explanation):`https://diataxis.fr/foundations/`- Docs-as-Code (Git versioning, PR preview, automated deployment examples):`https://about.readthedocs.com/docs-as-code`- ADR (Michael Nygard template for documenting key trade-offs):`https://tarf.co.uk/Reference/Architecture/adr/decision_record_template/`- Architecture map layering (C4 Model):`https://c4model.com/`
- SRE（incident response & postmortem）：
  - `https://sre.google/workbook/incident-response/`
  - `https://sre.google/workbook/postmortem-culture/`- Software catalog/service catalog management (Backstage catalog integrity):`https://backstage.io/docs/golden-path/adoption/full-catalog`

