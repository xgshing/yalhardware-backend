# YAL Hardware 后端系统

YAL Hardware 后端项目，基于 **Python + Django** 构建 API 服务，  
提供产品数据接口、订单管理及后台管理功能。与前端完全解耦，适用于工业 / 五金产品展示场景的企业后台系统。

---

## 🚀 项目简介

YAL Hardware Backend 提供完整的产品数据接口及后台管理功能，  
支持前端展示与后台内容管理。

项目重点不在“功能堆砌”，而在于：

- 清晰、可维护的项目结构
- 面向真实业务的数据建模与接口设计
- 可扩展的权限管理与 API 设计思路

---

## 📌 项目亮点

- 基于 Django + Django REST Framework 构建标准 RESTful API 架构
- 前后端完全解耦，支持多客户端接入（Web / Mobile）
- 订单状态机设计（Finite State Machine 思路），保证业务流程可控
- 原子事务（Atomic Transaction）保障库存一致性
- 双 Token 认证体系（前台用户 / 后台管理员权限隔离）
- 模块化 Django Apps 架构，符合企业级可扩展结构
- 支持多环境部署（Render / PostgreSQL / Cloudinary）

---

## 🧰 技术栈

- Python 3
- Django / Django REST Framework
- 数据库：PostgreSQL / SQLite
- 功能：ORM 数据模型、后台管理系统、双 Token 前台/后台认证
- 部署：可部署至 Render / Heroku / Vercel 等，图片存储支持 Cloudinary

---

## ✨ 核心功能

- 前台用户：浏览产品、下单、支付、确认收货
- 后台管理员：管理产品、库存、订单、内容、评论
- 原子事务保证库存安全，支持多条发货记录
- 订单状态机严格控制流程：Pending → Paid → Shipped → Completed → Review

---

## 📁 项目结构说明

```text
backend/
├── apps/             # Django apps
│   ├── products/     # 产品模块（产品信息、分类、属性）
│   ├── content/      # 内容管理模块（首页内容 / Banner / CMS 数据）
│   ├── inventory/    # 库存管理模块（SKU、库存数量、库存变更）
│   ├── orders/       # 订单模块（订单创建、状态流转）
│   ├── users/        # 用户模块（注册、登录、权限管理）
│   ├── reviews/      # 评论模块（产品评价）
│   └── system/       # 公司信息
├── config/           # Django 项目配置（settings / urls / wsgi）
├── core/             # 公共核心模块（基类模型、工具、公共逻辑）
├── manage.py         # Django 管理入口
├── requirements.txt  # Python 依赖文件
└── README.md         # 项目说明文档
```

---

## ▶️ 本地运行

```bash
git clone https://github.com/xgshing/yalhardware-backend.git
cd yalhardware-backend
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

```md
浏览器访问：

http://localhost:9000
```

---

## 🔗 Render 部署与演示

后端已部署至 Render，访问方式如下：

- 根路径 /

  ```text
  https://yalhardware-backend.onrender.com/
  ```

  Django 默认根路径没有配置页面，因此访问会显示 404 Page Not Found。
  根路径主要用于 API 状态或重定向，前端无需访问。

- API 接口路径 /api/
  例如：

  https://yalhardware-backend.onrender.com/api/products/

  前端 Vue 项目通过 Axios 调用这些接口获取产品数据。

- 后台管理 /admin/

```text
- https://yalhardware-backend.onrender.com/admin/

```

登录后可管理用户、组以及自定义模型（产品、首页内容、订单等）。

---

## 🧠 未来优化方向

- 基于角色的 RBAC 权限管理系统（细粒度权限控制）
- API 文档自动化（Swagger / OpenAPI）
- 单元测试与业务测试覆盖（Django TestCase）
- 订单状态扩展（退款 / 取消 / 部分发货支持）
- Webhook 机制支持支付回调与异步处理
- 日志系统与异常监控（Sentry 集成）
- API 版本管理（/api/v1/）
- 国际化支持（i18n API 字段扩展）
- Redis 缓存优化热点接口性能
- CI/CD 自动化部署流程

## 📄 License

MIT
