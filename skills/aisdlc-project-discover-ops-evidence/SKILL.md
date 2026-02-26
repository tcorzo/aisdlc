---
name: aisdlc-project-discover-ops-evidence
description: Use when 需要把“能跑、能验、能回滚、能排障”的运行入口与证据链固定到 `.aisdlc/project/ops`，并用入口页写法避免把操作手册/迁移步骤等细节堆进项目级文档。
---

# aisdlc-project-discover-ops-evidence（Step6：Ops & Evidence 入口与证据链）

## 概览

Ops 的高 ROI 在于：把“运行入口”固定下来（dashboard/告警/runbook/回滚入口），并把证据链补齐，减少事故时的搜索成本。

**写法约束：短、可执行、只提供入口与要点，不复制操作手册。**

**开始时宣布：**「我正在使用 aisdlc-project-discover-ops-evidence 技能补齐 ops 入口并串起证据链。」

## 输出文件（可选但强烈建议）

- `.aisdlc/project/ops/` 目录下的入口页（你可以按团队已有体系最小化）：
  - `ops/index.md`：总入口（**使用 `index.md`，不要用 `README.md`**）
  - 其他：监控/告警/回滚/值班/Runbook 的入口页（按需）

## 最小模板（可复制）

### `ops/index.md`

- 运行入口清单（每条都要可定位）：
  - Dashboard：`<link 或配置位置>`
  - Alerts：`<link 或配置位置>`
  - Logs：`<查询入口或配置位置>`
  - Runbook：`<入口页或外部链接>`
  - Rollback：`<入口页或策略链接>`
- 常见故障的“第一跳”：
  - 入口（点哪）
  - 关键指标（看什么）
  - 触发动作（下一步做什么/找谁）

## 证据链（必须在入口页体现）

把以下链路在合适的页面中用链接串起来（不要求一页写全，但必须可追溯）：

- **Contracts（契约）** → `contracts/*`
- **Code（实现入口）** → 代码目录/路由/handler/job
- **Tests（验证入口）** → 测试目录/命令
- **CI（门禁入口）** → pipeline 配置/关键 job
- **Ops（运行入口）** → dashboard/alerts/runbook/rollback

## 常见错误

- **把 ops 写成操作手册完整版**：项目级 ops 应只给入口与要点；细节会失控且过期。
- **把迁移步骤当作项目级长期资产**：迁移细节往往一次性且易过期，项目级只保留入口与策略。

## 红旗清单（出现任一条：停止并纠正）

- 在 `.aisdlc/project/ops/` 下新增 `runbooks/`、`migrations/` 等目录并把细节全文迁入
- ops 页没有任何可点击/可定位入口，只剩“检查日志/联系运维”之类空话
- 证据链断裂（找不到契约/实现/测试/CI 的入口链接）

