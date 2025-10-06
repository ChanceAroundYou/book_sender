# Book Sender

一个自动下载图书并分发给用户的Python应用，包含现代化的前端界面。

## 功能特点

- 自动抓取图书信息
- 支持多种图书格式（PDF, EPUB, MOBI）
- 用户管理系统
- 图书分发系统
- RESTful API接口
- 现代化React前端界面
- 异步任务处理
- 多种存储方式支持

## 系统要求

- Python 3.8+
- Node.js 20.0+
- PostgreSQL
- Redis

## 项目结构

```
book_sender/
├── app/                    # 后端应用目录
│   ├── admin/             # 管理后台
│   ├── api/               # API路由
│   │   ├── book.py        # 图书相关API
│   │   ├── user.py        # 用户相关API
│   │   ├── task.py        # 任务相关API
│   │   ├── download.py    # 下载相关API
│   │   ├── distribute.py  # 分发相关API
│   │   ├── crawl.py       # 爬虫相关API
│   │   └── utils.py       # API工具函数
│   ├── crawler/           # 图书抓取器
│   ├── database/          # 数据库模型
│   ├── distributor/       # 图书分发器
│   ├── downloader/        # 下载模块
│   ├── task/              # 异步任务
│   ├── uploader/          # 文件上传
│   ├── utils/             # 工具函数
│   ├── config.py          # 配置文件
│   ├── celery_app.py      # Celery配置
│   └── main.py           # 应用入口
├── frontend/              # 前端应用
│   ├── src/              # 源代码
│   ├── dist/             # 构建输出
│   ├── package.json      # 前端依赖
│   └── vite.config.ts    # Vite配置
├── docker/               # Docker配置
│   ├── Dockerfile        # 后端Dockerfile
│   └── docker-compose.yml # Docker Compose配置
├── docs/                 # 项目文档
├── tests/                # 测试用例
├── downloads/            # 下载目录
├── static/               # 静态文件
├── requirements.txt      # Python依赖
├── package.json          # 根目录package.json
└── run.py               # 启动脚本
```

## 安装

### 后端安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/book_sender.git
cd book_sender
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装Python依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
创建 `.env` 文件并设置以下变量：
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

# 其他配置
ACCESS_TOKEN_EXPIRE_MINUTES=11520
```

### 前端安装

1. 进入前端目录：
```bash
cd frontend
```

2. 安装依赖：
```bash
npm install
```

## 运行

### 使用Docker（推荐）

1. 使用Docker Compose启动所有服务：
```bash
docker-compose up -d
```

### 手动运行

1. 启动数据库服务：
```bash
# 确保PostgreSQL和Redis服务已启动
```

2. 启动后端服务：
```bash
# 在项目根目录
python run.py
# 或
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

3. 启动前端开发服务器：
```bash
cd frontend
npm run dev
```

4. 启动Celery工作进程（可选）：
```bash
celery -A app.celery_app worker --loglevel=info
```

5. 启动Celery监控（可选）：
```bash
celery -A app.celery_app flower
```
book_sender/
├── app/
│   ├── admin/          
│   ├── api/            # API路由
│   ├── crawler/        # 图书抓取器
│   ├── database/
│   ├── distributor/    # 图书分发器
│   ├── downloader/            # API路由
│   ├── task/            
│   ├── uploader/            # API路由
│   └── utils/          # 工具函数
├── static/             # 静态文件
├── templates/          # 模板文件
├── requirements.txt    # 项目依赖
└── README.md          # 项目文档
```

## API文档

启动应用后，访问 `/docs` 路径查看完整的API文档。

## 开发

### 代码格式化
```bash
# Python代码格式化
black app/
isort app/

# TypeScript代码格式化
cd frontend
npm run lint
```

### 测试
```bash
# 运行Python测试
pytest

# 运行前端测试
cd frontend
npm test
```

## 许可证

MIT 