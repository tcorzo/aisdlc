---
title: D1 研究（Research）— 设计阶段问题域与不确定性收口规范
status: draft
stage: design
module: D1
principles_ref: design/aisdlc.md
source_refs:
  - design/aisdlc_spec_design.md
---

## 0. 目标与定位

本设计文档用于定义 Design 阶段模块 D1「研究」的**框架性规则、硬约束与验收标准**，用于约束后续可能的命令/模板实现，以及指导人工/AI 产物生成。

D1 的目标是把需求/重构的**问题域与不确定性**变成可执行的设计输入：现状、范围、约束、风险、未知项及研究结论，为 D2 概要设计提供稳定上下文。

输出稳定落盘到：

- `{FEATURE_DIR}/design/research.md`

---

## 1. 术语与接口

### 1.1 上下文与路径

- **FEATURE_DIR**：由 `Get-SpecContext` 自动获取，定位到 `.aisdlc/specs/{num}-{short-name}/`
- **必读输入**：
  - `{FEATURE_DIR}/requirements/clarify.md`（范围边界与约束）
  - `{FEATURE_DIR}/requirements/solutions.md` 或 `requirements/prd.md`（若存在）
- **输出**：`{FEATURE_DIR}/design/research.md`

### 1.2 必读材料（最小必要读取）

- `requirements/clarify.md`（In/Out 与约束）
-（按需）相关现状代码、依赖拓扑、运行指标、协议/数据口径入口

---

## 2. 强制门禁（MUST）

- **必须列出所有未知项并标注为 "NEEDS CLARIFICATION"**。
- **必须输出研究结论**，且以“决策 / 理由 / 备选方案”三段式呈现。
- **未知项未解决不得进入 D2**（门禁失败则 ERROR）。
- **全程使用中文**。

---

## 3. 输出结构（`research.md` 最小骨架）

建议至少包含：

- **TL;DR**：问题域现状与最大风险
- **现状与问题域**：关键现状、痛点与影响
- **范围边界**：In/Out 与不变量
- **关键约束**：合规/性能/依赖/组织
- **风险清单**：Top 风险与影响描述
- **未知项清单**：统一标注为 "NEEDS CLARIFICATION"
- **研究结论**：
  - **Decision**：选择了什么结论/方向
  - **Rationale**：为什么选择
  - **Alternatives considered**：考虑过哪些替代方案
- **追溯链接**：raw/clarify/监控/ADR 入口

---

## 4. 进入 D2 的 DoR 清单（D1 末尾必须包含）

DoR 的目标是让“是否可以进入概要设计”变成可检查门禁：

- **未知项已处理**：所有 NEEDS CLARIFICATION 要么解决，要么明确不影响 D2
- **范围可执行**：In/Out 与不变量已冻结
- **研究可复用**：结论与依据可追溯

---

## 5. 质量门槛（D1-DoD）

- 评审者能够快速判断：当前问题域是否清晰、有哪些不确定性。
- 研究结论为 D2 提供可直接复用的输入。
