### 支持 SDLC Spec Coding 的项目知识库

让团队“以 Spec 为单一事实源（SSOT）”成为默认行为，显著降低返工与沟通成本，提高AI辅助研发的效率和质量。

背景：
* 各个团队都在不同工具、不同程度在实施 AI 辅助开发
* SDLC各个阶段，缺乏高质量的输入，AI辅助的质量效果不佳

---

### 1. 核心理念：双层 SSOT（需求 SSOT + 项目 SSOT）

* **SSOT（Single Source of Truth）**：单一事实源，确保信息一致性的原则
* **Spec as Code**：将 Spec 文档当做项目代码一样对待及维护，遵循版本控制、代码审查、持续更新等工程化实践

SDD 在项目里最常见的问题是：需求多、文档缺少、文档过时、碎片化，导致"无全局"、"全局失焦"。解决办法是建立**双层 SSOT**，并践行 **Spec as Code** 理念：

- **项目级 SSOT（Project Spec Set）**：项目维度的长期事实源：Roadmap、架构、对外契约、数据口径、运行手册、NFR 预算、风险清单等。通过版本控制、代码审查确保文档与代码同步演进，避免文档过时。
- **需求级 SSOT（Spec Pack）**：每个需求有自己的"Spec 包"，覆盖该需求从 PRD 到发布的闭环产物与证据。每个 Spec 文档都纳入版本控制，变更通过 PR/MR 评审，确保文档质量与可追溯性。

二者关系：
- **项目 Spec Set 是长生命周期、强治理**（以资产与运营为中心）：通过持续更新与版本管理，形成项目的长期知识资产
- **需求 Spec Pack 是短生命周期、强时效**（以交付为中心）：围绕交付闭环，文档随代码一起演进，避免文档与实现脱节
- 需求完成后，按规则把可复用资产从需求层"晋升"到项目层（见第 6 节），并通过版本控制记录完整的演进历史

---

### 1.1 可行性分析

SDLC Spec Coding 在当前时机具备良好的可行性，主要体现在以下几个方面：

#### 1.1.1 理论基础成熟

* **软件工程理论支撑**：软件工程领域已有成熟的理论基础，强调文档化、可追溯性、过程改进等核心原则
* **过程改进框架验证**：CMMI、ISO/IEC 15504 等过程改进框架已验证了规范化文档管理对项目质量提升的有效性
* **实践案例丰富**：业界已有大量成功案例证明 Spec 驱动开发能够显著减少返工、提升协作效率

#### 1.1.2 AI 辅助降低执行成本

* **AI 降低文档编写成本**：AI 辅助工具可以自动生成文档框架、填充模板、检查完整性，大幅降低文档编写和维护的成本
* **AI 提升文档质量**：AI 可以检查文档一致性、可追溯性、完整性，帮助发现遗漏和矛盾
* **人机分工优化**：AI 承担繁琐的执行细节（文档生成、格式检查、链接维护），人的工作聚焦于**决策、评审、质量保障**等核心价值活动

#### 1.1.3 技术条件成熟

* **版本控制普及**：Git 等版本控制系统已成为标准实践，为 Spec as Code 提供基础设施
* **文档即代码工具链**：Markdown、Mermaid、PlantUML 等工具让文档可以像代码一样管理
* **自动化能力增强**：CI/CD 可以自动检查文档完整性、生成文档索引、验证契约一致性

#### 1.1.4 组织需求迫切

* **AI 辅助开发普及**：各团队都在不同程度实施 AI 辅助开发，但缺乏高质量输入导致效果不佳
* **知识资产沉淀需求**：团队希望将项目知识沉淀下来，避免重复踩坑，提升长期效率

#### 1.1.5 渐进式落地可行

* **最小集启动**：可以从最小集（Spec Pack + Registry + Merge-back）开始，逐步完善
* **按需裁剪**：根据需求复杂度进行文档裁剪，避免过度文档化
* **工具链可逐步建设**：从手动维护到自动化，可以分阶段演进（L1 → L2 → L3）

