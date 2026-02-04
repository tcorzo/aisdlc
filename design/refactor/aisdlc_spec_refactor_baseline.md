---
title: R2 现状与基线（Baseline）— 影响面审计与 DoR 收口设计规范
status: draft
stage: refactor
module: R2
principles_ref: design/aisdlc.md
source_refs:
  - design/aisdlc_spec_refactor.md
  - design/refactor/aisdlc_spec_refactor_clarify.md
  - design/sdlc_spec_coding.md
  - .aisdlc-cli/commands/spec-refactor-baseline.md
  - .aisdlc-cli/templates/spec/refactor-baseline-template.md
---

## 0. 目标与定位

本设计文档用于定义 Refactor 阶段模块 R2「现状与基线」的**框架性规则、硬约束与验收标准**，用于约束后续可能的命令/模板实现，以及指导人工/AI 产物生成。

R2 的目标是把 R1 的“澄清结论”变成可执行的进入 design 块输入：把 As-Is 与影响面说清楚，建立最小可验证基线，并给出回滚止损初稿与 DoR 收口清单。

输出稳定落盘到：

- `{FEATURE_DIR}/refactors/baseline.md`

---

## 1. 术语与接口

### 1.1 上下文与路径

- **FEATURE_DIR**：由 `Get-SpecContext` 自动获取，定位到 `.aisdlc/specs/{num}-{short-name}/`
- **必读输入**：
  - `{FEATURE_DIR}/requirements/raw.md`
  - `{FEATURE_DIR}/refactors/clarify.md`
- **输出**：`{FEATURE_DIR}/refactors/baseline.md`

### 1.2 必读材料（最小必要读取）

- `refactors/clarify.md`（不变量/允许变化点/范围边界）
-（按需）现状代码结构、依赖拓扑、运行指标/日志/链路追踪入口（只需要链接入口，不要求在本阶段把所有数据复制进文档）

---

## 2. 强制门禁（MUST）

- **必须给出至少 1 个可验证基线**（选择最相关的一个即可）：
  - 性能（p95/p99 延迟、吞吐、队列堆积）
  - 稳定性（错误率、超时率、重试/熔断触发）
  - 成本（CPU/内存/存储/带宽、云成本、第三方调用成本）
  - 一致性/正确性（数据差异率、对账差异、幂等冲突率）
  - 安全（拦截命中率、告警数量、审计事件）
  - 其它与本次重构动机强相关的指标
- **必须给出回滚点与止损条件初稿**（可粗，但必须可执行/可讨论）。
- **必须完成影响面审计**：至少覆盖与本次重构相关的“代码模块 + 契约/数据/运行/NFR”中的适用项；不适用必须写“无影响 + 证据入口”。
- **全程使用中文**。

---

## 3. 输出结构（`refactors/baseline.md` 最小骨架）

建议至少包含：

- **TL;DR**：当前现状的关键结论与最大风险
- **As-Is 现状**（仅与本次重构相关）：模块边界、关键链路、主要依赖
- **影响面（Impact）**：
  - 代码模块/目录/组件
  - API/对外契约（若无变化：写“无变化声明 + 证据入口”）
  - 数据模型/数据口径/迁移（若无：写“无变化声明 + 证据入口”）
  - 运行与配置（开关、灰度、回滚路径、监控入口）
  - NFR（性能/稳定性/安全/成本）受影响点
- **基线（至少 1 个可验证）**：指标、当前值、口径、数据源、采样窗口
- **回归范围建议**：与 R1 不变量逐条对应（至少列出“必须回归的场景/接口/作业”）
- **风险登记与待验证假设**：进入 design 块要做的 PoC/验证清单
- **回滚点与止损条件（初稿）**
- **进入 design 块的 DoR 清单（最后一节，强制收口）**
- **追溯链接**：raw、监控看板、日志、链路、相关 ADR/契约等

---

## 4. 进入 design 块的 DoR 清单（baseline.md 最后一节必须包含）

DoR 的目标是让“是否可以进入 design 块”变成可检查门禁。

- **范围冻结**：In/Out 与允许变化点已定稿（与 R1 一致）
- **不变量冻结**：契约/关键行为/数据口径/安全合规底线已列出（与 R1 一致）
- **基线可度量**：至少 1 个基线有明确口径与数据源，且可复现采样
- **风险可操作**：Top 风险已登记，并形成后续 design 阶段的 PoC/验证清单
- **回滚可定义**：止损条件与回滚点初稿已给出（至少定义“触发信号→动作”）

满足 DoR 后，进入 design 块，复用 `design/sdlc_spec_coding.md` 的 Design 阶段产物与评审门禁（从 `design/research.md` 开始）。

---

## 5. 质量门槛（R2-DoD）

- 影响面审计能让评审者快速判断：这次重构会影响哪些契约/数据/运行资产。
- 基线可验证：给出指标口径与数据源入口，能在后续验证“是否变好/变差”。
- 回滚/止损可执行：至少能执行一次“假想演练”（不要求在 R2 落盘演练过程，但要能指导后续块补齐）。

