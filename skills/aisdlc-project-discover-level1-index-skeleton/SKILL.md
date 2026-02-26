---
name: aisdlc-project-discover-level1-index-skeleton
description: Use when 需要先生成 `.aisdlc/project` 的地图层索引骨架（components/products/contracts）与进度面板（checkbox），并用“索引只导航”的硬规则避免双写与维护爆炸。
---

# aisdlc-project-discover-level1-index-skeleton（Step3：索引骨架 + 进度面板）

## 概览

索引页的唯一职责是：**导航 + 进度**。细节一律落在模块页/契约入口页/ops 页。

**开始时宣布：**「我正在使用 aisdlc-project-discover-level1-index-skeleton 技能生成地图层索引骨架与复选框进度面板。」

## 输出文件（骨架）

- `.aisdlc/project/components/index.md`
- `.aisdlc/project/products/index.md`（可选）
- `.aisdlc/project/contracts/index.md`
- `.aisdlc/project/contracts/api/index.md`
- `.aisdlc/project/contracts/data/index.md`

## 写法约束（硬规则）

- `index.md` **只做导航**：表格 + 链接 + 状态复选框；禁止复制模块细节。
- 用复选框管理补齐进度：
  - `- [ ] moduleA`：未达标
  - `- [x] moduleA`：达到对应优先级 DoD

## 最小模板（可复制）

### `components/index.md`

| module | priority | owner | code_entry | api_contract | data_contract | ops_entry | status |
|---|---|---|---|---|---|---|---|
| <module> | P0/P1/P2 | <team> | `<path>` | `../contracts/api/<module>.md` | `../contracts/data/<module>.md` | `../ops/...` | - [ ] |

### `contracts/index.md`

- API：`./api/index.md`
- Data：`./data/index.md`

### `contracts/api/index.md`

| module | authority_entry | invariants | evidence | status |
|---|---|---|---|---|
| <module> | `<openapi/proto path>` | 3–7 条摘要 | code/test/ci 入口 | - [ ] |

### `contracts/data/index.md`

| module | ownership | authority_entry | invariants | evidence | status |
|---|---|---|---|---|---|
| <module> | 主写/只读/同步 | `<schema/migrations path>` | 3–7 条摘要 | code/test/ci 入口 | - [ ] |

### `products/index.md`（可选）

| product_module | owner | key_components | key_data_ownership | status |
|---|---|---|---|---|
| <name> | <team> | `../components/...` | `../contracts/data/...` | - [ ] |

## 常见错误

- **索引写成模块页**：越写越长，维护爆炸；应只保留链接与极短摘要。
- **没有 checkbox 进度**：会失去“先骨架后补证据”的迭代机制。

## 红旗清单（出现任一条：停止并纠正）

- 在索引里出现接口字段说明/表字段字典/详细时序/操作手册
- 为了“看起来完整”把模块页内容复制到 index
- 没有明确 P0/P1/P2 却开始写大量模块细节

