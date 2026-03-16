---
markdown-sharing:
  uri: 9ad9e4f3-f0ac-40f2-ad7d-e4676a39dafe
---


# AI SDLC 工具介绍

本工具提供一套 **Spec 级**工作流与技能集，围绕 **双层 SSOT（项目级 SSOT + 需求级 Spec Pack）**、**Spec as Code**、**渐进式披露**，把一个需求从“原始输入”推进到“可评审的决策（可选）”与“可直接执行的实现计划 + 分批执行”。

---

## 安装 / 更新

```

# powershell
npx skills add https://github.com/zixun-github/aisdlc --skill * --agent claude-code cursor --yes --copy --global

# bash
npx skills add https://github.com/zixun-github/aisdlc --skill '*' --agent claude-code cursor --yes --copy --global

```


## 创建项目级索引库

```
/project-discover
```

## 需求开发

```
# 开始新的需求或BUG修复(会自动创建开发分支)
/spec-init 输入新的需求内容...（自动进行澄清）
# 创建执行计划
/spec-plan 
# 执行计划
/spec-execute
# 测试验证（可选）
/spec-test
```

---
## 小需求（轻量）Spec Pack：最短闭环步骤（推荐）

适用于 **范围小、影响面可控、无明显交互不确定性** 的需求（例如：小修复、小增强、脚本/配置调整、一次性迁移）。目标是 **最小落盘 + 可追溯 + 可执行**，避免把小需求做成“重流程”。

- **步骤清单（从零到完成）**
  - **R0：初始化**：`spec-init` → 生成分支与 Spec Pack，并落盘 `raw.md`
  - **R1：最小澄清**：`spec-product-clarify` → 产出精简 `solution.md`（写清边界与验收）
    - 若需求已经清楚：也建议用极简方式补齐 `solution.md`，保证后续评审与回溯有锚点
  - **I1：实现计划**：`spec-plan` → 产出 `implementation/plan.md`
  - **I2：分批执行**：`spec-execute` → 按 `plan.md` 分批实现与最小验证，并回写审计信息
---

## 步骤速览（用途 & 输出）

> 下列步骤按“最短路径优先、按需扩展”组织：R0–R4 用于澄清与产品侧产物；D0–D2 为设计阶段（可整体跳过）；I1–I2 为实现阶段（必做）；V1–V4 为验证阶段（按需）。

- **R0：`spec-init`（初始化新需求）**
  - **用途**：创建 Spec 工作空间（分支 + Spec Pack 目录），并把原始需求落盘为可追溯输入
  - **输出**：新分支 `{num}-{short-name}` + `.aisdlc/specs/{branch}/...` + `requirements/raw.md`

- **R1：`spec-product-clarify`（澄清 + 方案决策）**
  - **用途**：把 `raw.md` 的模糊需求收敛为可评审的推荐方案，并给出 2–3 个备选与验证清单
  - **输出**：`requirements/solution.md`

- **R2：`spec-product-prd`（可选：PRD/交付规格）**
  - **用途**：把 R1 的决策转为可交付、可验收、可测试的规格（范围/场景/AC/风险与依赖）
  - **输出**：`requirements/prd.md`

- **R3：`spec-product-prototype`（可选：原型说明）**
  - **用途**：当存在新增/变更交互或交互不够明确时，用任务流 + 页面结构 + 状态说明消除理解偏差
  - **输出**：`requirements/prototype.md`

- **R4：`spec-product-demo`（可选：可交互 Demo）**
  - **用途**：把 `prototype.md` 的页面清单与交互说明落地成可运行 Demo，用于走查/验证/对齐并支持回流
  - **输出**：Demo 工程目录（默认 `demo/prototypes/{CURRENT_BRANCH}/`）

- **D0–D2：设计阶段（整体可跳过）**
  - **D0（分流）**：判断是否跳过 design；若跳过，implementation 的 `plan.md` 必须补齐最小决策信息（目标/边界/约束/验收/验证清单）
  - **D1：`spec-design-research`（可选 research）**
    - **输出**：`design/research.md`
  - **D2：`spec-design`（RFC/Decision Doc；未跳过时必做）**
    - **输出**：`design/design.md`

- **I1–I2：实现阶段（必做）**
  - **I1：`spec-plan`（实现计划 / SSOT）**
    - **输出**：`implementation/plan.md`（唯一执行清单与状态 SSOT）
  - **I2：`spec-execute`（分批执行 + 回写审计）**
    - **输出**：代码与配置变更；并将任务状态/审计信息**只回写**到 `implementation/plan.md`

