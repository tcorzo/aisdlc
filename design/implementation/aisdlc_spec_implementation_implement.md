---
title: I3 执行（Execute）— 任务解析与实施执行设计规范
status: draft
stage: implementation
module: I3
principles_ref: design/aisdlc.md
source_refs:
  - design/aisdlc_spec_implementation.md
  - design/implementation/aisdlc_spec_implementation_tasks.md
---

## 0. 目标与定位

本设计文档用于定义 Implementation 阶段模块 I3「执行」的**框架性规则、硬约束与验收标准**，用于约束后续可能的命令/脚本实现，以及指导人工/AI 按 `implementation/tasks.md` 完成实际实施。

I3 的目标是：

- 将 `{FEATURE_DIR}/implementation/tasks.md` 解析为**可执行序列**（阶段/依赖/并行提示/文件冲突）
- 按计划执行并持续校验（门禁、验证检查点、错误处理）
- **回写执行状态到 `tasks.md`**（完成项必须标记为 `- [x]` 并附最小证据）
- Spec 阶段仅在需求包内落盘与回写，**项目级资产的晋升在 merge-back 阶段统一执行**

输出稳定落盘到：

- `{FEATURE_DIR}/implementation/tasks.md`（执行状态与证据回写）

---

## 1. 术语与接口

### 1.1 上下文与路径

- **FEATURE_DIR**：由 `Get-SpecContext` 自动获取，定位到 `.aisdlc/specs/{num}-{short-name}/`
- **必读输入**：
  - `{FEATURE_DIR}/implementation/tasks.md`
  - `{FEATURE_DIR}/implementation/plan.md`
- **设计上下文**：
  - `{FEATURE_DIR}/design/solution.md`（本项目的“设计核心文档”；等价于外部口径中的 `design.md`）
  - `{FEATURE_DIR}/design/data-model.md`（如存在）
  - `{FEATURE_DIR}/design/contracts/`（如存在）
  - `{FEATURE_DIR}/design/research.md`（如存在）
  - `{FEATURE_DIR}/quickstart.md`（如存在，用于集成场景入口）
- **参考输入（按需）**：
  - `{FEATURE_DIR}/requirements/prd.md` 或 `{FEATURE_DIR}/requirements/solutions.md`
  - `{FEATURE_DIR}/refactors/clarify.md`、`{FEATURE_DIR}/refactors/baseline.md`（如为重构路径）
- **项目级索引（只读）**：
  - `project/memory/*`、`project/contracts/`、`project/adr/`（仅用于查入口/编号/权威定义，不在 I3 阶段回写）

### 1.2 I3 的输入/输出约定

- **输入 SSOT**：
  - 执行清单与状态 SSOT：`implementation/tasks.md`
  - 技术栈与结构约束 SSOT：`implementation/plan.md`
  - 系统设计与决策上下文：`design/solution.md`（若存在）
- **输出 SSOT**：
  - 任务完成状态：回写到 `implementation/tasks.md`（必须）
  - 代码与配置变更：仓库代码（路径以任务条目内标注为准）
  - 决策/契约变更（Spec 内草案）：写入 `{FEATURE_DIR}/design/`（merge-back 再晋升到 `project/`）

---

## 2. 强制门禁（MUST）

- **必须存在** `{FEATURE_DIR}/implementation/tasks.md`，缺失则不得执行（ERROR）。
- **必须存在** `{FEATURE_DIR}/implementation/plan.md`，缺失则不得执行（ERROR）。
- `tasks.md` 必须使用严格清单格式：任务条目为 `- [ ]` 或 `- [x]`。
- 任何不确定项必须标注为 “NEEDS CLARIFICATION”，且要说明影响与取证路径；不得脑补。
- **完成任务后必须回写**：将对应条目改为 `- [x]`（大小写不敏感，但推荐 `x`），并附最小证据（提交号/PR/关键文件路径）。
- **Spec 阶段不得更新 `project/*`**（含 `project/adr/`、`project/contracts/`、`project/memory/` 等）：只允许读取索引作为参考；需要沉淀的稳定资产必须在 `{FEATURE_DIR}` 内草拟，并列入 merge-back 晋升清单。

---

## 3. I3 执行工作流（详细步骤）

> 注：以下步骤可以用于命令/脚本/Agent 执行实现；步骤中的路径已按本项目结构统一为 `{FEATURE_DIR}/...`。

