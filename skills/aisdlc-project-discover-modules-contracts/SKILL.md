---
name: aisdlc-project-discover-modules-contracts
description: Use when 需要为选中的模块（优先 P0）同时产出组件页与契约入口页（API/Data），把“权威入口 + 不变量摘要 + 证据入口”立起来，并回填索引，避免写成字段大全或缺少证据链。
---

# aisdlc-project-discover-modules-contracts（Step4：模块页 + 契约入口页）

## 概览

这一阶段的交付不是“把代码翻译成文档”，而是把**权威入口**立起来：

- `components/{module}.md`：模块边界与协作入口
- `contracts/api|data/{module}.md`：契约权威入口 + 不变量摘要 + 证据入口

**开始时宣布：**「我正在使用 aisdlc-project-discover-modules-contracts 技能为模块生成组件页与 API/Data 契约入口页，并建立证据链。」

## 输出文件

- `.aisdlc/project/components/{module}.md`
- `.aisdlc/project/contracts/api/{module}.md`
- `.aisdlc/project/contracts/data/{module}.md`
- 回填：
  - `.aisdlc/project/components/index.md`
  - `.aisdlc/project/contracts/api/index.md`
  - `.aisdlc/project/contracts/data/index.md`

## 最小模板（可复制）

### `components/{module}.md`

- 模块定位：In/Out（明确不负责什么）
- Owner：团队/负责人（可链接通讯录/值班）
- 入口：
  - 代码入口：`<目录/路由/handler/consumer/job/cli 的路径>`
  - 运行入口：`../ops/<...>`（若有）
- 对外接口与契约入口：
  - API：`../contracts/api/{module}.md`
  - Data：`../contracts/data/{module}.md`
- 代表性协作场景（1–2 个）：只写“谁调用谁 + 关键边界”，不写详细时序
- NFR 分摊摘要：性能/可用性/安全关键点（只写护栏与入口）
- 证据链接：
  - 关键测试入口：`<tests/...>` 或 CI job
  - 关键监控/告警入口：`<dashboard/alert>`（若有）

### `contracts/api/{module}.md`

- 权威入口（必须可定位）：
  - OpenAPI/Proto 文件：`<path 或外部链接>`
  - 网关/路由入口：`<path>`
- 不变量摘要（3–7 条，写“承诺边界”）：
  - 鉴权/授权模型（谁能调用）
  - 幂等/重试语义（客户端如何安全重试）
  - 错误码族/错误分类（稳定契约）
  - 版本/兼容策略（变更窗口）
  - 审计/合规要求（如有）
- 证据入口：
  - handler/路由：`<path>`
  - 测试：`<path>`
  - CI 门禁：`<job/命令或配置路径>`

### `contracts/data/{module}.md`

- 数据主责（Ownership）：主写/只读/同步来源（明确边界）
- 核心对象与主键：对象名 + 主键/唯一标识 + 生命周期一句话
- 权威入口：
  - Schema/DDL/迁移：`<path>`
  - ORM model：`<path>`（如适用）
- 不变量摘要（3–7 条）：
  - 关键口径（例如状态含义、金额/时间口径）
  - 状态机/生命周期约束
  - 唯一性/外键/不可变字段（只写稳定约束）
- 证据入口：
  - 关键读写路径：`<repo path>`
  - 关键测试：`<tests path>`
  - CI 门禁：`<job/命令或配置路径>`

## 质量门禁（P0 必须满足）

- P0 模块的三份文件必须同时存在并互相链接正确
- 两个契约页都必须具备“三件套”：权威入口 + 不变量摘要 + 证据入口
- 任何“不确定”不得写成字段大全或脑补结论，只能：
  - 写“未发现/待定位”的入口占位
  - 写下一步如何找到证据（具体到文件类型/目录线索）

## 常见错误

- **把契约页写成字段字典**：Discover 的契约页是入口与不变量摘要，不是全量字段说明。
- **只写路径，不写不变量**：会导致协作时无法理解“稳定承诺边界”。
- **没有证据入口**：后续无法验证、无法定位实现与测试。

## 红旗清单（出现任一条：停止并纠正）

- 新增 `.aisdlc/project/docs/api-reference`、`data-dictionary` 等目录来堆字段级细节
- 在契约页里贴大量字段表格，且没有权威入口文件链接
- 协作场景写成详细时序（应留给需求级/变更级产物，而非项目级）

