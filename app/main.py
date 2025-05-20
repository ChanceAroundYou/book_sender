from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import BaseModel, engine
from app.api import book, crawl, download, user, distribute, task

# 创建数据库表
BaseModel.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(book.router, prefix=settings.API_V1_STR, tags=["book"])
app.include_router(user.router, prefix=settings.API_V1_STR, tags=["user"])
app.include_router(download.router, prefix=settings.API_V1_STR, tags=["download"])
app.include_router(crawl.router, prefix=settings.API_V1_STR, tags=["crawl"])
app.include_router(distribute.router, prefix=settings.API_V1_STR, tags=["distribute"])
app.include_router(task.router, prefix=settings.API_V1_STR, tags=["task"])

@app.get("/")
async def root():
    return {"message": "Welcome to Book Sender API"} 