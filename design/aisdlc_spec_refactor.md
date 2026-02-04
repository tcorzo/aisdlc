---
title: Spec 级重构阶段（Refactor）SOP（输出 澄清 + 基线，进入通用 Design/Impl 流程）
status: draft
audience: [PM, BA, DEV, QA, SRE]
principles_ref: design/aisdlc.md
related_refs:
  - design/aisdlc_spec_init.md
  - design/aisdlc_spec_product.md
  - design/sdlc_spec_coding.md
---

# 重构阶段（Refactor）流程

## 1. 背景与目标（对齐 `design/aisdlc.md`）

本方案用于 **Spec 级** 的“重构阶段（Refactor）”提效：在遵循“双层 SSOT + Spec as Code + 渐进式披露”的前提下，用 **R0~R2** 的最小闭环，把一次重构从“想改一改”稳定推进到可进入后续执行块的状态。

本方案只定义 **Refactor 块**，后续执行块将复用通用 SOP（不在本方案重复定义）：

- **design**：复用 `design/sdlc_spec_coding.md` 的 Design 阶段（从 `design/research.md` 开始）
- **impl / verification / release / merge-back**：同样复用 `design/sdlc_spec_coding.md`

### 1.1 这套 Refactor 块解决什么问题

重构最常见失败模式是：

- **目标/边界漂移**：做着做着变成改需求、改行为、改契约
- **无法证明变好**：没有基线与指标口径，重构后争论不休
- **不可回滚/止损**：缺少回滚点与止损条件，导致风险失控

因此 Refactor 块的核心目标是把“做什么”说清楚，并把“进入后续设计/开发”的门槛做成可检查清单。

### 1.2 本块产物（最小闭环）

- `requirements/raw.md`：原始输入与证据入口（R0，复用 `spec-init`）
- `refactors/clarify.md`：重构澄清（R1）
- `refactors/baseline.md`：现状与基线（R2，末尾包含“进入 design 块的 DoR 清单”）

---

## 2. 产物落盘与“渐进式披露”读取顺序

### 2.1 建议落盘结构（需求级 Spec Pack）

对齐 `design/aisdlc.md` 的 Spec Pack 目录约定，并在需求级新增 `refactors/`（仅作为 Refactor 块产物目录）：

```text
.aisdlc/specs/<DEMAND-ID>/
  index.md
  requirements/
    raw.md                       # R0：原始重构输入（证据入口）
  refactors/
    clarify.md                   # R1：重构澄清（不变量/允许变化点/范围/风险）
    baseline.md                  # R2：现状与基线（影响面/指标口径/回滚止损/DoR）
  design/                        # 后续块：复用通用 SOP（从 design/research.md 开始）
  implementation/
  verification/
  release/
  merge_back.md
```

> 说明：`refactors/` 是为了把“做什么”的输入与后续执行块的产物解耦，从而稳定复用 `design/sdlc_spec_coding.md` 的 design/impl/... 流程。

### 2.2 Agent 读取顺序（渐进式披露）

- **必读（项目级）**：优先读项目级 `memory/`（业务、技术、结构、术语）与 contracts/adr 索引，避免不必要的口径与约束错误。
- **按需（当前 Spec Pack）**：仅当任务明确指向某个 `<DEMAND-ID>` 时，读取该需求的：
  - `requirements/raw.md`（证据入口）
  - `refactors/clarify.md`（重构澄清）
  - `refactors/baseline.md`（现状与基线，含 DoR）
- **进入 design 块后**：在 DoR 满足时，按通用 SOP 读取/产出 `design/*`、`implementation/*` 等。

---

## 3. 模块化流程总览（R0~R2）

> 原则：一个模块 = 一个目标 = 一个落盘产物；每步都有门禁与 DoD。

- **R0 Spec 初始化（复用 `spec-init`）**
  - **目标**：建立需求上下文（分支+目录），落盘原始重构需求
  - **输出**：`requirements/raw.md`
  - **下一步**：R1
- **R1 重构澄清（Clarify）**
  - **目标**：把“为什么重构/重构范围/不变量/允许变化点/约束/风险”说清楚
  - **输出**：`refactors/clarify.md`
  - **下一步**：R2
- **R2 现状审计与基线（Baseline）**
  - **目标**：固化 As-Is 与影响面，建立可验证基线，给出回滚止损点与进入 design 的 DoR
  - **输出**：`refactors/baseline.md`
  - **下一步**：进入 design 块（复用通用 SOP）

---

## 4. 模块 R0：Spec 初始化（复用 `design/aisdlc_spec_init.md`）

### 4.1 目标

输入重构的原始需求，创建并切换到 `{num}-{short-name}` 分支，生成对应 Spec Pack 目录，并将原始需求落盘到：

- `{FEATURE_DIR}/requirements/raw.md`

### 4.2 下一步（R0 → R1）

执行完 R0 后进入 R1，开始澄清“重构到底要解决什么、哪些必须不变”。

---

## 5. 模块 R1：重构澄清（输出 `refactors/clarify.md`）

### 5.1 输入

- `{FEATURE_DIR}/requirements/raw.md`（必须）
-（可选）项目级 `memory/*` 与相关 contracts/adr（用于口径与约束对齐）

### 5.1.1 命令与模板（可选，但推荐）

- **命令**：`spec-refactor-clarify`（见 `.aisdlc-cli/commands/spec-refactor-clarify.md`）
- **模板**：`.aisdlc-cli/templates/spec/refactor-clarify-template.md`

### 5.2 输出（落盘到 `refactors/clarify.md`）

最小结构建议（模板骨架见第 8 节）：

