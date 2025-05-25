# Book Sender 项目结构说明

## 1. 项目概述

Book Sender 是一个自动化书籍分发系统，主要功能包括：
- 自动爬取书籍信息
- 下载电子书文件
- 通过邮件分发给用户
- 支持多种存储方式（本地、S3、R2等）
- 支持多种分发方式（SMTP、SES等）

## 2. 目录结构

```
book_sender/
├── app/                    # 主应用目录
│   ├── api/               # API接口
│   ├── config.py          # 配置文件
│   ├── celery_app.py      # Celery配置
│   ├── main.py           # 应用入口
│   ├── database/         # 数据库模型
│   ├── distributor/      # 分发模块
│   ├── downloader/       # 下载模块
│   ├── crawler/          # 爬虫模块
│   ├── uploader/         # 上传模块
│   ├── utils/            # 工具类
│   ├── task/             # 任务模块
│   └── static/           # 静态资源
├── docs/                  # 项目文档
├── tests/                # 测试用例
├── downloads/            # 下载目录
└── requirements.txt      # 依赖文件
```

## 3. 核心模块说明

### 3.1 API模块 (app/api/)
- 提供RESTful API接口
- 包含用户、书籍、任务、下载、分发、爬虫等接口
- 使用FastAPI框架实现

### 3.2 数据库模块 (app/database/)
- 使用SQLAlchemy ORM
- 包含用户、书籍、任务等数据模型
- 提供通用的CRUD操作

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

## 4. 技术栈

- 后端框架：FastAPI
- 数据库：PostgreSQL
- 缓存：Redis
- 任务队列：Celery
- ORM：SQLAlchemy
- 存储：AWS S3/Cloudflare R2
- 邮件服务：SMTP/SES
- 文档：OpenAPI/Swagger

## 5. 部署架构

- 使用Docker容器化部署
- 使用Nginx作为反向代理
- 支持HTTPS

## 6. 开发规范

- 使用Python 3.12+
- 遵循PEP 8编码规范
- 使用Type Hints进行类型提示
- 编写单元测试
- 使用Black进行代码格式化
- 使用isort进行导入排序
- 使用mypy进行类型检查 