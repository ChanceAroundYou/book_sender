# Book Sender 项目结构说明

## 1. 项目概述

Book Sender 是一个自动化书籍分发系统，主要功能包括：
- 自动爬取书籍信息
- 下载电子书文件
- 通过邮件分发给用户
- 支持多种存储方式（本地、S3、R2等）
- 支持多种分发方式（SMTP、SES等）
- 现代化React前端界面
- 异步任务处理系统

## 2. 目录结构

```
book_sender/
├── app/                    # 主应用目录
│   ├── admin/             # 管理后台模块
│   ├── api/               # API接口
│   │   ├── book.py        # 图书相关API
│   │   ├── user.py        # 用户相关API
│   │   ├── task.py        # 任务相关API
│   │   ├── download.py    # 下载相关API
│   │   ├── distribute.py  # 分发相关API
│   │   ├── crawl.py       # 爬虫相关API
│   │   └── utils.py       # API工具函数
│   ├── config.py          # 配置文件
│   ├── celery_app.py      # Celery配置
│   ├── main.py           # 应用入口
│   ├── database/         # 数据库模型
│   ├── distributor/      # 分发模块
│   ├── downloader/       # 下载模块
│   ├── crawler/          # 爬虫模块
│   ├── uploader/         # 上传模块
│   ├── utils/            # 工具类
│   └── task/             # 任务模块
├── frontend/              # 前端应用
│   ├── src/              # 源代码
│   │   ├── components/   # React组件
│   │   ├── pages/        # 页面组件
│   │   ├── store/        # Redux状态管理
│   │   ├── utils/        # 工具函数
│   │   └── types/        # TypeScript类型定义
│   ├── dist/             # 构建输出
│   ├── package.json      # 前端依赖
│   ├── vite.config.ts    # Vite配置
│   ├── tailwind.config.js # Tailwind配置
│   └── tsconfig.json     # TypeScript配置
├── docker/               # Docker配置
│   ├── Dockerfile        # 后端Dockerfile
│   └── docker-compose.yml # Docker Compose配置
├── docs/                  # 项目文档
├── tests/                # 测试用例
├── downloads/            # 下载目录
├── static/               # 静态资源
├── requirements.txt      # Python依赖
├── package.json          # 根目录package.json
├── run.py               # 启动脚本
└── pytest.ini          # 测试配置
```

## 3. 核心模块说明

### 3.1 API模块 (app/api/)
- 提供RESTful API接口
- 包含用户、书籍、任务、下载、分发、爬虫等接口
- 使用FastAPI框架实现
- 支持JWT认证
- 包含API工具函数和中间件

### 3.2 数据库模块 (app/database/)
- 使用SQLAlchemy ORM
- 包含用户、书籍、任务等数据模型
- 提供通用的CRUD操作
- 支持PostgreSQL和SQLite

### 3.3 分发模块 (app/distributor/)
- 支持多种分发方式（SMTP、SES）
- 处理邮件发送和文件分发
- 支持大文件云存储分发

### 3.4 下载模块 (app/downloader/)
- 支持多种下载方式
- 处理文件下载和存储
- 支持断点续传

### 3.5 爬虫模块 (app/crawler/)
- 支持多种网站爬取
- 提取书籍信息和下载链接
- 支持增量更新
- 使用Playwright、Selenium、BeautifulSoup等技术

### 3.6 上传模块 (app/uploader/)
- 支持多种存储方式（本地、S3、R2）
- 处理文件上传和URL生成
- 支持文件完整性校验

### 3.7 任务模块 (app/task/)
- 使用Celery实现异步任务
- 处理定时任务和调度
- 支持任务重试和监控

### 3.8 工具模块 (app/utils/)
- 提供通用工具函数
- 包含数据转换、图片处理等功能
- 支持文件压缩和格式转换

### 3.9 前端模块 (frontend/)
- 使用React 18 + TypeScript
- 基于Vite构建工具
- 使用Ant Design UI组件库
- Redux Toolkit状态管理
- Tailwind CSS样式框架
- 支持响应式设计

### 3.10 Docker模块 (docker/)
- 提供容器化部署方案
- Docker Compose多服务编排
- 支持开发和生产环境

## 4. 技术栈

### 后端技术栈
- **Web框架**: FastAPI 0.109.2
- **ASGI服务器**: Uvicorn 0.27.1
- **数据库ORM**: SQLAlchemy 2.0.27
- **数据库迁移**: Alembic 1.12.1
- **数据库驱动**: psycopg2-binary 2.9.9
- **认证**: python-jose[cryptography] 3.3.0
- **密码哈希**: passlib[bcrypt] 1.7.4
- **任务队列**: Celery >= 5.3.6
- **缓存**: Redis >= 5.0.1
- **HTTP客户端**: requests 2.31.0, httpx 0.26.0
- **爬虫工具**: 
  - beautifulsoup4 4.12.3
  - playwright 1.42.0
  - selenium 4.18.1
  - cloudscraper 1.2.71
- **云存储**: boto3 >= 1.34.0
- **日志**: loguru 0.7.0
- **配置管理**: pydantic-settings 2.1.0

### 前端技术栈
- **框架**: React 18.2.0
- **构建工具**: Vite 5.1.4
- **语言**: TypeScript 5.3.3
- **UI组件库**: Ant Design 5.14.2
- **状态管理**: Redux Toolkit 2.2.1
- **路由**: React Router DOM 6.22.1
- **样式**: Tailwind CSS 3.4.1
- **HTTP客户端**: Axios 1.6.7
- **图标**: Ant Design Icons 5.3.0

### 开发工具
- **代码格式化**: Black, isort
- **类型检查**: mypy
- **测试框架**: pytest
- **监控工具**: Flower (Celery监控)
- **容器化**: Docker, Docker Compose

## 5. 部署架构

- 使用Docker容器化部署
- 使用Nginx作为反向代理
- 支持HTTPS
- 支持多环境部署（开发、测试、生产）
- 使用Docker Compose进行服务编排

## 6. 开发规范

- 使用Python 3.8+
- 使用Node.js 20.0+
- 遵循PEP 8编码规范
- 使用Type Hints进行类型提示
- 编写单元测试
- 使用Black进行代码格式化
- 使用isort进行导入排序
- 使用mypy进行类型检查
- 前端使用ESLint进行代码检查
- 使用Prettier进行代码格式化

## 7. 环境配置

### 必需的环境变量
```env
# 数据库配置
POSTGRES_HOST=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=book_sender
POSTGRES_PORT=5432

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379

# 安全配置
SECRET_KEY=your_secret_key

# 存储配置
DB_DIR=app/db

# 其他配置
ACCESS_TOKEN_EXPIRE_MINUTES=11520
```

### 可选的环境变量
```env
# 云存储配置
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1
AWS_S3_BUCKET=your_bucket

# 邮件配置
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email
SMTP_PASSWORD=your_password
``` 