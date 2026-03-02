---
title: 页面证据包（单页）
status: draft
---

# <page_name>（<page_id>）

> 面向产品阅读：先看“页面概览/核心任务/关键规则”。技术映射与代码证据在附录，供研发复核。

## 页面概览（产品视角）

- 所属模块（按菜单分组）：<module_name｜未归类>
- 页面名称（UI 标题）：<page_name>
- 一句话目标：...
- 目标用户/角色：...
- 入口（从哪来）：...
- 出口（到哪去）：...

## 页面面包屑（Breadcrumb）

> 用于快速定位“页面在产品结构中的位置”。优先来源：页面自身面包屑组件渲染/路由 meta/breadcrumb 配置；缺失则写入 Evidence Gaps。

- <模块>
- <子模块（可选）>
- <页面名称>

## 页面线框图（ASCII Wireframe）

> 只画结构，不画像素与视觉稿；让读者一眼看到“页面区块、信息架构、主要交互”。

```txt
+--------------------------------------------------------------+
| Header: <title>                        [PrimaryAction]       |
+--------------------------------------------------------------+
| Breadcrumb: <模块> / <子模块> / <页面>                        |
+-------------------------------+------------------------------+
| Filters/Search                | MainContent                  |
| - 条件1 [v]                   | - 列表/详情/表单/看板...     |
| - 条件2 [ ]                   | - 关键字段/区块/卡片...      |
| [Search] [Reset]              |                              |
+-------------------------------+------------------------------+
| Footer/Notes: <提示/说明/版本信息>                             |
+--------------------------------------------------------------+
```

## 核心任务（Top 3）

- T1: ...
- T2: ...
- T3: ...

## 关键规则摘要（Top 5）

- R1: ...
- R2: ...
- R3: ...
- R4: ...
- R5: ...

## 功能点（Feature points）

- FP-001: ...
  - 说明：...
  - 用户价值：...
  - 证据（附录引用）：file:lines 或见“附录 B”

## 用户旅程（User journeys）

- J-001: 入口 → 关键步骤 → 出口
  - 触发：...
  - 成功标准：...
  - 异常分支：...
  - 证据（附录引用）：file:lines 或见“附录 B”

## 业务规则（Rules）

- rule_id: ...
  statement: ...（可验收陈述）
  trigger: ...（触发点）
  condition: ...（条件）
  outcome: ...（结果）
  evidence:
    - file:lines
  evidence_gaps: []

## 附录 A：技术映射（供研发复核）

- page_id: <page_id>
- module_name: <module_name｜未归类>
- page_name: <page_name>
- page_name_evidence: file:lines（优先来自页面头部标题/Document.title；缺失则写 Evidence Gap）
- route_forms: ...
- normalized_path: ...
- entry_file: ...
- layout/shell: ...
- reachability: public|guarded|direct-link|internal-only|unknown
- auth（如有）：...（仅在证据足够时写）
- data_deps（如有）：...（仅写页面级关键依赖）

## 附录 B：Evidence（最小证据包）

- type: page_title | route_decl | file_convention | menu_static | menu_backend | nav_call | guard | api_call | state_machine | form_validation | other
  strength: strong | medium | weak
  file: ...
  lines: ...
  how: ...
  excerpt: ...

## Evidence Gaps（本页）

- gap: ...
  candidate_locations: ...
  impact: ...