> **结论**：SDLC Spec Coding 在当前时机具备良好的可行性。理论基础成熟、AI 辅助降低执行成本、技术条件成熟、组织需求迫切，且可以渐进式落地，风险可控。

### 2. 文档与目录结构（推荐：仓库即事实源）

建议在项目仓库内建立统一目录（示例）：

```text
ssd/
  template/
    index.md
    gateway
  project/                     # 项目级 SSOT（长期资产）
    index.md                   # 项目总览入口（项目视角 Dashboard）
    roadmap.md                 # 路线图/里程碑/发布车道
    nfr.md                     # NFR 预算与目标（SLO/性能/成本/安全/合规）
    architecture/              # 架构资产（稳定）
      product.md               # 定义项目的业务上下文（Why & What），产品愿景与目标用户，业务约束与成功指标；
      tech.md                  # 定义项目的技术上下文（How），技术栈（语言、框架、数据库），开发原则（如 TDD、代码风格）
      structure.md             # 定义项目的结构上下文（Where），项目目录结构树、模块组织规则
      adr/                     # ADR 索引与归档
    contracts/                 # 对外契约资产（稳定）
      api/                     # OpenAPI/AsyncAPI/GraphQL schema（或链接）
      data/                    # 数据字典/口径/Schema/质量规则
      ux/                      # 关键流程/信息架构/组件规范（如适用）
    ops/                       # 运行资产（稳定）
      runbook.md               # 运行手册（总览）
      release.md               # 发布策略/回滚策略/灰度规范
      monitoring.md            # 指标/告警/看板索引
    decisions.md               # 重要决策摘要（链接到 ADR）
    glossary.md                # 术语表（可与 spec.md 附录对齐）

  demands/                     # 需求级 SSOT（短生命周期 Spec Pack）
    DEMO-0001-feature-x/       # 一个需求/故事/史诗的 Spec Pack
      index.md                 # 该需求入口（状态、链接、证据）
      changelog.md              # 需求内变更记录（可选，或写在各文档内）
      merge_back.md             # 合并回项目层的清单与状态（见第 6 节）
      requirements/             # 需求阶段（Discovery & Requirements）
        raw.md                  # 原始需求（用户反馈/工单/业务需求等）
        prd.md                  # 或 brd_prd.md（按团队习惯）
      design/                   # 方案设计阶段（Solution Design）
        research.md             # 方案研究（如有）
        design.md               # 差量设计 / HLD/LLD 合并或拆分
        api.md                  # 契约变化（如有）
        data.md                 # 数据变化（如有）
        ux.md                   # 交互变化（如有）
      implementation/           # 开发阶段（Implementation）
        plan.md                 # 实施计划
        tasks.md                # 任务清单
      verification/             # 测试阶段（Verification/QA）
        test_plan.md            # 测试计划与覆盖矩阵
        test_cases.md           # 测试用例文档（用例集）
      release/                  # 发布与运维阶段（Release & Ops）
        release.md              # 本需求的发布/灰度/回滚与验证
        evidence.md             # 证据（测试报告/截图/指标链接）
```

目录设计要点：
- **项目层**放“稳定且需要长期维护的事实源”（架构、契约、运行资产、术语、NFR 预算）。
- **需求层**放“围绕交付闭环的差量文档与证据”，完成后可归档但可追溯。

---

### 3. 需求 Spec Pack 的统一元信息（让并行可治理）

每个需求 `demands/<ID>/index.md` 必须包含（建议表格）：

