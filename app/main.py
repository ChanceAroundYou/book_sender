from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api import book, crawl, distribute, download, task, user, utils
from app.config import settings
from app.database import BaseModel, engine

# 创建数据库表
BaseModel.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.debug(f"Request headers: {request.headers}")
    response = await call_next(request)
    logger.debug(f"Response headers: {response.headers}")
    return response


# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
    expose_headers=["*"],
    max_age=3600,
)

# 注册路由
app.include_router(book.router, prefix=settings.API_V1_STR, tags=["book"])
app.include_router(user.router, prefix=settings.API_V1_STR, tags=["user"])
app.include_router(download.router, prefix=settings.API_V1_STR, tags=["download"])
app.include_router(crawl.router, prefix=settings.API_V1_STR, tags=["crawl"])
app.include_router(distribute.router, prefix=settings.API_V1_STR, tags=["distribute"])
app.include_router(task.router, prefix=settings.API_V1_STR, tags=["task"])
app.include_router(utils.router, prefix=settings.API_V1_STR, tags=["utils"])


@app.get("/")
async def root():
    return {"message": "Welcome to Book Sender API"}
