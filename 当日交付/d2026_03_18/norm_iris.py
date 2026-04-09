# ================== 1. 导入依赖库 ==================
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import seaborn as sns

# ================== 2. 读取真实数据（鸢尾花） ==================
df = pd.read_csv("iris\iris.data", header=None, names=["sepal_l","sepal_w","petal_l","petal_w","species"])
data = df["petal_l"].values  # 花瓣长度 → 真实业务数据

# ================== 3. 绘制：直方图 + 拟合正态曲线 ==================
# 设置画图中文字体
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置中文字体为黑体
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

plt.figure(figsize=(14, 5))

# 左图：分布拟合图
plt.subplot(1, 2, 1)
# 真实数据直方图
sns.histplot(data, bins=15, stat="density", color="skyblue", alpha=0.7)
# 拟合正态曲线（scipy 自动算均值、标准差）
mu, sigma = stats.norm.fit(data)
x = np.linspace(min(data), max(data), 100)
y = stats.norm.pdf(x, mu, sigma)
plt.plot(x, y, "r-", lw=2, label="标准正态分布")
plt.title("花瓣长度分布 + 正态拟合曲线")
plt.legend()

# ================== 4. 绘制 QQ 图 ==================
plt.subplot(1, 2, 2)
stats.probplot(data, plot=plt)  # QQ 图核心代码
plt.title("QQ 图（越贴近对角线越正态）")
plt.tight_layout()
plt.show()

# ================== 5. Shapiro 正态性检验 ==================
print("="*50)
print("📊 Shapiro 正态性检验")
stat_sh, p_sh = stats.shapiro(data)
print(f"统计量 = {stat_sh:.4f}, p值 = {p_sh:.4f}")
print("结论：p > 0.05 → 服从正态；否则不服从\n")

# ================== 6. K-S 正态性检验 ==================
print("📊 K-S 正态性检验")
stat_ks, p_ks = stats.kstest(data, "norm", args=(mu, sigma))
print(f"统计量 = {stat_ks:.4f}, p值 = {p_ks:.4f}")
print("结论：p > 0.05 → 服从正态；否则不服从")
print("="*50)