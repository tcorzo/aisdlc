---
name: aisdlc-project-discover-scope
description: Use when 存量项目 Discover（逆向）容易覆盖面失控，需要先做模块分级（P0/P1/P2）与逆向深度约束，确保优先把高 ROI 的模块做到可追溯而不是“写全但不可维护”。
---

# aisdlc-project-discover-scope（Step1：范围止损与模块分级）

## 概览

Discover 的最大风险不是“写得不够”，而是“试图覆盖所有模块导致不可维护”。Scope 的任务是先把范围**收敛**，并对不同优先级规定**最低交付深度**。

**开始时宣布：**「我正在使用 aisdlc-project-discover-scope 技能对模块做 P0/P1/P2 分级并设置逆向深度门禁。」

## 分级规则（建议）

- **P0（必须逆向）**：高频变更、跨团队交界、对外集成多、事故热点、合规风险高
- **P1（建议逆向）**：稳定但高频被引用/被问到/被依赖的基础能力
- **P2（按需逆向）**：低风险、低协作、生命周期短；只保留索引占位与入口

## 深度门禁（强约束）

- **P0 必须同时具备**
  - `.aisdlc/project/components/{module}.md`
  - `.aisdlc/project/contracts/api/{module}.md`
  - `.aisdlc/project/contracts/data/{module}.md`
  - 证据入口（代码/测试/CI/ops）
- **P1 必须具备**
  - `.aisdlc/project/components/{module}.md`
  - 至少一个契约入口页（API 或 Data）
- **P2 只要求**
  - 在索引占位（`components/index.md`；如有 products 也占位）
  - 保留入口链接即可（没有入口就写“未发现”）

## Scope 输出怎么写（放到索引里）

在 `.aisdlc/project/components/index.md` 的表格里体现分级与进度（索引只导航，不写细节）：

| module | priority | owner | code_entry | api_contract | data_contract | ops_entry | status |
|---|---|---|---|---|---|---|---|
| user | P0 | TeamA | `path/...` | `contracts/api/user.md` | `contracts/data/user.md` | `ops/...` | - [ ] |

> `status` 用复选框：`- [ ]` 未达标；`- [x]` 达到对应优先级的 DoD。

## 常见错误

- **把 P0/P1/P2 当“写作优先级”**：正确含义是“交付深度门禁不同”。
- **P0 只写组件页，不写契约入口页**：这会导致后续对接/改动无法追溯“承诺边界”。
- **P2 也写成详尽模块页**：范围会失控，维护失败。

## 红旗清单（出现任一条：停止并纠正）

- “全模块都要写到字段级”或“先把细节写全”
- 还没完成 P0，就开始铺开 P1/P2 的细节
- 不能明确 P0 模块是谁/边界是什么，却已经开始写大量流程细节