- **`spec-test`（验证阶段，按需）**
  - **用途**：测试计划、用例、套件、报告与缺陷的生成与落盘
  - **输出**：`verification/*` 相关产物
  - **子技能**：`spec-test-plan`（测试计划）→ `spec-test-usecase`（用例）→ `spec-test-suites`（套件，可选）→ `spec-test-execute`（报告）；`spec-test-bug`（缺陷报告，可插入）

- **快捷方式**
  - 不确定下一步怎么选：`using-aisdlc`，自动判读 spec pack 的进展及下一步的推进

---

## Spec Pack（你最终会落盘什么）

- **分支（上下文锚点）**：`{num}-{short-name}`
- **根目录（需求级 SSOT）**：`.aisdlc/specs/{num}-{short-name}/`
- **常用产物（按阶段渐进生成）**
  - **Clarify / requirements/**
    - `requirements/raw.md`：原始输入（证据入口）
    - `requirements/solution.md`：澄清 + 方案决策（需求侧 SSOT）
    - `requirements/prd.md`：（可选）交付规格（更细 AC/范围/依赖）
    - `requirements/prototype.md`：（可选）原型说明（任务流/页面/状态/AC 映射）
  - **Design / design/**（整体可跳过；未跳过时 `design.md` 为 SSOT）
    - `design/research.md`：（可选）调研结论（风险/假设 → 验证清单）
    - `design/design.md`：（可选）决策文档 / RFC（design 阶段 SSOT，写决策不写实现）
  - **Implementation / implementation/**
    - `implementation/plan.md`：实现计划（I1 必做；**唯一执行清单与状态 SSOT**，含任务 checkbox、步骤、最小验证、提交点与审计信息）
  - **Verification / verification/**（按需）
    - `verification/test-plan.md`：测试计划（V1；范围/策略/环境/准入准出）
    - `verification/usecase.md`：测试用例（V2；AC 可追溯）
    - `verification/suites.md`：（可选）测试套件（V3；smoke/regression/targeted）
    - `verification/report-{date}-{version}.md`：测试报告（V4；结论 + 缺陷引用）

---

## 项目包含多个Git 仓库工作方式

- 创建新的项目根仓库 project_root
- 使用 git submodule 将各个子仓库加入到 project_root 中，命令为 `git submodule add <repo-url> [<path>]`

当项目使用 `git submodule`（存在 `.gitmodules`）时，Spec Pack 流程会按以下方式适配多仓协作：

- **Spec Pack 始终在根项目**：需求/设计/实现文档统一落在根项目的 `.aisdlc/specs/{branch}/`，子仓仅作为代码工作区，不承载 Spec 文档。
- **spec-init**：只初始化根项目的 Spec 分支；子仓分支由后续 I1/I2 门禁处理。
- **spec-context**：会额外暴露 submodule 状态快照（分支/HEAD/脏工作区），供实现阶段校验。
- **I1（spec-plan）**：在 `plan.md` 中声明「子仓范围」与「代码工作区清单」（路径、是否受影响、是否 required、期望分支）；任务审计按 repo 记录。
- **I2（spec-execute）**：执行前**必须**校验受影响的 `required` 子仓是否已切到与根项目同名的 Spec 分支（如 `001-xxx`）；若不满足则阻断并汇报。执行后按 repo 回写 `branch/commit/pr/changed_files`，不把多仓结果压成单条。
- **spec-merge-back**：晋升资产时需区分证据来自根项目还是子仓路径。

**简要流程**：`spec-init`（根仓）→ 澄清/设计 → `spec-plan`（声明子仓）→ 手动或脚本将子仓切到同名分支 → `spec-execute`（校验 + 按 repo 审计）。

---

## 使用最佳实践

面向本工具使用者的推荐做法，可减少上下文漂移、返工与不可追溯问题：

- **先项目级，再需求级**：团队规模化使用前，建议先用 `project-discover` 建立 `.aisdlc/project/` 知识库（至少 memory + 1–3 个 P0 模块页），再跑 Spec Pack，可减少 `CONTEXT GAP` 与影响分析漂移。
- **不确定下一步时用 using-aisdlc**：让 Router 根据当前产物与意图自动判定下一步技能，避免手动选错阶段。
- **重要！**任何时候都优先使用技能，特别是在执行阶段有任何针对方案和代码的调整都优先使用 spec-plan 技能，保障 spec pack 信息的一致。
---

