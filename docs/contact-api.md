# 联系表单新增接口

Vue 联系页面已调用此接口，成功请求写入 SQLite 的 `contract` 表。访客可以新增需求；查看记录需要登录 Django 管理后台。

## 获取请求令牌

`GET /api/inquiries/` 返回 `ready` 和 `csrf_token`，并设置 CSRF cookie。随后提交时携带 cookie 和 `X-CSRFToken` 请求头。

## 新增需求

`POST /api/inquiries/`，使用 `Content-Type: application/json`。八项字段均必填：

| JSON 字段 | 含义 | 要求 |
| --- | --- | --- |
| contact | 联系人 | 最多 60 字符 |
| phone | 联系电话 | 6–30 字符，数字、空格、加号、括号或短横线 |
| company | 公司/品牌 | 最多 120 字符 |
| request_type | 需求类型 | 企业存储采购、存储扩容升级、备份与容灾、方案咨询、其他需求 |
| quantity | 预计数量 | 1–1000000 的整数 |
| city | 交付城市 | 最多 80 字符 |
| budget | 预算区间 | 5万元以下、5–20万元、20–50万元、50–100万元、100万元以上、待评估 |
| description | 需求说明 | 最多 3000 字符 |

成功返回 HTTP 201：

```json
{"message":"需求已提交成功。","id":1}
```

校验失败返回 HTTP 400 和 `errors` 字段；缺少有效 CSRF 令牌返回 403；非 JSON 请求返回 415。错误请求不新增记录。

前端使用同源相对地址，部署时应使 `/api/` 与官网位于同一站点。Vite 开发代理已配置 `/api/`。

后台记录入口：`/admin/core/inquiry/`。数据库模型保留 `Inquiry` 名称，实际数据表名为 `contract`。
