import random
import string
from datetime import UTC, datetime, timedelta
from typing import List

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api import get_request_params
from app.database import User, get_depend_db

# JWT相关配置
SECRET_KEY = "your-secret-key-keep-it-secret"  # 在生产环境中应该使用环境变量
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 请求模型
class UserCreate(BaseModel):
    email: str
    password: str
    username: str | None = None


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


router = APIRouter()


def generate_random_username(email: str, db: Session) -> str:
    """生成随机用户名"""
    # 从邮箱获取基础用户名
    base = email.split("@")[0]
    # 如果基础用户名少于3个字符，补充随机字符
    if len(base) < 3:
        base += "".join(random.choices(string.ascii_lowercase, k=3 - len(base)))

    username = base
    # 如果用户名已存在，添加随机数字直到找到可用的用户名
    counter = 1
    while User.query_first(db, username=username):
        username = f"{base}{counter}"
        counter += 1

    return username


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt).decode()


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_depend_db)
):
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not (email := payload.get("sub")):
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = User.query_first(db, email=email)
    if not user:
        raise credentials_exception
    return user


@router.post("/register", response_model=dict)
async def register(user: UserCreate, db: Session = Depends(get_depend_db)):
    """用户注册"""
    # 检查邮箱是否已存在
    if User.query_first(db, email=user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="该邮箱已被注册"
        )

    # 生成用户名（如果未提供）
    username = user.username or generate_random_username(user.email, db)

    # 创建新用户
    hashed_password = get_password_hash(user.password)
    db_user = User.create(
        db, username=username, email=user.email, hashed_password=hashed_password
    )
    return db_user.to_dict()


@router.post("/login", response_model=Token)
async def login(
    user_login: UserLogin,
    db: Session = Depends(get_depend_db),
):
    """用户登录"""
    # 通过邮箱查找用户
    user = User.query_first(db, email=user_login.email)
    if not user or not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 生成访问令牌
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=dict)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return current_user.to_dict()


@router.get("/users", response_model=List[dict])
async def get_users_api(request: Request, db: Session = Depends(get_depend_db)):
    """获取用户列表"""
    params = await get_request_params(request)
    params.setdefault("limit", 50)

    users = User.query(db, **params)
    return [user.to_dict() for user in users]


@router.get("/users", response_model=dict)
async def get_user_api(request: Request, db: Session = Depends(get_depend_db)):
    """获取用户详情"""
    params = await get_request_params(request)
    user_id = params.get("user_id", None)
    if user_id is None:
        raise HTTPException(status_code=400, detail="User ID is required")

    user = User.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.to_dict()


@router.post("/users", response_model=dict)
async def create_user_api(request: Request, db: Session = Depends(get_depend_db)):
    """创建用户"""
    params = await get_request_params(request)
    user = User.create(db, **params)
    return user.to_dict()


@router.put("/users", response_model=dict)
async def update_user_api(request: Request, db: Session = Depends(get_depend_db)):
    """更新用户"""
    params = await get_request_params(request)
    user_id = params.get("user_id", None)
    if user_id is None:
        raise HTTPException(status_code=400, detail="User ID is required")

    user = User.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.update(**params)
    return user.to_dict()


@router.delete("/users", response_model=dict)
async def delete_user_api(request: Request, db: Session = Depends(get_depend_db)):
    """删除用户"""
    params = await get_request_params(request)
    user_id = params.get("user_id", None)
    if user_id is None:
        raise HTTPException(status_code=400, detail="User ID is required")

    user = User.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.delete()
    return {"message": "User deleted successfully"}


@router.put("/users/subscriptions")
async def add_user_subscription_api(
    request: Request, db: Session = Depends(get_depend_db)
):
    """添加用户订阅"""
    params = await get_request_params(request)
    user_id = params.get("user_id", None)
    if user_id is None:
        raise HTTPException(status_code=400, detail="User ID is required")

    series = params.get("series", "")
    date = params.get("date", "")

    if not series:
        raise HTTPException(status_code=400, detail="Series is required")

    user = User.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.add_subscription(series, date)
    return user.to_dict()


@router.delete("/users/subscriptions")
async def remove_user_subscription_api(
    request: Request, db: Session = Depends(get_depend_db)
):
    """删除用户订阅"""
    params = await get_request_params(request)
    user_id = params.get("user_id", None)
    if user_id is None:
        raise HTTPException(status_code=400, detail="User ID is required")

    series = params.get("series", "")

    if not series:
        raise HTTPException(status_code=400, detail="Series is required")

    user = User.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.remove_subscription(series)
    return user.to_dict()


@router.post("/forgot-password", response_model=dict)
async def forgot_password(email: str, db: Session = Depends(get_depend_db)):
    """忘记密码"""
    if not User.query_first(db, email=email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="该邮箱未注册"
        )

    # TODO: 实现发送重置密码邮件的逻辑

    return {"message": "重置密码链接已发送到您的邮箱"}
