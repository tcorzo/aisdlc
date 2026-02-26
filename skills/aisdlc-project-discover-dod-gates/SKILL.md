---
name: aisdlc-project-discover-dod-gates
description: Use when 需要对 `.aisdlc/project/` 的 Discover（逆向）成果做 DoD 自检与门禁收口，确保 P0 模块三件套齐全、索引只导航、契约页具备权威入口与证据链，并在压力下能拒绝写字段大全与项目级细节沉积。
---

# aisdlc-project-discover-dod-gates（Step7：DoD 完成标准与门禁）

## 概览

DoD 的作用是：**让成果可维护**。没有 DoD 的 Discover 会在压力下退化成“细节堆积/不可追溯/无人敢改”。

**开始时宣布：**「我正在使用 aisdlc-project-discover-dod-gates 技能对 Discover 成果执行 DoD 自检与门禁收口。」

## 项目级 DoD（最小自检清单）

- [ ] `memory/` 四份已具备“入口清晰/边界清晰/可导航”
- [ ] Level-1 索引骨架已生成，且复选框进度可用
- [ ] 每个 **P0 模块**满足：
  - [ ] `components/{module}.md` 存在且边界清晰（In/Out）
  - [ ] `contracts/api/{module}.md` 具备三件套（权威入口 + 不变量 + 证据入口）
  - [ ] `contracts/data/{module}.md` 具备三件套（权威入口 + 不变量 + 证据入口）
  - [ ] 索引回填完成（`components/index.md`、`contracts/*/index.md`）
- [ ] `products` 已收敛到 ≤ 6；若无法收敛，已记录原因与治理入口
- [ ] 索引只导航，细节不双写；模块页/契约页是权威入口
- [ ] （若有 ops）`ops/index.md` 提供可定位入口（dashboard/告警/runbook/回滚），且不复制操作手册

## 门禁规则（必须 enforce）

- **索引只导航**：任何 `index.md` 出现字段表格/详细时序/操作手册 → 视为失败。
- **契约页不写字段大全**：契约页的目标是权威入口与不变量摘要；字段级说明不属于本 Discover 的项目级产物。
- **证据缺失不允许脑补**：缺证据只能写“未发现 + 下一步如何找”，并把缺口暴露给维护者。

## 常见陷阱（以及规避）

- **陷阱：试图一次性写全**
  - 规避：先 Scope；P0 先落地；P1/P2 只占位与入口
- **陷阱：把一次性交付细节写进项目级**
  - 规避：项目级只写入口/边界/护栏；细节只提供证据入口
- **陷阱：索引与模块双写**
  - 规避：索引只导航；模块页/契约页才是权威
- **陷阱：契约不权威**
  - 规避：必须三件套；缺一不可

## 红旗清单（出现任一条：停止并回滚改动方向）

- 新增 `.aisdlc/project/docs/*`（data-dictionary/api-reference）来承载字段大全
- 新增 `.aisdlc/project/flows/*` 或 `.aisdlc/project/ops/runbooks/*` 来承载一次性交付细节
- “先把细节写全，索引以后补”的交付方式
- P0 模块缺契约页或缺证据入口，却宣称“已完成”

