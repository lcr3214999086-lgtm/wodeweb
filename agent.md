# 项目开发指南

## 协作约定

- 默认使用中文沟通，界面文案使用简体中文。
- 修改前先阅读相关代码，保持改动与当前任务范围一致。
- 保留 Vue 前台、Django 后端和 SimpleUI 管理后台的现有架构。
- 不在文档、代码或日志中记录管理员密码等敏感信息。
- 完成后说明修改内容、验证结果和仍存在的限制。

## 技术栈

- Python 3.12，项目虚拟环境为 `.venv`。
- Django 5.2.18，依赖版本见 `requirements.txt`。
- Django SimpleUI 2026.1.13，位于 `INSTALLED_APPS` 首位。
- Vue 固定为 **3.5.25**，未经任务要求不要升级或改为浮动版本。
- Vite 7、JavaScript、Vue 单文件组件，使用 pnpm 和 `frontend/pnpm-lock.yaml`。
- SQLite 数据库为 `db.sqlite3`；语言为 `zh-hans`，时区为 `Asia/Shanghai`。

## 目录和请求流程

- `config/`：Django 设置、根路由和服务入口。
- `core/`：业务应用，已注册到 Django。
- `core/views.py`：按页面读取独立 HTML 构建入口；缺少构建产物时返回 404。
- `frontend/src/App.vue`：Vue 首页组件。
- `frontend/src/main.js`：Vue 应用入口。
- `frontend/src/style.css`：首页样式。
- `frontend/vite.config.js`：构建和开发代理配置。
- `frontend/dist/`：生成的构建产物，不直接编辑。
- `/`：Vue 网站首页；`/admin/`：SimpleUI 管理后台。
- 前端资源基路径为 `/static/frontend/`，Django 使用静态目录前缀 `frontend` 提供构建文件。
- Vite 将 `/api`、`/admin` 和 `/static/admin` 代理到 `http://127.0.0.1:8000`。目前尚未实现业务 API。
- 官网为多页面站点：`/`、`/products/`、`/support/`、`/contact/`、`/about/` 各有独立 HTML 入口与 Django 路由。导航使用普通链接，不使用 hash 路由；新页面需要同时配置 HTML 入口、Vite 构建入口及 Django 路由。

## 常用命令

以下命令在项目根目录的 PowerShell 中执行：

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

不激活虚拟环境时使用 `.\.venv\Scripts\python.exe`，避免误用全局 Python。

前端命令：

```powershell
cd frontend
pnpm install --frozen-lockfile
pnpm dev
pnpm build
```

Vite 开发页面路径为 `/static/frontend/`，端口以启动输出为准。访问 Django 的首页前必须完成 `pnpm build`。修改 Vue 源码后重新构建，才能更新 `http://127.0.0.1:8000/` 的内容。

如果当前工具环境未提供 pnpm 命令，先查找可用的 Node.js 和 pnpm 运行时。已有依赖时也可在 `frontend` 中执行 `node node_modules/vite/bin/vite.js build`。沙箱权限导致构建失败时按实际错误申请所需权限。

## 修改和验证

- 修改前端依赖时同步更新锁文件，保持 Vue 精确版本约束；不要混用 npm、yarn 的锁文件。
- `frontend/pnpm-workspace.yaml` 允许 esbuild 的必要构建脚本；新增脚本许可前确认依赖用途。
- 修改前端后执行构建；确认首页及生成的 JS、CSS 资源可访问。
- 修改 Django 后执行 `python manage.py check`；涉及业务行为时运行相关测试。
- 修改模型后生成、检查并应用迁移；保留数据库中的现有用户和数据。
- 修改依赖后检查依赖兼容性；Python 依赖可使用 `python -m pip check`。
- 前后端集成修改后检查 `/` 和 `/admin/`，确保管理后台继续可用。
- 若服务器以 `--noreload` 启动，修改 Python 代码或设置后需重启当前项目的服务器。

## 文件与部署

- 不提交或直接修改 `.venv/`、`frontend/node_modules/`、`frontend/dist/` 等环境或生成文件。
- 不提交 `db.sqlite3`、`.env`、密钥和密码；保留 `.gitignore` 中的忽略规则。
- 当前配置用于本地开发。正式部署需要单独配置密钥、`DEBUG`、`ALLOWED_HOSTS` 和静态资源服务。
- Django 默认用户没有独立昵称字段；当前昵称使用 `first_name`。需要独立昵称功能时先设计数据模型和迁移。
