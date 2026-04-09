"""
将MySQL表导出为CVS/Excel格式
支持单表/多表批量导出，避免中文乱码
所需依赖：pandas pymysql openpyxl
"""

import pandas as pd
import pymysql

def export_mysql_to_file(
        host='localhost',
        port=3306,
        user='root',
        password='Mysql111.',
        db='demo1',
        tables=['users', 'products', 'orders'], # 要导出的表名列表
        export_format='xlsx',
        save_path='./'  # 保存路径（默认当前目录）
):
    """
    导出MySQL表到文件
    """
    # 1.链接数据库
    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            db=db,
            charset='utf8mb4'  # 解决中文乱码
        )
        print(f"✅️ 成功连接数据库：{db}")

        # 2. 遍历表名，逐个导出
        for table in tables:
            # 2.1 读取表数据到DataFrame
            sql = f"select * from {table}"
            df = pd.read_sql(sql, conn)

            # 2.2 定义文件名
            file_name = f"{save_path}{table}.{export_format}"

            # 2.3 导出为指定格式
            if export_format == 'xlsx':
                df.to_excel(file_name, index=False, engine='openpyxl')
            elif export_format == 'csv':
                df.to_csv(file_name, index=False, encoding='utf-8-sig')  # utf-8-sig解决中文乱码)
            else:
                print(f"❌️ 不支持的导出格式：{export_format}")
                continue

            print(f"✅️ 表{table}已导出到：{file_name}")

    except Exception as e:
        print(f"❌️ 导出失败！错误信息：{str(e)}")
    finally:
        # 关闭数据库连接
        if 'conn' in locals() and conn.open:
            conn.close()
            print("✅️ 数据库连接已关闭")

# 主函数：执行导出
if __name__ == "__main__":
    # 配置参数（替换为真实数据库信息）
    export_mysql_to_file(
        password='Mysql111.',
        db='demo1',
        tables=['users', 'products', 'orders'],  # 要导出的表名列表
        export_format='xlsx',  # 导出格式：xlsx或csv
        save_path='./'  # 保存路径（默认当前目录）
    )