- 一句话结论（TL;DR）
- 目标与非目标（In/Out）
- 现状痛点与动机（为什么要重构）
- **不变量（Must Not Change）**：外部契约/关键行为/数据口径/安全合规底线/关键 NFR 护栏
- **允许变化点（May Change）**：哪些内部实现/结构/依赖/数据表/接口形态允许调整（以及边界）
- 约束与依赖（时间、人、系统、合规）
- 风险与待确认问题（仅列关键问题，避免无穷追问）

### 5.3 门禁（R1 MUST）

- 必须显式写出“不变量”与“允许变化点”；缺信息允许写“未知/待确认”，但不得跳过。
- 必须写清 In/Out，否则后续 baseline 与设计不可控。

### 5.4 质量门槛（R1-DoD）

- 读完 `clarify.md`，任何参与者都能复述：
  - 为什么重构（动机/痛点/目标）
  - 做什么不做什么（In/Out）
  - 什么必须不变（不变量清单）
  - 哪些允许变化（允许变化点清单）

---

## 6. 模块 R2：现状审计与基线（输出 `refactors/baseline.md`）

### 6.1 输入

- `{FEATURE_DIR}/requirements/raw.md`（证据入口）
- `{FEATURE_DIR}/refactors/clarify.md`（必须）
-（按需）现有代码结构/依赖/运行指标入口（链接即可，不要求在本阶段补齐所有细节）

### 6.1.1 命令与模板（可选，但推荐）

- **命令**：`spec-refactor-baseline`（见 `.aisdlc-cli/commands/spec-refactor-baseline.md`）
- **模板**：`.aisdlc-cli/templates/spec/refactor-baseline-template.md`

### 6.2 输出（落盘到 `refactors/baseline.md`）

最小结构建议（模板骨架见第 8 节）：

- As-Is：当前架构/模块边界/关键链路（只写与本次重构相关的部分）
- 影响面：代码模块、接口契约、数据契约、运行资产、NFR（按适用项填写）
- **基线（至少 1 个可验证）**：当前指标 + 口径 + 数据源链接 + 采样窗口
- 回归范围建议：哪些能力/接口/场景必须回归验证（与不变量对齐）
- 风险登记与待验证假设：进入 design 后需要做的 PoC/验证清单
- 初稿回滚点/止损条件：出现什么信号必须回滚或暂停
- **进入 design 块的 DoR 清单（强制收口）**：见 6.4

### 6.3 门禁（R2 MUST）

- 必须给出至少 **1 个可验证基线**（性能/成本/错误率/稳定性/一致性等选择最相关的一个）
- 必须给出回滚/止损的“可执行初稿”（允许不完整，但必须可讨论、可落盘）

### 6.4 进入 design 块的 DoR 清单（作为 baseline.md 最后一节）

- 范围冻结：In/Out 与“允许变化点”已定稿
- 不变量冻结：契约/关键行为/数据口径/安全合规底线已列出
- 基线可度量：至少 1 个基线可复现/可采样/有口径与数据源
- 风险可操作：Top 风险与待验证假设已登记，并形成后续 PoC/验证清单
- 回滚可定义：止损条件与回滚点初稿已写出

当上述 DoR 满足，即可进入 design 块，复用通用 SOP 产出 `design/research.md` 等后续产物。

---

## 7. 与后续块的复用边界（关键说明）

本方案只负责回答“做什么”。后续块负责回答“怎么做/怎么验证/怎么上线/怎么沉淀”，其流程与产物复用：

- `design/sdlc_spec_coding.md` 的 Design/Implementation/Verification/Release/Merge-back
- `design/aisdlc.md` 的 Merge-back 规则（ADR/契约/ops/NFR/registry 等晋升）

---

## 8. 附：产物模板骨架（最小可用）

### 8.1 `refactors/clarify.md`（R1）

```markdown
---
title: 重构澄清（Clarify）
status: draft
stage: refactor
module: R1
principles_ref: design/aisdlc.md
source_refs:
  - requirements/raw.md
---

## 0. 一句话结论（TL;DR）

## 1. 目标与非目标（In/Out）

## 2. 为什么要重构（动机/痛点/收益）

## 3. 不变量（Must Not Change）
- 契约/API：
- 数据口径/一致性：
- 安全/合规：
- 关键行为/用户体验：
- 关键 NFR 护栏（性能/稳定性/成本）：

## 4. 允许变化点（May Change）

## 5. 约束与依赖

## 6. 风险与待确认问题

## 7. 追溯链接（Evidence & References）
```

### 8.2 `refactors/baseline.md`（R2）

```markdown
---
title: 现状与基线（Baseline）
status: draft
stage: refactor
module: R2
principles_ref: design/aisdlc.md
source_refs:
  - requirements/raw.md
  - refactors/clarify.md
---

## 0. 一句话结论（TL;DR）

## 1. As-Is 现状（仅与本次重构相关）

## 2. 影响面（Impact）
- 代码模块/边界：
- API/对外契约：
- 数据模型/迁移：
- 运行与配置：
- NFR（性能/稳定性/安全/成本）：

## 3. 基线（至少 1 个可验证）
- 指标：
- 当前值：
- 口径/计算方式：
- 数据源/链接：
- 采样窗口：

## 4. 回归范围建议（与不变量对齐）

## 5. 风险登记与待验证假设（进入 design 的 PoC/验证清单）

## 6. 回滚点与止损条件（初稿）

## 7. 进入 design 块的 DoR 清单（必须满足后才能进入）
- 范围冻结：
- 不变量冻结：
- 基线可度量：
- 风险可操作：
- 回滚可定义：

## 8. 追溯链接（Evidence & References）
```

