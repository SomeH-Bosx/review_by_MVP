"""
Pandas 读取Excel/CSV文件并完成基础数据查看
功能：
1. 读取Excel/CSV文件
2. 基础数据查看（维度、前/后行、数据类型、描述性统计等）
3. 异常处理（文件不存在、格式错误等）
所需依赖：pandas openpyxl
"""

import pandas as pd
import os

def read_and_view_file(file_path):
    """
    读取文件并展示基础信息
    :param file_path：文件路径（支持 .xlsx / .csv）
    :return：读取后的DataFrame（失败返回None）
    """

    # 1. 检验文件是否存在

    if not os.path.exists(file_path):
        print(f"错误：文件{file_path} 不存在！")
        return None
    
    # 2. 根据文件后缀选择读取方式
    try:
        if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            # 读取Excel文件（默认读取第一个工作表
            df = pd.read_excel(file_path, sheet_name=0)
            file_type = "Excel"
        elif file_path.endswith('.csv'):
            # 读取CSV文件（自动适配编码，避免中文乱码）
            df = pd.read_csv(file_path, encoding='utf-8-sig')
            file_type = "CSV"
        else:
            print(f"错误：不支持的文件格式！仅支持 .xlsx/.xls/.csv")
            return None
    
        # 3.基础数据查看
        print("="*50)
        print(f"✅️ 成功读取{file_type} 文件： {file_path}")
        print('='*50)

        # 3.1 查看数据维度（行数、列数）
        print(f"\n1. 数据维度（行×列）：{df.shape}")

        # 3.2 查看前5行数据
        print(f"\n2. 前5行数据：")
        print(df.head())

        # 3.3 查看后3行数据
        print(f"\n3. 后3行数据：")
        print(df.tail(3))

        # 3.4 查看数据类型（避免后续处理类型错误）
        print(f"\n4. 各列数据类型：")
        print(df.dtypes)

        # 3.5 查看描述性统计（仅数值列）
        print(f"\n5. 数值列描述性统计（均值、标准差、最值等）：")
        print(df.describe())

        # 3.6 查看空值情况（关键：处理缺失值前的检查）
        print(f"\n6. 各列空值数量：")
        print(df.isnull().sum())

        # 3.7 查看列名（方便后续按列操作）
        print(f"\n7. 所有列名：")
        print(df.columns.tolist())

        return df

    except Exception as e:
        print(f"读取文件失败！错误信息：{str(e)}")
        return None
# 主函数：测试示例
if __name__=='__main__':
    #-----------------------
    #替换为你的文件路径
    #-----------------------
    #示例1：读取 Excel 文件
    file_path = 'users.xlsx'

    # 执行读取和查看
    df = read_and_view_file(file_path)

    # 如果读取成功，可在此处继续处理数据
    if df is not None:
        print("\n✅️ 数据读取完成，可继续后续分析/处理！")