- **需求 ID / 标题 / 类型**：Feature / Refactor / POC / Site / Tool
- **状态**：Draft → In Review → Approved(DoR) → In Dev → In QA → Released → Merged & Archived
- **Owner/RACI**：产品 Owner、技术 Owner、QA Owner、发布 Owner
- **目标与 AC**：链接到 PRD 关键段落
- **关键契约**：API/Data/UX Delta 的链接与版本
- **风险与依赖**：P0/P1 + 缓解措施
- **发布车道**：目标发布窗口/版本/灰度策略
- **证据**：测试报告/监控看板/发布记录
- **Merge-back 状态**：哪些资产要合并回项目层（见第 6 节）

> 这样做的结果：即使需求多、并行多，项目负责人只看每个 `index.md` 就能掌握全局。

---

### 4. 项目级视角：Spec Registry（总览索引）是关键

建议在 `ssd/project/index.md` 维护一个 **Spec Registry（登记表）**，它是项目层的“控制面板”：

- **需求列表**：ID、标题、状态、Owner、目标发布窗口
- **契约变更列表**：
  - API：新增/变更/弃用，版本号与依赖方
  - Data：Schema/口径变化，迁移状态
  - UX：关键流程变化（对用户可见）
- **NFR 预算与消耗**：关键链路 SLO、性能预算、成本预算、容量评估
- **风险雷达**：P0/P1 风险、阻塞依赖、未决问题
- **发布车道**：每个发布窗口包含哪些需求、灰度与回滚计划

Registry 的价值：让“需求级并行推进”不会破坏“项目级一致性”，尤其在契约与 NFR 上。

---

### 5. 需求 Spec Pack 生命周期

每个需求（Spec Pack）从创建到归档的完整生命周期，遵循 SDLC 流程，并在关键点与项目层对齐：

#### 5.1 创建（Create）- 状态：Draft
- 创建 `demands/<ID>/` 目录结构（按 SDLC 阶段组织：requirements/、design/、implementation/、verification/、release/）
- 创建 `index.md`，初始化需求元信息（ID、标题、类型、Owner、状态等）
- 明确需求类型（Feature/Refactor/POC/Site/Tool）并选用对应裁剪标准
- 创建 `requirements/raw.md` 记录原始需求输入

#### 5.2 需求分析（Requirements）- 状态：Draft → In Review
- 编写 `requirements/prd.md`：明确问题、目标、范围、AC、业务规则
- 完成需求评审，确保 AC 可测试、可观测
- 更新 `index.md` 状态为 `In Review`

#### 5.3 方案设计（Design）- 状态：In Review → Approved(DoR)
- 编写 `design/research.md`：技术调研、方案对比（如有）
- 编写 `design/design.md`：HLD/LLD、架构方案、关键决策
- 编写契约文档（如有）：
  - `design/api.md`：API 契约变化（必须先行并冻结版本）
  - `design/data.md`：数据模型/口径变化
  - `design/ux.md`：交互流程变化
- 完成设计评审，达到 DoR（范围冻结、验收可执行、依赖可用、风险可控）
- 更新 `index.md` 状态为 `Approved(DoR)`

#### 5.4 开发实现（Implementation）- 状态：In Dev
- 编写 `implementation/plan.md`：实施计划、任务拆分、开关策略、回滚方案
- 编写 `implementation/tasks.md`：任务清单、进度跟踪
- **契约先行**：若契约已冻结，则以 Mock/Schema/契约测试为约束推进
- 代码实现与 Spec 文档同步更新（践行 Spec as Code）
- 更新 `index.md` 状态为 `In Dev`

#### 5.5 测试验证（Verification）- 状态：In QA
- 编写 `verification/test_plan.md`：测试策略、覆盖矩阵、环境与数据
- 编写 `verification/test_cases.md`：测试用例集，关联到 PRD 的 AC
- 执行测试，生成测试报告
- 更新 `verification/evidence.md`：测试报告、截图、指标链接
- 更新 `index.md` 状态为 `In QA`

