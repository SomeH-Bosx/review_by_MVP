import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# 生成标准正态分布数据
np.random.seed(666)
data = np.random.normal(loc=50, scale=10, size=10000) # 均值50， 标准差10
df = pd.DataFrame(data, columns=["value"])

# 验证正态分布核心指标
print("均值：", round(df["value"].mean(), 2))
print("中位数：", round(df["value"].median(), 2))
print("众数（近似）：", round(df["value"].mode()[0], 2))
print("标准差：", round(df["value"].std(), 2))

# 绘制分布图
plt.figure(figsize=(10, 5))
plt.hist(data, bins=50, density=True, alpha=0.7, color="skyblue") # 绘制直方图

# 绘制密度曲线
x = np.linspace(20, 80, 1000)
y = stats.norm.pdf(x, 50, 10)
plt.plot(x, y, "r-", linewidth=2)
plt.title("Normal Distribution (μ=50， σ=10)")
plt.xlabel("Value")
plt.ylabel("Density")
plt.grid(alpha=0.3)
plt.show()