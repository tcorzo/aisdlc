---
title: 前端页面清单（Page Inventory）
status: draft
---

目的：面向产品同学快速理解“有哪些页面、分别做什么、入口是什么、关键规则是什么”。技术映射与代码证据下沉到附录，仍保持可追溯与可复核。

## 0) 页面模块目录（按菜单分组）

> 模块口径：优先按侧边栏/顶部导航的菜单分组（一级/二级均可）。无法从菜单证据归类的页面放入“未归类”，并写 Evidence Gaps。

| module_name | 页面数 | 说明 | 备注/缺口 |
|---|---:|---|---|
| ... | ... | ... | ... |

## 1) 页面清单（产品视角，按模块分节）

### 1.1 模块：<module_name>

| page_id | page_name | 页面目标（一句话） | 核心任务（Top 3） | 入口（从哪来） | 关键规则摘要（Top 5） | 备注/缺口 |
|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... |

### 1.2 模块：未归类（缺少模块归属证据）

| page_id | page_name | 页面目标（一句话） | 核心任务（Top 3） | 入口（从哪来） | 关键规则摘要（Top 5） | 备注/缺口 |
|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | gap: 缺少菜单映射证据 |

## 附录 A：技术映射与证据（供研发复核）

### A.1 去重与审计口径

- PageKey: NormalizedPath + EntryFile
- NormalizedPath 规则：:id/[id]/{id} → {param}；[...slug] → {*param}
- 并集：Routes ∪ Menus ∪ NavCalls
- 差集审计：
  - MenuPaths - RoutePaths: ...
  - RoutePaths - MenuPaths: ...
  - NavCalls - (Routes ∪ Menus): ...

### A.2 技术事实表（可追溯）

| page_id | module_name | page_name | page_name_evidence | route_forms | normalized_path | entry_file | reachability | auth | data_deps | evidence_links | evidence_gaps |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ... | ... | ... | file:lines | ... | ... | ... | ... | ... | ... | file:lines | ... |

### A.3 证据入口（索引）

- FrontendRoots:
  - <path>（证据：file:lines）
- RouteEntrypoints:
  - <path>（证据：file:lines）
- MenuEntrypoints:
  - <path>（静态/后端下发；证据：file:lines）
- AuthEntrypoints:
  - <path>（guard/middleware；证据：file:lines）
- ApiClientEntrypoints:
  - <path>（axios/fetch/client；证据：file:lines）

### A.4 Evidence Gaps（全局）

- gap: ...
  candidate_locations: ...
  impact: ...
