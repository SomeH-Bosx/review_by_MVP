# import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# load the dataset
# 使用seaborn自带的鸢尾花数据集
df1 = sns.load_dataset('iris')

# 读取本地iris.data文件
# 列名
columns = ["sepal_length", "speal_width", "petal_length", "petal_width", "species"]

# 读取本地iris.data文件
df2 = pd.read_csv("iris/iris.data", header=None, names=columns)

# 只保留数值变量
df1_numeric = df1.select_dtypes(include=[np.number])
df2_numeric = df2.select_dtypes(include=[np.number])

# 计算皮尔逊相关系数
corr_matrix1 = df1_numeric.corr(method="pearson")
corr_matrix2 = df2_numeric.corr(method="pearson")

print("===== 皮尔逊相关系数矩阵 =====")
print("seaborn自带数据集:{}".format(corr_matrix1.round(2)))
print("本地iris.data文件:{}".format(corr_matrix2.round(2)))
save_path = "pearson_correlation_matrix.txt"
with open(save_path, "w") as f:
    f.write("===== 皮尔逊相关系数矩阵 =====\n")
    f.write("seaborn自带数据集:\n{}\n".format(corr_matrix1.round(2)))
    f.write("本地iris.data文件:\n{}\n".format(corr_matrix2.round(2)))

# 绘制热力图
# 设置绘图字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为SimHei
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

plt.figure(figsize=(12, 8))
plt.subplot(1, 2, 1)
sns.heatmap(
    corr_matrix1,
    annot=True,
    cmap="coolwarm",
    vmax=1, vmin=-1,
    linewidths=0.5,
    fmt='.2f'
)
plt.title("自带数据集的皮尔逊相关系数热力图", fontsize=14)
plt.tight_layout()
plt.subplot(1, 2, 2)
sns.heatmap(
    corr_matrix2,
    annot=True,
    cmap="RdBu_r",
    vmax=1, vmin=-1,
    linewidths=0.5,
    fmt='.2f'
)
plt.title("本地Iris数据集的皮尔逊相关系数热力图", fontsize=14)
plt.tight_layout()

plt.savefig("pearson_correlation_heatmap.png", dpi=300)
plt.show()