# Book Sender

一个自动下载图书并分发给用户的Python应用。

## 功能特点

- 自动抓取图书信息
- 支持多种图书格式（PDF, EPUB, MOBI）
- 用户管理系统
- 图书分发系统
- RESTful API接口

## 系统要求

- Python 3.8+
- PostgreSQL
- Redis

## 安装

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

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
创建 `.env` 文件并设置以下变量：
```
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=book_sender
REDIS_HOST=localhost
REDIS_PORT=6379
SECRET_KEY=your_secret_key
```

## 运行

1. 启动数据库：
```bash
# 确保PostgreSQL和Redis服务已启动
```

2. 运行应用：
```bash
uvicorn app.main:app --reload
```

3. 访问API文档：
```
http://localhost:8000/docs
```

## 项目结构

```
book_sender/
├── app/
│   ├── api/            # API路由
│   ├── crawler/        # 图书抓取器
│   ├── distributor/    # 图书分发器
│   ├── models/         # 数据模型
│   ├── core/           # 核心配置
│   └── utils/          # 工具函数
├── static/             # 静态文件
├── templates/          # 模板文件
├── requirements.txt    # 项目依赖
└── README.md          # 项目文档
```

## API文档

启动应用后，访问 `/docs` 路径查看完整的API文档。

## 许可证

MIT 