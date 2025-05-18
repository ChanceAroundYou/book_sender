import argparse

from sqlalchemy import MetaData, Table, create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError

from app.config import settings


def list_all_tables(engine):
    """列出数据库中的所有表"""
    inspector = inspect(engine)
    return inspector.get_table_names()


def delete_table(table_name: str):
    """删除指定的表"""
    try:
        # 创建数据库引擎
        engine = create_engine(settings.DATABASE_URL)

        # 获取现有表列表
        existing_tables = list_all_tables(engine)
        if table_name not in existing_tables:
            print(f"错误: 表 '{table_name}' 不存在")
            print(f"可用的表: {', '.join(existing_tables)}")
            return False

        # 使用元数据反射现有表
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=engine)

        # 删除表
        metadata.drop_all(engine, tables=[table])
        print(f"成功删除表 '{table_name}'")
        return True

    except SQLAlchemyError as e:
        print(f"数据库错误: {str(e)}")
        return False
    except Exception as e:
        print(f"发生未知错误: {str(e)}")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="数据库表删除工具")
    parser.add_argument("table", nargs="?", help="要删除的表名")
    parser.add_argument("-l", "--list", action="store_true", help="列出所有可用的表")
    args = parser.parse_args()

    engine = create_engine(settings.DATABASE_URL)

    if args.list:
        tables = list_all_tables(engine)
        print("可用的表:")
        for table in tables:
            print(f"- {table}")
        return

    if not args.table:
        parser.print_help()
        return

    delete_table(args.table)


if __name__ == "__main__":
    main()