#### 5.6 发布上线（Release）- 状态：Released
- 编写 `release/release.md`：发布步骤、灰度策略、回滚计划、监控告警
- 执行发布，按灰度策略逐步放量
- 更新 `release/evidence.md`：发布记录、监控指标、验证结果
- 更新 `index.md` 状态为 `Released`

#### 5.7 合并沉淀（Merge-back）- 状态：Merged & Archived
- 执行"合并回项目层"的清单（见第 6 节）：
  - ADR 归档到项目层
  - 契约更新到项目层 contracts/
  - 运行资产更新到项目层 ops/
  - NFR 预算更新到项目层 nfr.md
- 更新 `merge_back.md` 记录合并状态
- 更新 Registry 中需求状态为 `Merged`
- 更新 `index.md` 状态为 `Merged & Archived`（保留可追溯）

---

### 6. 合并回项目层（Merge-back）：把短期交付变成长期资产

需求完成后，不应把所有文档“全拷贝”到项目层，而是按资产类型**筛选晋升**：

#### 6.1 必须合并回项目层的内容（默认）
- **ADR**：任何关键决策必须进入 `project/architecture/adr/` 并在 `project/decisions.md` 汇总
- **对外契约**：
  - API：若有变更，更新 `project/contracts/api/`（或链接到 Schema 文件），并更新弃用策略
  - Data：若有变化，更新 `project/contracts/data/`（字典/口径/质量规则）与迁移结论
  - UX：关键流程/信息架构变更，更新 `project/contracts/ux/`（如适用）
- **运行资产**：上线相关 Runbook/监控告警/回滚策略，更新 `project/ops/`
- **NFR 预算与基线**：若对性能/稳定性/成本有影响，更新 `project/nfr.md`（预算、现状、目标）

#### 6.2 可选合并（视团队习惯）
- 复杂模块的 LLD（若未来维护者需要）
- 通用组件/库的设计规范
- 重要测试策略（如契约测试标准、回归策略变化）

#### 6.3 Merge-back 的执行方式（推荐）
在每个需求 `merge_back.md` 里维护清单（Done/Not Done）：
- ADR 是否已归档到项目层
- API/Data/UX 是否已更新到项目层契约目录
- Runbook/监控是否已更新到项目层
- NFR 预算是否更新
- Registry 是否更新需求状态为 Released / Merged

> Merge-back 是“需求真正完成”的一部分，建议纳入 DoD。

---

### 7. 变更管理与版本策略（项目级）

项目级变更管理与 `spec.md` 第 6 节一致，但多一个要求：**变更既要落到需求层，也要同步项目层**。

- **需求内变更**：在需求 Spec Pack 的文档里更新版本与 Changelog（并引用变更单/ADR）
- **项目层同步**：只要影响“项目长期资产”（架构/契约/运行/NFR），必须同步更新项目层对应文件，并在 Registry 记录“变更影响面”

建议统一版本口径：
- 契约类（API/Data）：语义化版本（major/minor/patch）+ 弃用期
- 需求 Spec：可用 `v0.x`（迭代中）→ `v1.0`（发布冻结）

---

### 8. 需求颗粒度与文档裁剪策略

由于需求大小、复杂度、影响范围不同，并非所有需求都需要完整的 Spec Pack。应根据需求颗粒度进行**文档裁剪**，但必须明确"缺省不产出"的理由与替代品。

#### 8.1 需求颗粒度分类

根据需求的影响范围、技术复杂度、业务复杂度，可将需求分为三类：

- **简单需求（Simple）**：影响范围小、技术方案明确、无外部依赖、无数据迁移、无架构变更
  - 示例：UI 文案调整、简单配置项、Bug 修复、小功能优化
- **中等需求（Medium）**：有一定复杂度、涉及部分模块、有外部依赖或数据变更、需要设计评审
  - 示例：新增功能模块、API 接口变更、数据模型调整、流程优化
- **复杂需求（Complex）**：影响范围大、技术方案复杂、涉及架构变更、多系统协作、有数据迁移
  - 示例：核心功能重构、架构升级、跨系统集成、大规模数据迁移

