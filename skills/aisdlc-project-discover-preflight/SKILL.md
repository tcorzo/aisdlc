---
name: aisdlc-project-discover-preflight
description: Use when 开始对存量项目做 Discover（逆向）前需要盘点“可作为证据的入口”（运行/测试/CI/契约/关键目录/监控告警），避免后续写成观点文档或在缺证据时脑补。
---

# aisdlc-project-discover-preflight（Step0：准备与证据入口盘点）

## 概览

Preflight 的目标不是“理解全部代码”，而是先找到**可执行证据**与**权威入口**，为后续 `.aisdlc/project/*` 的每个链接提供可追溯来源。

**开始时宣布：**「我正在使用 aisdlc-project-discover-preflight 技能盘点证据入口，建立可追溯清单。」

## 输入 / 输出

- **输入**：仓库目录结构、构建脚本、依赖文件、配置文件、CI/CD 配置、契约文件（OpenAPI/Proto/Schema/迁移）、可观测性入口（如有）。
- **输出（最小）**：一份“证据入口清单”（先作为草稿，后续分散回填到 Memory/索引/模块页/契约页/ops）。

## 证据入口清单（最小项）

把你找到的入口按下面分类记录（**没有就写“未发现”**，不要猜）：

- **运行入口**
  - 本地启动命令/脚本路径
  - 环境变量/配置入口（示例：`.env.example`、`config/*`、`values.yaml` 等）
- **测试入口**
  - 单测/集成测/E2E 的命令或脚本路径
  - 覆盖率/质量门禁入口（若有）
- **构建与发布入口**
  - build 命令/脚本路径
  - pipeline/job 的配置文件位置
- **契约入口**
  - OpenAPI/Proto/JSON Schema/GraphQL schema 的文件路径（若有）
  - DB schema/DDL/迁移目录（若有）
  - ORM model 定义入口（若有）
- **关键目录（地图线索）**
  - 服务/应用边界（apps/services/packages/src 等）
  - 网关/路由/handler 入口
  - job/consumer/worker 入口
- **可观测性入口（如有）**
  - dashboard / alerts / logs 查询入口链接或配置位置
  - runbook/值班/回滚入口（若有）

## 推荐证据来源（按优先级）

优先找“能执行/能定位”的证据，再找描述性文档：

1. **脚本/命令**：`package.json`、`Makefile`、`justfile`、`*.ps1`、`*.sh`
2. **CI/CD**：`.github/workflows/*`、Azure/GitLab/Jenkins pipeline 文件
3. **契约文件**：`openapi.*`、`proto/`、`schema/`、`migrations/`
4. **README/Docs**：只作为导航，不作为最终证据

## 把“证据入口清单”先落在哪里（不新增目录）

先把草稿写进 `.aisdlc/project/memory/structure.md` 的一个临时小节（后续会被拆散回填）：

- `## 证据入口清单（临时）`
  - 运行/测试/构建发布/契约/可观测性/关键目录的入口列表（每条包含路径或链接）

> 不要为了“放草稿”在 `.aisdlc/project/` 下发明新目录（例如 `docs/`、`inbox/`）；会扩大维护面并诱发细节沉积。

## 红旗清单（出现任一条：停止并纠正）

- 证据没找到就开始写“项目怎么跑/怎么测/契约在哪”（应写“未发现 + 下一步如何找到”）
- 为了交付速度，先生成大量字段级说明（字段大全不是 Discover 的项目级产物）
- 把 README 的描述当作事实而不链接到脚本/CI/契约文件

## 一个好例子（证据入口清单的一条记录）

- 测试入口：`package.json` 的 `scripts.test`（路径：`package.json`；命令：`npm test`）
- CI 门禁：GitHub Actions `ci.yml`（路径：`.github/workflows/ci.yml`；关键 job：`test`）

