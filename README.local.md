# YAL Hardware 后端系统

YAL Hardware 后端项目，基于 **Python + Django** 构建 API 服务，提供产品数据接口并支持后台管理。  
与前端完全解耦，适用于工业 / 五金产品展示场景的企业后台系统。

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

- 使用 Django 与 Django REST Framework 构建可扩展 API
- 数据库模型设计清晰，可支持多种产品类别和属性
- 后台管理系统可快速查看、增删改产品数据
- 可部署至云端（Render / Heroku / Vercel 等）
- 与前端项目完全解耦，支持 API 调用与状态管理

---

## 🧰 技术栈

- Python 3
- Django / Django REST Framework
- 数据库：PostgreSQL / SQLite
- ORM 数据模型
- 后台管理系统
- 虚拟环境管理与依赖安装（pip / requirements.txt）

---

## ✨ 核心功能

- 产品 CRUD 接口（Create / Read / Update / Delete）
- 用户与权限基础管理
- 数据库迁移与管理
- 与前端 API 解耦
- 可扩展的后台管理与接口权限控制

---

## 📁 项目结构说明

```text
backend/
├── apps/          # Django apps
├── migrations/    # 数据库迁移文件
├── static/        # 静态文件
├── templates/     # 模板文件
├── manage.py      # Django 管理命令
└── requirements.txt # Python 依赖
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

http://localhost:8000
```

---

## 🔗 Render 部署与演示

后端已部署至 Render，访问方式如下：

- 根路径 /

  ```text
  https://yalhardware-backend.onrender.com/
  ```

  ⚠️ Django 默认根路径没有配置页面，因此访问会显示 404 Page Not Found。
  根路径主要用于 API 状态或重定向，前端无需访问。

- API 接口路径 /api/
  例如：

  https://yalhardware-backend.onrender.com/api/products/

  前端 Vue 项目通过 Axios 调用这些接口获取产品数据。

- 后台管理 /admin/

```text
- https://yalhardware-backend.onrender.com/admin/

```

登录后可管理用户、组以及自定义模型（产品、首页内容等）。

---

## 🧠 未来优化方向

- 后台权限管理模块（基于角色 / 权限点控制）
- 单元测试覆盖（Django Tests），保障核心业务逻辑稳定性
- API 文档完善（Swagger / Postman）
- 部署流程优化及 CI/CD 自动化

## 📄 License

MIT