#### 8.2 文档裁剪策略

**核心原则**：简单需求可以跳过中间产物，但必须保留**关键节点文档**；复杂需求必须完整产出。

##### 简单需求的文档裁剪（最小集）

**必须保留的文档**：
- `index.md`：需求入口（状态、Owner、AC、证据）
- `requirements/prd.md`：需求文档（可简化，但必须包含 AC）
- `verification/test_cases.md`：测试用例（至少覆盖核心 AC）
- `release/release.md`：发布步骤（可简化）

**可跳过的文档**（需在 `index.md` 中说明理由）：
- `requirements/raw.md`：原始需求简单明确，直接写入 PRD
- `design/research.md`：技术方案成熟，无需调研
- `design/api.md`、`design/data.md`、`design/ux.md`：无契约变化，或变化已在 `design/design.md` 中说明
- `design/design.md`：方案简单，在 PRD 或 Implementation Plan 中已说明
- `implementation/plan.md`：任务简单，在 `index.md` 或任务系统已跟踪
- `verification/test_plan.md`：测试范围明确，用例已覆盖
- `release/evidence.md`：证据简单，直接记录在 `release/release.md` 中

**替代方案**：
- 简单设计 → 在 PRD 中补充"技术方案"章节
- 简单测试 → 在 `test_cases.md` 中补充"测试策略"说明
- 简单发布 → 在 `release.md` 中补充"发布验证"清单

##### 中等需求的文档裁剪（标准集）

**必须保留的文档**：
- `index.md`：需求入口
- `requirements/prd.md`：需求文档
- `design/design.md`：设计文档（HLD 或简化版）
- 契约文档（如有变化）：`design/api.md`、`design/data.md`、`design/ux.md` 至少一个
- `implementation/plan.md`：实施计划
- `verification/test_plan.md`：测试计划
- `verification/test_cases.md`：测试用例
- `release/release.md`：发布文档

**可跳过的文档**：
- `requirements/raw.md`：原始需求已整理到 PRD
- `design/research.md`：技术方案成熟，无需深度调研（但需在 `design/design.md` 中说明选型理由）
- `implementation/tasks.md`：任务在项目管理工具中跟踪
- `release/evidence.md`：证据在测试报告或监控系统中

##### 复杂需求的文档要求（完整集）

**必须完整产出**所有阶段的文档，包括：
- 需求阶段：`raw.md`、`prd.md`
- 设计阶段：`research.md`、`design.md`、契约文档（`api.md`/`data.md`/`ux.md`）
- 实现阶段：`plan.md`、`tasks.md`
- 测试阶段：`test_plan.md`、`test_cases.md`
- 发布阶段：`release.md`、`evidence.md`

#### 8.3 裁剪决策原则

**判断标准**：
1. **影响范围**：是否影响外部系统、用户、数据？影响范围越大，文档越完整
2. **技术风险**：是否有技术不确定性、架构变更、性能风险？风险越高，文档越详细
3. **协作复杂度**：是否需要多团队协作、前后端分离、跨系统联调？协作越多，契约文档越重要
4. **可追溯性要求**：是否需要长期维护、审计、知识传承？要求越高，文档越完整

**裁剪记录**：
- 在 `index.md` 中明确标注：哪些文档已跳过，理由是什么，替代方案是什么
- 建议使用表格记录文档状态：`Required` / `Optional` / `Skipped (Reason: xxx)`

#### 8.4 裁剪示例

**示例 1：简单需求 - UI 文案调整**
```
跳过文档：design/、implementation/plan.md、verification/test_plan.md
保留文档：index.md、requirements/prd.md（简化版）、verification/test_cases.md、release/release.md（简化版）
理由：无技术变更、无契约变化、测试简单
```

