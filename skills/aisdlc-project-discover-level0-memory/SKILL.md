---
name: aisdlc-project-discover-level0-memory
description: Use when 需要为存量项目建立 `.aisdlc/project/memory/*` 北极星入口，让任何人/AI 在几分钟内知道项目边界、怎么跑、怎么验、权威入口在哪，并避免把一次性交付细节写进项目级。
---

# aisdlc-project-discover-level0-memory（Step2：Level-0 / Memory）

## 概览

Memory 的目标是“3 分钟可入场”：项目是什么、边界是什么、怎么跑、怎么验证、权威入口在哪。

**写法约束：短、只写稳定入口与边界、用证据链接。**

**开始时宣布：**「我正在使用 aisdlc-project-discover-level0-memory 技能生成项目级 Memory（structure/tech/product/glossary）。」

## 输出文件（固定 4 份）

- `.aisdlc/project/memory/structure.md`
- `.aisdlc/project/memory/tech.md`
- `.aisdlc/project/memory/product.md`
- `.aisdlc/project/memory/glossary.md`

## 最小模板（可复制）

### `memory/structure.md`

- 项目形态：单体/多服务/Monorepo（写**证据入口**：目录/脚本/CI）
- 入口（必须可定位）：
  - 本地启动：`<命令或脚本路径>`
  - 测试：`<命令或脚本路径>`
  - 构建/发布：`<CI job 配置路径 或 脚本>`
- 地图入口：
  - 组件索引：`../components/index.md`
  - 契约索引：`../contracts/index.md`
  - 运行入口：`../ops/`（若有）
- `## 证据入口清单（临时）`（来自 Step0 的草稿，后续拆散回填）

### `memory/tech.md`

- 技术栈（只列稳定选择）：语言/框架/数据库/消息/网关
- 工程护栏入口：lint/test/安全扫描（命令与 CI job 配置位置）
- NFR 护栏入口：性能/可用性/成本/安全（链接到 `../nfr.md` 或外部规范）

### `memory/product.md`

- 业务边界：In/Out（一句话 + 证据入口链接）
- 关键业务模块入口：`../products/index.md`（若有）
- 关键术语入口：`./glossary.md`

### `memory/glossary.md`

- 术语：定义（1 句）+ 权威出处链接（契约页/代码类型/ADR/外部文档）

## 常见错误

- **把 Memory 写成“项目说明书”**：Memory 只做入口与边界，细节应链接到模块页/契约页/ops。
- **为了显得完整而脑补**：没有证据就写“未发现 + 下一步如何找到”，不要猜。

## 红旗清单（出现任一条：停止并纠正）

- Memory 出现字段级约束、详细时序、迁移步骤、操作手册完整版
- “先写一大段概述，入口链接以后补”（入口是 Memory 的核心）
- 术语没有权威出处链接（会变成口头定义，快速漂移）

