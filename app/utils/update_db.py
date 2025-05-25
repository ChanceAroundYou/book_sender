import psycopg2
from psycopg2 import Error

# 数据库连接参数
db_params = {
    'host': '192.168.1.6',
    'port': '25432',
    'database': 'postgres',
    'password': 'postgres',
    'user': 'postgres'
}

try:
    # 建立数据库连接
    conn = psycopg2.connect(**db_params)
    
    # 创建游标对象
    cursor = conn.cursor()
    
    # SQL语句：重命名列
    alter_query = "ALTER TABLE books RENAME COLUMN category TO series;"
    
    # 执行SQL语句
    cursor.execute(alter_query)
    
    # 提交更改
    conn.commit()
    
    print("列名修改成功：category -> series")

except (Exception, Error) as error:
    print("数据库操作出错:", error)

finally:
    # 关闭数据库连接
    if 'conn' in locals():
        if cursor:
            cursor.close()
        conn.close()
        print("数据库连接已关闭")