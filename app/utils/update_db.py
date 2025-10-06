import psycopg2
from config import settings
from psycopg2 import Error

# 数据库连接参数
db_params = {
    "connection_factory": None,
    "cursor_factory": None,
    "host": settings.POSTGRES_HOST,
    "port": settings.POSTGRES_PORT,
    "database": settings.POSTGRES_DB,
    "password": settings.POSTGRES_PASSWORD,
    "user": settings.POSTGRES_USER,
}

try:
    # Build the connection
    conn = psycopg2.connect(**db_params)
    # Create a cursor object
    cursor = conn.cursor()

    # SQL statement: rename column
    # This operation renames the category column in the books table to series.
    # Prerequisites: The books table must exist, and the category column must also exist, otherwise an error will be reported.
    alter_query = "ALTER TABLE books RENAME COLUMN category TO series;"

    # Execute SQL statement
    cursor.execute(alter_query)

    # Commit changes
    conn.commit()
    print("Column name changed successfully: category -> series")

except (Exception, Error) as error:
    print("Database operation error:", error)

finally:
    # Close database connection
    if "conn" in locals() and (conn := locals()["conn"]):
        if "cursor" in locals() and (cursor := locals()["cursor"]):
            cursor.close()
        conn.close()
        print("Database connection closed")
