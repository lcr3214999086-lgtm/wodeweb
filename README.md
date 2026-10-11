# 网站开发

前台使用 Vue 3 和 Vite，后端使用 Django，管理后台使用 SimpleUI。

## 启动网站

在项目根目录的 PowerShell 中执行：

```powershell
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

首页：http://127.0.0.1:8000/；后台：http://127.0.0.1:8000/admin/。

## 前端开发

安装 Node.js 和 pnpm 后，在 `frontend` 目录执行：

```powershell
pnpm install
pnpm dev
```

开发地址以 Vite 输出为准，路径为 `/static/frontend/`。Django 需同时启动；Vite 将 `/api` 和管理后台请求代理到 Django。

修改前端后执行 `pnpm build`，刷新 Django 首页即可看到更新。构建结果位于 `frontend/dist`。

当前 Django 开发服务器提供前端静态资源。正式部署前须另行配置静态资源服务。

## 官网页面

官网使用独立 HTML 多页面入口，导航会加载完整页面：

- 首页：`/`
- 产品：`/products/`
- 服务支持：`/support/`
- 联系：`/contact/`
- 关于我们：`/about/`

每个页面可直接访问和刷新。开发时在 Vite 的 `/static/frontend/` 基路径下访问对应目录。