### 3.1 设置（Setup）

- 在仓库根目录调用 `Get-SpecContext`（`.aisdlc-cli/scirpts/spec-common.ps1`），解析出 `FEATURE_DIR`
- 校验关键文件存在：
  - `{FEATURE_DIR}/implementation/tasks.md`
  - `{FEATURE_DIR}/implementation/plan.md`
- 设定执行策略：
  - **分阶段执行**：阶段 1 → 阶段 2 → 阶段 3+（按用户故事优先级）→ 最终阶段
  - **依赖优先**：依赖未满足的任务不得开始
  - **文件冲突串行**：涉及同一文件/目录的任务必须顺序运行（见 3.6）

### 3.2 加载并分析实施上下文（Load & analyze context）

- **必须**：读取 `{FEATURE_DIR}/implementation/tasks.md` 以获取完整任务列表与阶段结构
- **必须**：读取 `{FEATURE_DIR}/implementation/plan.md` 以获取技术栈、架构与文件结构约束（例如：语言/框架/构建与测试命令/目录规范）
- **必须（如存在；缺失则记录 NEEDS CLARIFICATION）**：读取 `{FEATURE_DIR}/design/solution.md` 以获取架构决策与系统上下文
- **如果存在**：读取 `{FEATURE_DIR}/design/data-model.md` 以获取实体与关系，指导模型/迁移/校验
- **如果存在**：读取 `{FEATURE_DIR}/design/contracts/` 以获取 API/事件/数据契约草案与对应测试要求（Spec 阶段仅草拟，不晋升到 `project/`）
- **如果存在**：读取 `{FEATURE_DIR}/design/research.md` 以获取技术决策、约束与权衡背景
- **如果存在**：读取 `{FEATURE_DIR}/quickstart.md` 以获取集成/验收场景入口（端到端用例、联调步骤、样例数据）
- **按需**：读取 `{FEATURE_DIR}/requirements/prd.md` 或 `{FEATURE_DIR}/requirements/solutions.md`（用于核对 AC 与业务验收口径）
- **只读参考**：读取 `project/memory/*`、`project/contracts/`、`project/adr/` 索引（仅用于查入口与编号；禁止在 I3 回写）

### 3.3 项目设置验证（Repository hygiene）

> 目的：根据实际项目设置创建/验证忽略文件，减少噪音与误提交风险。该步骤属于工程配置，可在 I3 中执行；但其不等同于更新 `project/*` SSOT（I3 仍禁止修改 `project/` 目录）。

**检测与创建逻辑（PowerShell 语义）**：

- **Git 仓库检测**：执行 `git rev-parse --git-dir 2>$null`  
  - 成功：创建/验证 `.gitignore`
  - 失败：跳过 `.gitignore`（或记录 NEEDS CLARIFICATION：仓库并非 git 或 git 未安装）

- **Docker ignore**：
  - 若仓库存在 `Dockerfile*`，或 `plan.md` 明确使用 Docker：创建/验证 `.dockerignore`
- **ESLint ignore**：
  - 若存在 `.eslintrc*`：创建/验证 `.eslintignore`
  - 若存在 `eslint.config.*`：确保配置中的 `ignores` 覆盖所需模式（不强制创建 `.eslintignore`）
- **Prettier ignore**：
  - 若存在 `.prettierrc*`：创建/验证 `.prettierignore`
- **npm ignore**（仅发布包场景）：
  - 若存在 `.npmrc` 或 `package.json` 且 `plan.md` 明确为“发布 npm 包”：创建/验证 `.npmignore`
- **Terraform ignore**：
  - 若存在 `*.tf`：创建/验证 `.terraformignore`
- **Helm ignore**：
  - 若存在 Helm charts：创建/验证 `.helmignore`

**规则**：

- 若忽略文件已存在：只追加缺失的关键模式，不做破坏性重写。
- 若忽略文件缺失：为检测到的技术创建包含完整模式集的文件。

**按技术分类的通用模式（从 `plan.md` 技术栈推导）**：