**示例 2：中等需求 - 新增 API 接口**
```
跳过文档：requirements/raw.md、design/research.md、implementation/tasks.md
保留文档：index.md、requirements/prd.md、design/design.md、design/api.md、implementation/plan.md、verification/test_plan.md、verification/test_cases.md、release/release.md
理由：有契约变化，需要完整的设计和测试，但技术方案成熟
```

**示例 3：复杂需求 - 核心模块重构**
```
完整产出：所有阶段文档
理由：影响范围大、技术风险高、需要长期维护和知识传承
```

> **重要提醒**：文档裁剪不等于"不写文档"，而是根据需求复杂度选择合适的文档粒度。即使是最简单的需求，也必须保留 `index.md`、`prd.md`（含 AC）、`test_cases.md` 和 `release.md`，确保可追溯、可验收。

## 术语表

### 核心概念

- **SDD（Spec Driven Development）**：规范驱动开发，本文档体系的核心方法论
- **SSOT（Single Source of Truth）**：单一事实源，确保信息一致性的原则
- **Spec Pack（Specification Pack）**：需求规格包，单个需求从 PRD 到发布的完整闭环产物与证据集合
- **Project Spec Set**：项目规格集，项目维度的长期事实源（架构、契约、运行资产等）
- **Spec Registry**：规格登记表，项目层的控制面板，用于追踪需求、契约变更、发布车道和风险

### 文档类型

- **PRD（Product Requirements Document）**：产品需求文档
- **BRD（Business Requirements Document）**：业务需求文档
- **HLD（High-Level Design）**：高层设计
- **LLD（Low-Level Design）**：低层设计
- **ADR（Architecture Decision Record）**：架构决策记录，记录重要的架构决策及其上下文
- **Runbook**：运行手册，包含系统运维、故障处理等操作指南

### 需求与质量

- **NFR（Non-Functional Requirements）**：非功能性需求，包括性能、稳定性、安全性、合规性等
- **SLO（Service Level Objective）**：服务级别目标，用于衡量服务质量的具体指标
- **AC（Acceptance Criteria）**：验收标准，需求完成的可验证条件
- **DoR（Definition of Ready）**：就绪定义，需求可以开始开发的前置条件
- **DoD（Definition of Done）**：完成定义，需求被认为完成的标准

### 项目管理

- **RACI**：责任分配矩阵（Responsible, Accountable, Consulted, Informed），用于明确角色职责
- **Roadmap**：路线图，项目的时间规划和里程碑
- **Dashboard**：仪表板/控制面板，项目总览的可视化界面
- **发布车道（Release Lane）**：发布计划中的不同发布路径或版本线
- **发布窗口（Release Window）**：计划进行发布的时间窗口
- **灰度（Gray Release）**：灰度发布，逐步向用户开放新功能的发布策略
- **回滚（Rollback）**：回滚策略，当发布出现问题时恢复到之前版本的操作

### 技术术语

- **契约（Contract）**：系统间或系统与外部交互的约定，包括 API 契约、数据契约、UX 契约
- **Delta**：差量/增量，相对于现有系统的变更部分
- **Schema**：数据模式/结构定义，描述数据的格式和约束
- **OpenAPI**：开放 API 规范，用于描述 RESTful API 的标准格式
- **AsyncAPI**：异步 API 规范，用于描述消息驱动的 API
- **GraphQL**：图形查询语言，一种 API 查询语言
- **Mock**：模拟/模拟数据，用于开发和测试的假数据或服务

### 流程与状态

- **SDLC（Software Development Life Cycle）**：软件开发生命周期
- **Merge-back**：合并回项目层，将需求完成后的可复用资产晋升到项目层的过程
- **Changelog**：变更日志，记录文档或系统的变更历史
- **证据（Evidence）**：证明需求完成的可验证材料，如测试报告、监控指标、截图等

### 优先级与风险

- **P0/P1**：优先级标识，P0 为最高优先级，P1 次之，用于风险与依赖的分类


