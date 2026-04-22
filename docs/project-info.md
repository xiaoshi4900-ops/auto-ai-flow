# 项目信息

版本：v3  
状态：持续更新  
用途：供后续 AI / 开发人员接手时快速获取项目环境、远程测试机信息、部署约束与已确认配置

---

## 1. 项目基础信息

- 项目名称：`AutoAiFlow`
- 当前阶段：一期 MVP 设计与实施准备阶段
- 本地工作区路径：`C:\workspace\AutoAiFlow`
- 主文档：
  - [implementation-spec-mvp-v1.md](docs/implementation-spec-mvp-v1.md)
  - [tdd-task-breakdown-spec-v1.md](docs/tdd-task-breakdown-spec-v1.md)
  - [ui-reference-spec-v1.md](docs/ui-reference-spec-v1.md)
  - [playwright-test-cases-v1.md](docs/playwright-test-cases-v1.md)

---

## 2. 本地与远程职责划分

### 2.1 本地机器

本地机器负责：

1. 编写代码
2. 维护文档
3. 生成 task packet / implementation spec / TDD spec
4. 通过 SSH 连接远程测试机

### 2.2 远程测试机

远程测试机负责：

1. 安装 Python / Node.js / PostgreSQL / Redis
2. 创建数据库和数据库用户
3. 创建项目虚拟环境
4. 部署 backend / frontend / worker
5. 执行 migration
6. 做联调与环境级验证

结论：

- 所有“安装环境”“安装数据库”“创建数据库”“部署服务”的默认语义，都指远程测试机，不是本地机器。

---

## 3. 远程测试机信息

### 3.1 SSH 连接信息

- 协议：`ssh`
- 主机：`172.18.14.8`
- 端口：`22`
- 用户名：`chat`
- 密码：`chat886`

### 3.2 基础系统信息

- 操作系统：`Ubuntu 22.04.3 LTS`
- Node.js：`v20.20.2`
- npm：`10.8.2`

---

## 4. 当前远程环境状态

### 4.1 Python

- 系统默认可用 Python：
  - `python3` -> `Python 3.10.12`
- 项目要求的 Python 基线：
  - `python3.11` -> `Python 3.11.15`
- 项目虚拟环境：
  - 路径：`/home/chat/apps/autoaiflow/.venv`
  - 解释器：`/home/chat/apps/autoaiflow/.venv/bin/python`
  - 版本：`Python 3.11.15`

说明：

- 不修改系统默认 `python3`
- 项目后续一律使用 `python3.11` 或 `.venv/bin/python`

### 4.2 PostgreSQL

- 版本：`PostgreSQL 14.22`
- 服务状态：`active`
- 数据库名：`auto_ai_flow`
- 数据库用户：`auto_ai_flow`
- 当前数据库密码：`AutoAiFlow_pg_2026!`
- 验证结果：
  - 已通过 `psql -h 127.0.0.1 -U auto_ai_flow -d auto_ai_flow` 登录验证

建议连接串：

```text
postgresql+psycopg://auto_ai_flow:AutoAiFlow_pg_2026!@127.0.0.1:5432/auto_ai_flow
```

### 4.3 Redis

- 版本：`Redis 6.0.16`
- 服务状态：`active`
- 连通性：`redis-cli ping` -> `PONG`
- 当前监听：`127.0.0.1:6379`

---

## 5. 当前确认可用的远程连接参数

推荐远程 `.env`：

```env
APP_NAME=AutoAiFlow
APP_ENV=dev
APP_DEBUG=true

DATABASE_URL=postgresql+psycopg://auto_ai_flow:AutoAiFlow_pg_2026!@127.0.0.1:5432/auto_ai_flow
REDIS_URL=redis://127.0.0.1:6379/0

JWT_SECRET=dev-secret-change-in-production-2026
JWT_EXPIRE_MINUTES=120
JWT_REFRESH_EXPIRE_DAYS=7

DEFAULT_TIMEOUT_SEC=300
```

---

## 6. 当前工程内应同步使用的值

以下值已经确认，后续工程配置、部署脚本、AI 交接都应使用：

- PostgreSQL 用户：`auto_ai_flow`
- PostgreSQL 密码：`AutoAiFlow_pg_2026!`
- 数据库名：`auto_ai_flow`
- Python 基线：`3.11.15`
- 项目虚拟环境：`/home/chat/apps/autoaiflow/.venv`

---

## 7. 当前未完成项

虽然远程基础环境已经基本具备，但以下事项仍需继续完成：

1. 在 `.venv` 中安装项目后端依赖
2. 将远程部署实际使用的 `.env` 文件落地
3. 跑 Alembic migration / 健康检查
4. 验证 backend / worker / frontend 的完整启动流程
5. 确认 PostgreSQL 是否需要收紧监听地址

---

## 8. 最近更新

- 2026-04-20：初始化远程测试机信息文档。
- 2026-04-20：明确安装环境、数据库创建、部署服务默认都指远程测试机 `172.18.14.8`。
- 2026-04-20：确认远程机为 Ubuntu 22.04.3 LTS。
- 2026-04-20：安装并修复稳定版 `Python 3.11.15`，创建项目虚拟环境 `/home/chat/apps/autoaiflow/.venv`。
- 2026-04-20：确认 PostgreSQL 14.22、Redis 6.0.16、Node.js 20.20.2 可用。
- 2026-04-20：将数据库用户 `auto_ai_flow` 密码重置为 `AutoAiFlow_pg_2026!` 并验证连接成功。