- **Node.js/JavaScript/TypeScript**：`node_modules/`, `dist/`, `build/`, `*.log`, `.env*`
- **Python**：`__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `dist/`, `*.egg-info/`
- **Java**：`target/`, `*.class`, `*.jar`, `.gradle/`, `build/`
- **C#/.NET**：`bin/`, `obj/`, `*.user`, `*.suo`, `packages/`
- **Go**：`*.exe`, `*.test`, `vendor/`, `*.out`
- **Ruby**：`.bundle/`, `log/`, `tmp/`, `*.gem`, `vendor/bundle/`
- **PHP**：`vendor/`, `*.log`, `*.cache`, `*.env`
- **Rust**：`target/`, `debug/`, `release/`, `*.rs.bk`, `*.rlib`, `*.prof*`, `.idea/`, `*.log`, `.env*`
- **Kotlin**：`build/`, `out/`, `.gradle/`, `.idea/`, `*.class`, `*.jar`, `*.iml`, `*.log`, `.env*`
- **C++**：`build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.so`, `*.a`, `*.exe`, `*.dll`, `.idea/`, `*.log`, `.env*`
- **C**：`build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.a`, `*.so`, `*.exe`, `Makefile`, `config.log`, `.idea/`, `*.log`, `.env*`
- **Swift**：`.build/`, `DerivedData/`, `*.swiftpm/`, `Packages/`
- **R**：`.Rproj.user/`, `.Rhistory`, `.RData`, `.Ruserdata`, `*.Rproj`, `packrat/`, `renv/`
- **通用**：`.DS_Store`, `Thumbs.db`, `*.tmp`, `*.swp`, `.vscode/`, `.idea/`

**工具特定模式（可按需补充）**：

- **Docker**：`node_modules/`, `.git/`, `Dockerfile*`, `.dockerignore`, `*.log*`, `.env*`, `coverage/`
- **ESLint**：`node_modules/`, `dist/`, `build/`, `coverage/`, `*.min.js`
- **Prettier**：`node_modules/`, `dist/`, `build/`, `coverage/`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
- **Terraform**：`.terraform/`, `*.tfstate*`, `*.tfvars`, `.terraform.lock.hcl`
- **Kubernetes/k8s**：`*.secret.yaml`, `secrets/`, `.kube/`, `kubeconfig*`, `*.key`, `*.crt`

### 3.4 解析 `tasks.md`（Parse tasks.md）

I3 执行器需要从 `tasks.md` 中提取以下结构化信息：

- **任务阶段**：阶段 1（设置）、阶段 2（基础）、阶段 3+（用户故事）、最终阶段（打磨/横切关注点）
- **任务依赖**：
  - 显式依赖：任务描述中声明的依赖/阻塞条件（若有）
  - 故事级依赖：来自 “故事依赖关系（完成顺序）” 的 Mermaid 图
- **任务详情**：
  - 任务文本（描述）
  - 文件路径/代码范围（建议从 `（路径：\`...\`）` 提取）
  - 可选并行标记：
    - **推荐方式**：以 “并行执行示例” 段落作为并行分组提示
    - **兼容方式**：若任务描述中包含 `[P]`，视为并行候选任务（不改变必须遵守的依赖/文件冲突规则）
- **执行流程**：按阶段顺序 + 依赖拓扑 + 文件冲突串行 + TDD（见 3.5）

> 兼容性要求：`tasks.md` 模板未强制 `[P]`，因此 I3 必须同时支持 “并行执行示例” 和可选 `[P]` 标签两种提示来源。

### 3.5 执行调度（Execution scheduling）

#### 3.5.1 分阶段执行

- **阶段 1：设置**：项目结构、依赖、基础配置
- **阶段 2：基础**：阻塞性先决条件（基础库、通用模块、脚手架、通用工具链）
- **阶段 3+：用户故事**：按优先级（P1→P2→P3）推进；每个用户故事内仍遵循依赖与验证
- **最终阶段：打磨与横切关注点**：一致性、性能、可观测性、错误处理、文档补齐等

#### 3.5.2 依赖与并行规则

- **依赖关系**：
  - 任务若引用其它任务/故事作为前置，则必须等待前置完成（`- [x]`）才可开始
- **并行规则**：
  - 若任务被标记为并行候选（来自并行示例或 `[P]`），可与其它并行任务同批推进
  - 但必须同时满足：
    - 依赖已满足
    - 不涉及同一文件/同一强耦合目录（见 3.6）

#### 3.5.3 TDD 与“测试先于代码”

若 `tasks.md` 在同一阶段/故事内同时存在“测试类任务”和“实现类任务”，I3 必须优先执行测试类任务：

