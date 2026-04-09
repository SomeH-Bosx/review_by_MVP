# iris鸢尾花数据集做分析


"""
鸢尾花（Iris）数据集描述性统计分析
功能：
1. 读取鸢尾花原始数据文件（.data）格式
2. 为数据集添加列名
3. 计算全套描述性统计指标
4. 输出清晰的统计结果
"""

import pandas as pd
import numpy as np

# --------------------------
# 1. 读取鸢尾花数据集
# --------------------------
# 注意：请根据你的实际路径修改文件路径
# 这里假设 iris.data 和代码在同一目录下
file_path = ".\iris\iris.data"  # 若路径不同，改为："E:/.../iris/iris.data"

# 读取.data文件（逗号分隔，无表头）
df = pd.read_csv(
    file_path,
    header=None,  # 原始数据无列名
    names=[
        "sepal_length",  # 花萼长度(cm)
        "sepal_width",   # 花萼宽度(cm)
        "petal_length",  # 花瓣长度(cm)
        "petal_width",   # 花瓣宽度(cm)
        "species"        # 品种（标签列）
    ]
)

# --------------------------
# 2. 基础数据预览
# --------------------------
print("=" * 60)
print("📊 鸢尾花数据集基础信息预览")
print("=" * 60)

print("\n1. 数据维度（行数 × 列数）：", df.shape)
print("\n2. 前5行数据：")
print(df.head())

print("\n3. 各列数据类型：")
print(df.dtypes)

print("\n4. 缺失值统计：")
print(df.isnull().sum())  # 鸢尾花数据集无缺失值，用于验证

# --------------------------
# 3. 分离数值型特征（仅对数值列做统计）
# --------------------------
numeric_cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
df_numeric = df[numeric_cols]


# 4.2 手动计算补充指标（更全面）
stats_df = pd.DataFrame()  # 相当与创建一个新的表格

# 均值：所有数据的算术平均值，反映数据集中趋势
stats_df["均值(mean)"] = df_numeric.mean()
# 中位数：排序后中间位置的值，不受极端值影响，反映集中趋势
stats_df["中位数(median)"] = df_numeric.median()
# 众数：出现次数最多的值，反映数据集中趋势（离散特征更有意义）
stats_df["众数(mode)"] = [df_numeric[col].mode().iloc[0] for col in numeric_cols]
# 极差：最大值 - 最小值，反映数据离散程度
stats_df["极差(range)"] = df_numeric.max() - df_numeric.min()
# 方差：各数据与均值差的平方的平均数，反映离散程度
stats_df["方差(var)"] = df_numeric.var(ddof=0)  # ddof=0 为总体方差
# 标准差：方差的平方根，单位与原数据一致，更直观反映离散程度
stats_df["标准差(std)"] = df_numeric.std(ddof=0)
# 变异系数：标准差 / 均值，用于不同量纲数据间比较离散程度
stats_df["变异系数(cv)"] = stats_df["标准差(std)"] / stats_df["均值(mean)"]
# 四分位数：反映数据位置分布
stats_df["25%分位数(Q1)"] = df_numeric.quantile(0.25)
stats_df["50%分位数(Q2/中位数)"] = df_numeric.quantile(0.5)
stats_df["75%分位数(Q3)"] = df_numeric.quantile(0.75)
# 四分位距(IQR)：Q3 - Q1，用于识别异常值
stats_df["四分位距(IQR)"] = stats_df["75%分位数(Q3)"] - stats_df["25%分位数(Q1)"]
# 偏度：反映数据分布的不对称性，>0右偏，<0左偏
stats_df["偏度(skew)"] = df_numeric.skew()
# 峰度：反映数据分布的陡峭程度，>0尖峰，<0平峰
stats_df["峰度(kurt)"] = df_numeric.kurt()

print("\n✅ 完整描述性统计指标：")
print(stats_df.round(4))  # 保留4位小数，便于阅读

# --------------------------
# 5. 按品种分组统计（进阶分析）
# --------------------------
print("\n" + "=" * 60)
print("🌸 按鸢尾花品种分组统计（均值）")
print("=" * 60)
print(df.groupby("species")[numeric_cols].mean().round(4))

# --------------------------
# 6. 保存统计结果到文件（可选）
# --------------------------
stats_df.to_csv("./iris_descriptive_stats.csv", encoding="utf-8-sig")
print("\n💾 完整统计结果已保存到：./iris_descriptive_stats.csv")