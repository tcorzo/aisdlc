---
name: aisdlc-project-discover-products-aggregation
description: Use when 需要从存量代码/契约/数据主责反推业务模块（products）并收敛到可治理的数量（建议 <=6），以避免认知与维护失控，同时为跨模块讨论提供稳定地图。
---

# aisdlc-project-discover-products-aggregation（Step5：业务模块聚合与收敛）

## 概览

Products 层的目标是“可治理的业务地图”，不是把所有功能名都列出来。数量过多会让地图失效，建议收敛到 **≤ 6**（如无法收敛必须写明原因与治理建议入口）。

**开始时宣布：**「我正在使用 aisdlc-project-discover-products-aggregation 技能从代码事实反推业务模块并收敛数量。」

## 线索优先级（从强到弱）

1. **数据主责（最强）**：哪个模块主写哪些核心对象（来自 `contracts/data/*`）
2. **对外能力边界**：哪些 API 是稳定承诺（来自 `contracts/api/*`）
3. **组织边界**：Owner/团队负责的模块群
4. **运行边界**：独立部署/扩缩容/SLO（如存在）

## 输出文件

- `.aisdlc/project/products/index.md`（可选但推荐）
- `.aisdlc/project/products/{module}.md`（每个业务模块一页）

## 最小模板（可复制）

### `products/index.md`

| product_module | owner | key_components | key_data_ownership | key_contracts | status |
|---|---|---|---|---|---|
| <name> | <team> | `../components/...` | `../contracts/data/...` | `../contracts/api/...` | - [ ] |

### `products/{module}.md`

- 业务边界：In/Out（一句话 + 链接到证据入口）
- 承载组件（入口）：链接到 `../components/*`
- 数据主责（入口）：链接到 `../contracts/data/*`
- 对外能力（入口）：链接到 `../contracts/api/*`
- 关键术语（入口）：链接到 `../memory/glossary.md`

## 收敛策略（<= 6 的做法）

- 先按“数据主责”聚类，再用“对外能力”校正边界
- 优先合并“仅被内部调用、没有数据主责、没有稳定对外契约”的碎片模块
- 保留“跨团队接口多/数据主责清晰/对外承诺稳定”的业务模块为一级

## 无法收敛怎么办（允许 >6，但必须写明）

在 `products/index.md` 顶部增加一段“不可收敛原因与治理入口”，常见可接受原因：

- 合规隔离/数据隔离硬要求
- 数据主责天然分裂且短期不可合并
- 组织边界强约束（多个独立团队/域）

并给出治理建议入口（例如 ADR/迁移路线/组织对齐会议纪要链接），不要留空洞 TODO。

## 红旗清单（出现任一条：停止并纠正）

- 把产品层写成“功能清单大全”（地图应短）
- 业务模块数量持续膨胀且没有收敛策略
- products 页复制组件页/契约页细节（应只链接入口）