- **测试类任务识别（建议规则）**：描述包含 `测试/单测/集成测试/E2E/契约测试/回归/coverage` 等关键词，或路径落在 `test/`, `tests/`, `__tests__/` 等目录
- **实现类任务识别**：描述包含 `实现/开发/增加接口/新增命令/增加端点/完善逻辑` 等，或路径落在源码目录

### 3.6 基于文件的协调（File-based coordination）

为避免并行导致冲突，I3 需要维护“文件锁/目录锁”规则：

- 若两个任务涉及相同文件：必须顺序执行
- 若两个任务涉及同一强耦合目录（例如同一个模块目录）：默认顺序执行（除非 `tasks.md` 明确可并行且验证无冲突）
- 锁粒度建议：
  - 优先使用“文件路径”粒度
  - 文件路径缺失时，使用“模块目录/包目录”作为降级锁

### 3.7 按照任务计划执行实施（Execute）

对每个任务执行统一循环：

1. **前置检查**
   - 依赖是否完成？阻塞条件是否解除？
   - 任务要求的输入（文件/权限/环境）是否满足？
2. **阻塞处理**
   - 若发现 “NEEDS CLARIFICATION” 或输入缺失：停止该任务并记录
     - 缺什么
     - 如何补齐
     - 向谁取证/从哪里取证
3. **实施变更**
   - 按任务指定路径完成代码/配置/文档/脚本变更
4. **验证检查点**
   - 在进入下一阶段前，必须完成该阶段的最小验证（由 `plan.md` 与任务验收点共同决定）
5. **进度回写**
   - 任务完成后，必须把该任务标记为 `- [x]`
   - 并补充最小证据（推荐直接追加在同一行：`（证据：<commit/PR>；文件：\`...\`）`）

### 3.8 进度跟踪与错误处理（Progress & error handling）

- 完成每个任务后应报告进度（至少：已完成任务、当前阶段、剩余阻塞项）。
- **失败策略**：
  - 若任何“非并行任务”失败：停止执行并报告错误上下文（便于调试与回滚）。
  - 对“并行候选任务”：
    - 可继续推进同批中已成功的任务
    - 对失败任务必须报告：失败原因、影响范围、重试/替代方案
- 若实施无法继续：给出后续步骤（最短解阻路径），并明确需补齐的输入或决策。

### 3.9 完成验证（Completion validation）

在结束 I3 前必须完成以下验证：

- 验证 `tasks.md` 中所有必要任务均已处理：
  - 可完成项均为 `- [x]`
  - 不可继续项必须在原任务处标注阻塞原因与取证路径（不得静默跳过）
- 核对实现结果是否符合原始规范：
  - 与 `plan.md` 的技术栈/架构/文件结构一致
  - 与 `requirements/prd.md` 或 `requirements/solutions.md` 的关键 AC 对齐（按需抽样或全量）
- 验证检查点通过：
  - 构建/静态检查/测试（具体由 `plan.md` 与任务定义决定）
- 确认 Spec 阶段未修改 `project/*`：
  - 若产生可复用 ADR/契约：已在 `{FEATURE_DIR}/design/` 内草拟，并已列入 merge-back 晋升清单（在 `tasks.md` 或 `{FEATURE_DIR}/merge_back.md`）

---

## 4. 输出与回写规范（tasks.md）

- I3 的状态回写只允许：
  - 将任务从 `- [ ]` 改为 `- [x]`
  - 为任务补充证据文本（不改变章节结构与编号）
  - 补充阻塞说明（NEEDS CLARIFICATION + 影响 + 取证路径）
- 禁止在 I3 中把 `tasks.md` 重写为另一种结构（否则影响可审计与后续解析）。

---

## 5. 质量门槛（I3-DoD）

- [ ] `implementation/tasks.md` 已完整回写执行状态（完成项 `- [x]`，且有最小证据）
- [ ] 执行顺序遵循阶段与依赖，且对并行提示与文件冲突做了约束
- [ ] 各阶段验证检查点完成（构建/测试/静态检查等以 `plan.md` 与任务验收点为准）
- [ ] 阻塞项均已记录（NEEDS CLARIFICATION + 影响 + 取证路径）
- [ ] Spec 阶段未更新 `project/*`；需晋升的资产已在 Spec 内草拟并列入 merge-back 待办
