from app.config import settings


def test_env_variables():
    """测试环境变量是否正确加载"""
    # 打印一些关键配置（注意不要打印敏感信息）
    print("\n=== 环境变量加载测试 ===")
    print(f"数据库主机: {settings.POSTGRES_SERVER}")
    print(f"Redis主机: {settings.REDIS_HOST}")
    print(f"AWS区域: {settings.AWS_REGION}")
    print(f"邮件后端: {settings.EMAIL_BACKEND}")
    
if __name__ == "__main__":
    test_env_variables()