# 2026.03.16

——实现日期：2026年3月18日

2026年3月23日

## 一、本地MySQL 环境跑通，完成 3张基础表的创建与数据增删改查

本地MySQL环境已跑通✅️

三张基础表的创建以及增删改查：[demo1(three_table_CRUD)](E:\系统默认\桌面\Plan\求职\实践\当日交付\d2026_03_16\demo1(three_table_CRUD).sql)

```sql
-- 创建数据库demo1【默认属性】
create
    database if not exists
    demo1
    default charset utf8mb4;

use demo1;
show tables;

-- 以基础业务系统为例子：
-- 完成用户表、商品表、订单表的创建，以及完整的正删改查

-- 创建
-- 1. 用户表（user):存储用户基础信息
create table if not exists users (
    id int primary key auto_increment comment '用户ID（主键，自增）',
    username varchar(50) not null unique comment '用户名（唯一',
    password varchar(100) not null comment '密码（建议加密存储）',
    phone varchar(20) comment '手机号',
    create_time datetime default current_timestamp comment '创建时间'
) comment = '用户表';

-- 2. 商品表（products）：存储商品信息
create table if not exists products(
    id int primary key auto_increment comment '商品ID（主键，自增）',
    product_name varchar(100) not null comment '商品名称',
    price decimal(10, 2) not null comment '商品价格（保留2位小数）',
    stock int default 0 comment '商品库存',
    create_time datetime default current_timestamp comment '创建时间'
) comment = '商品表';

-- 3. 订单表（orders）：存储用户下单信息（关联用户和商品）
create table if not exists orders(
    id int primary key auto_increment comment '订单ID（主键，自增）',
    user_id int not null comment '关联用户ID',
    product_id int not null  comment '关联商品表ID',
    order_num varchar(50) not null unique comment '订单编号',
    amount decimal(10, 2) not null comment '订单金额',
    create_time datetime default current_timestamp comment '创建时间',

    -- 外键关联（增强数据完整性）
    foreign key (user_id) references users(id) on delete cascade,
    foreign key (product_id) references products(id) on delete cascade -- 级联删除（主表删，从表关联数据页删）
) comment = '订单表';

-- 数据的增删改查操作（CRUD）
-- 1.新增数据（create）

-- 新增用户
insert into users(username, password, phone)
values('zhangsan', '123456', '13800138000'),
      ('lisi', '654321', '13900139000');

-- 新增商品
insert into products(product_name, price, stock)
values('小米手机', 1999.99, 100),
      ('华为手机', 299.99, 500);

-- 新增订单（关联用户ID=1,商品ID=1）
insert into orders(user_id, product_id, order_num, amount)
values(1, 1, 'order20260323001', 1999.99),
      (2, 2, 'order20260323002', 299.99);


-- 2. 查询数据（read）【涵盖单表、多表以及条件查询】
-- 查询所有用户
select * from users;

-- 查询价格 < 500的商品（条件）
select id, products.product_name, price from products where price < 500;

-- 关联查询：查询订单详情（包含用户名、商品名）
select
    o.id as 订单ID,
    u.username as 用户名,
    p.product_name as 商品名,
    o.order_num as 订单编号,
    o.amount as 订单金额
from orders o
join users u on o.user_id = u.id
join products p on o.product_id = p.id;


-- 3. 修改数据（update）
-- 修改用户手机号（条件：用户名=zhangsan）
update users set phone = '138111138111' where username = 'zhangsan';

-- 修改商品库存（条件：商品ID = 1）
update products set stock = 99 where id = 1;

-- 修改订单金额（条件：订单编号=order20260323002）
update orders set amount = 289.99 where order_num = 'order20260323002';


-- 4. 删除数据（delete）
-- 删除指定用户（条件：ID=2，注意：外键级联删除会同步删除该用户的订单）、
delete from users where id = 2;

-- 删除库存为0的商品（当前无符合条件数据）【可正常运行不报错】
delete from products where stock = 0;

-- 删除指定订单（条件：ID=1)
delete from orders where id = 1;
```



* 关键规则：ON DELETE CASCADE（级联删除）

  * `ON DELETE CASCADE` 是外键的**删除规则**，意思是：

    - 当 `users` 表中某条用户记录被删除时，`orders` 表中所有关联该用户（`user_id` 匹配）的订单会**自动被删除**；
    - 当 `products` 表中某条商品记录被删除时，`orders` 表中所有关联该商品（`product_id` 匹配）的订单会**自动被删除**。

    |        规则        |                 含义                 |                   适用场景                   |
    | :----------------: | :----------------------------------: | :------------------------------------------: |
    | ON DELETE CASCADE  | 级联删除（主表删，从表关联数据也删） |          订单依赖用户 / 商品的场景           |
    | ON DELETE SET NULL |    主表删，从表关联字段设为 NULL     | 评论依赖用户（用户删了，评论保留但作者为空） |
    | ON DELETE RESTRICT |  主表有关联数据时，禁止删除主表记录  | 核心数据（如商品分类，不允许删有商品的分类） |

    ### 总结

==工具的选择🔧：DataGrip✅️==



## 二、 Pandas 完成Excel/CSV 文件的读取与基础查看，输出可运行代码文件

### 1. 创建并激活虚拟环境发生报错：

```cmd
python -m venv demo1
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Users\SomeH\AppData\Local\Programs\Python\Python311\Lib\venv\__main__.py", line 6, in <module>
    main()
  File "C:\Users\SomeH\AppData\Local\Programs\Python\Python311\Lib\venv\__init__.py", line 546, in main
    builder.create(d)
  File "C:\Users\SomeH\AppData\Local\Programs\Python\Python311\Lib\venv\__init__.py", line 76, in create
    self._setup_pip(context)
  File "C:\Users\SomeH\AppData\Local\Programs\Python\Python311\Lib\venv\__init__.py", line 358, in _setup_pip
    self._call_new_python(context, '-m', 'ensurepip', '--upgrade',
  File "C:\Users\SomeH\AppData\Local\Programs\Python\Python311\Lib\venv\__init__.py", line 354, in _call_new_python
    subprocess.check_output(args, **kwargs)
  File "C:\Users\SomeH\AppData\Local\Programs\Python\Python311\Lib\subprocess.py", line 466, in check_output
    return run(*popenargs, stdout=PIPE, timeout=timeout, check=True,
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\SomeH\AppData\Local\Programs\Python\Python311\Lib\subprocess.py", line 550, in run  
    stdout, stderr = process.communicate(input, timeout=timeout)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\SomeH\AppData\Local\Programs\Python\Python311\Lib\subprocess.py", line 1196, in communicate
    stdout = self.stdout.read()
             ^^^^^^^^^^^^^^^^^^
KeyboardInterrupt
```

#### a. 报错原因分析

你的报错核心是 `KeyboardInterrupt`（键盘中断），大概率是以下原因：

- 创建虚拟环境时，系统正在下载 / 安装`pip`（`ensurepip`模块），过程中你手动按了`Ctrl+C`中断；
- 网络问题导致`pip`下载超时，触发中断；
- Python 安装不完整，`venv`/`ensurepip`模块缺失。

#### b. 分步修复方案

##### 方案 1：重新创建（跳过 pip 安装，最快）

创建虚拟环境时，暂时跳过`pip`的自动安装，避免中断：

```bash
# 核心命令：--without-pip 跳过pip安装
python -m venv demo1 --without-pip
```

✅ 执行后若无报错，虚拟环境已创建成功，后续手动安装 pip 即可：

```bash
# 1. 激活虚拟环境（Windows cmd）
demo1\Scripts\activate.bat

# 2. 手动安装pip（激活后执行）
python -m ensurepip --upgrade
```

### 2. 下载依赖时未能正确下载在虚拟环境当中

#### a.原因分析

一、核心问题定位

从你的终端输出可以看出：

1. 虽然终端显示 `(demo1)`，但 `where python` 无任何返回，说明**PowerShell 环境变量解析异常**，系统找不到当前激活的虚拟环境 Python 路径。
2. 直接执行 `python export.py` 时，系统找不到可用的 `python` 命令，或仍在调用全局 Python（而虚拟环境内根本没装 pandas），所以报 `ModuleNotFoundError`。

#### b.最直接解决办法（强制指定虚拟环境 Python）

既然环境变量出问题，我们**直接用虚拟环境 Python 的完整路径**来运行脚本，绕开环境变量解析：

#### 步骤 1：在当前终端执行（复制粘贴即可）

```powershell
# 强制用虚拟环境的 Python 解释器运行脚本
.\demo1\Scripts\python.exe -m pip install pandas pymysql openpyxl
```

这一步会**把 pandas 安装到 demo1 虚拟环境里**，而不是全局 Python。

#### c.彻底解决

第一步：以管理员身份打开 PowerShell

**必须管理员！必须管理员！必须管理员！**

## 第二步：执行这条命令（修复权限）

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

提示时输入 **Y** 回车。

**作用**：让 PowerShell 允许激活虚拟环境，这是 90% 人环境异常的根源。

------

## 第三步：删除你坏掉的虚拟环境（必须删）

你现在的 `demo1` 已经环境错乱，必须重建！

进入你的项目文件夹：

```powershell
cd E:\系统默认\桌面\Plan\求职\实践\当日交付\d2026_03_16
```

删除旧虚拟环境：

```powershell
Remove-Item -Recurse -Force .\demo1
```

------

## 第四步：重建一个**绝对干净、不会再坏**的虚拟环境

```powershell
python -m venv .venv
```

注意：我用的是 **`.venv`**（前面带点），这是业界标准，PowerShell 识别最稳定！

*****

### 3. 如何将数据库中的表导出为xlsx或cvs格式？

1. 在datagrip里直接单击右键选中表格导出

   ![image-20260323220012260](E:\系统默认\桌面\Plan\求职\实践\当日交付\picture\image-20260323220012260.png)

2. MySQL客户端命令行导出

   ```bash
   # 登录MySQL
   mysql -u root -p
   
   # 切换到目标数据库
   USE test_db;
   
   # 导出表为CSV（以users表为例）
   SELECT * FROM users
   INTO OUTFILE 'C:/Users/你的用户名/Desktop/users.csv'  # Windows路径（用/而非\）
   -- INTO OUTFILE '/Users/你的用户名/Desktop/users.csv'  # macOS/Linux路径
   FIELDS TERMINATED BY ','  # 列分隔符为逗号
   ENCLOSED BY '"'  # 字段用双引号包裹（避免含逗号的字段出错）
   LINES TERMINATED BY '\n'  # 行分隔符为换行
   IGNORE 1 ROWS;  # 忽略表头（若需导出表头，需先查询列名）
   ```

​	命令行仅原生支持 CSV，不支持直接导出 Excel；

​	需确保 MySQL 有写入目标路径的权限，否则会报错。

3. Python 代码导出（灵活可控，支持批量导出）

   ### 前置准备

   ```bash
   # 安装依赖库
   pip install pandas pymysql openpyxl
   ```

   - `pymysql`：连接 MySQL 数据库；
   - `pandas`：数据处理；
   - `openpyxl`：支持 Excel 写入。

   ### 完整代码（可直接运行）

   ```python
   # -*- coding: utf-8 -*-
   """
   将MySQL表导出为CSV/Excel格式
   支持单表/多表批量导出，避免中文乱码
   """
   import pandas as pd
   import pymysql
   
   def export_mysql_to_file(
       host='localhost',
       port=3306,
       user='root',
       password='你的数据库密码',
       db='test_db',
       tables=['users', 'products', 'orders'],  # 要导出的表名列表
       export_format='xlsx',  # 导出格式：xlsx 或 csv
       save_path='./'  # 保存路径（默认当前目录）
   ):
       """
       导出MySQL表到文件
       """
       # 1. 连接数据库
       try:
           conn = pymysql.connect(
               host=host,
               port=port,
               user=user,
               password=password,
               db=db,
               charset='utf8mb4'  # 解决中文乱码
           )
           print(f"✅ 成功连接数据库：{db}")
   
           # 2. 遍历表名，逐个导出
           for table in tables:
               # 2.1 读取表数据到DataFrame
               sql = f"SELECT * FROM {table}"
               df = pd.read_sql(sql, conn)
               
               # 2.2 定义文件名
               file_name = f"{save_path}{table}.{export_format}"
               
               # 2.3 导出为指定格式
               if export_format == 'xlsx':
                   df.to_excel(file_name, index=False, engine='openpyxl')
               elif export_format == 'csv':
                   df.to_csv(file_name, index=False, encoding='utf-8-sig')  # utf-8-sig解决中文乱码
               else:
                   print(f"❌ 不支持的格式：{export_format}")
                   continue
               
               print(f"✅ 表 {table} 已导出到：{file_name}")
   
       except Exception as e:
           print(f"❌ 导出失败！错误信息：{str(e)}")
       finally:
           # 关闭数据库连接
           if 'conn' in locals() and conn.open:
               conn.close()
   
   # 主函数：执行导出
   if __name__ == "__main__":
       # 配置参数（替换为你的数据库信息）
       export_mysql_to_file(
           password='123456',  # 替换为你的MySQL密码
           db='test_db',       # 替换为你的数据库名
           tables=['users', 'products', 'orders'],  # 要导出的表
           export_format='xlsx',  # 可选：xlsx / csv
           save_path='C:/Users/你的用户名/Desktop/'  # 导出到桌面
       )
   ```

   ### 代码使用说明

   1. 替换参数：修改`password`（数据库密码）、`db`（数据库名）、`save_path`（保存路径）；
   2. 选择格式：`export_format='xlsx'` 导出 Excel，`export_format='csv'` 导出 CSV；
   3. 运行代码：执行后，指定的表会以「表名.xlsx/csv」的格式保存到目标路径。

   ### 关键优化点

   - `charset='utf8mb4'`：支持 emoji、特殊中文，避免数据库读取乱码；
   - `encoding='utf-8-sig'`：CSV 导出时解决 Excel 打开中文乱码问题；
   - `index=False`：导出时不包含 Pandas 的行索引，文件更整洁。

#### 核心代码——实现读取和基础查看

```python
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
```

输出结果：

```cmd
==================================================
✅️ 成功读取Excel 文件： users.xlsx
==================================================

1. 数据维度（行×列）：(1, 5)

2. 前5行数据：
   id  username  password         phone         create_time
0   1  zhangsan    123456  138111138111 2026-03-23 15:05:50

3. 后3行数据：
   id  username  password         phone         create_time
0   1  zhangsan    123456  138111138111 2026-03-23 15:05:50

4. 各列数据类型：
id                      int64
username                  str
password                int64
phone                   int64
create_time    datetime64[us]
dtype: object

5. 数值列描述性统计（均值、标准差、最值等）：
        id  password         phone          create_time
count  1.0       1.0  1.000000e+00                    1
mean   1.0  123456.0  1.381111e+11  2026-03-23 15:05:50
min    1.0  123456.0  1.381111e+11  2026-03-23 15:05:50
25%    1.0  123456.0  1.381111e+11  2026-03-23 15:05:50
50%    1.0  123456.0  1.381111e+11  2026-03-23 15:05:50
75%    1.0  123456.0  1.381111e+11  2026-03-23 15:05:50
max    1.0  123456.0  1.381111e+11  2026-03-23 15:05:50
std    NaN       NaN           NaN                  NaN

6. 各列空值数量：
id             0
username       0
password       0
phone          0
create_time    0
dtype: int64

7. 所有列名：
['id', 'username', 'password', 'phone', 'create_time']

✅️ 数据读取完成，可继续后续分析/处理！
```



# 2026.03.17

——实现日期：2026年3月24日

## 1. 用 Pandas 实现描述性统计全指标计算，对公开数据集（鸢尾花）做基础统计描述

### pandas

#### 必须记住的 Pandas 核心语法（总结）

```plaintext
读取文件：pd.read_csv()
查看前几行：df.head()
查看行列数：df.shape
查看空值：df.isnull().sum()
均值：mean()
中位数：median()
方差：var()
标准差：std()
分位数：quantile()
分组统计：groupby()
df.groupby("species")[numeric_cols].mean()

保存文件：to_csv()  
stats_df.to_csv("./iris_descriptive_stats.csv", encoding="utf-8-sig")
utf-8-sig：解决 Excel 打开中文乱码
```

#### DataFrame

**DataFrame = 一张带行名和列名的二维表格**

**就等于：内存里的一张 Excel 表**

##### 结构组成：

1. **columns 列名** → 表格的表头
2. **index 行索引** → 每行的编号（0,1,2,3...）
3. **values 值** → 表格里的数字 / 文字

#### pandas最常用操作速记

##### 一、先记住 2 个核心概念（看懂所有代码）

###### 1. DataFrame = 一张完整表格（Excel 表）

```python
df = pd.DataFrame(...)
```

- 有行、有列、有表头
- 代码里所有 `df` 都是表格

###### 2. Series = 表格里的一列

```python
df["age"]
```

- 单独一列数据
- 有数值 + 索引

##### 二、Pandas 15 个常用操作速记图（必背）

###### 1. 创建 / 读取数据

|           代码            |    功能    |      大白话      |
| :-----------------------: | :--------: | :--------------: |
|     `pd.DataFrame()`      | 创建空表格 | 拿一张空白 Excel |
|  `pd.read_csv("a.csv")`   |  读取 CSV  |  打开 CSV 文件   |
| `pd.read_excel("a.xlsx")` | 读取 Excel | 打开 Excel 文件  |

###### 2. 查看数据（最常用）

|     代码     |     功能     |      大白话      |
| :----------: | :----------: | :--------------: |
| `df.head()`  |  看前 5 行   |   快速预览数据   |
|  `df.shape`  | 看行数、列数 |     表格多大     |
| `df.columns` |    看列名    |    表头有哪些    |
| `df.dtypes`  |  看数据类型  | 每一列是什么类型 |
| `df.info()`  |  看完整信息  |   表格体检报告   |

###### 3. 筛选 / 查询数据

|         代码         |   功能   |      大白话      |
| :------------------: | :------: | :--------------: |
|     `df["age"]`      |  取一列  |    抽一列出来    |
| `df[["age","name"]]` |  取多列  |      抽多列      |
|  `df[df["age"]>18]`  | 条件筛选 | 筛选满足条件的行 |

###### 4. 数据清洗

|        代码         |    功能    |      大白话      |
| :-----------------: | :--------: | :--------------: |
| `df.isnull().sum()` | 统计缺失值 |  查哪里有空数据  |
|    `df.dropna()`    | 删除空值行 | 扔掉有空数据的行 |
|   `df.fillna(0)`    |  填充空值  |   把空值填成 0   |

###### 5. 描述性统计（你正在学的！）

|            代码             |       功能       |
| :-------------------------: | :--------------: |
|       `df.describe()`       | 一键生成基础统计 |
|         `df.mean()`         |       均值       |
|        `df.median()`        |      中位数      |
|         `df.var()`          |       方差       |
|         `df.std()`          |      标准差      |
|     `df.quantile(0.25)`     |    25% 分位数    |
| `df.groupby("列名").mean()` |     分组统计     |

###### 6. 保存文件

|          代码           |     功能     |
| :---------------------: | :----------: |
|  `df.to_csv("a.csv")`   |  保存为 CSV  |
| `df.to_excel("a.xlsx")` | 保存为 Excel |

##### 三、最最最重要的 6 句口诀（背会 = 精通入门）

1. **`df` = 表格**
2. **`df["列名"]` = 取一列**
3. **`head()` = 看前几行**
4. **`mean()` = 算平均值**
5. **`isnull()` = 查空值**
6. **`groupby()` = 分组统计**

##### 四、你现在的代码 = 这些语法拼起来的

```python
stats_df = pd.DataFrame()        # 1. 创建空表格
stats_df["均值"] = df.mean()     # 2. 加一列：均值
stats_df["中位数"] = df.median() # 3. 加一列：中位数
stats_df.to_csv("out.csv")       # 4. 保存
```

*****

### 专门对应你现在的鸢尾花项目

| 统计指标 |    Pandas 代码    |
| :------: | :---------------: |
|   均值   |     `.mean()`     |
|  中位数  |    `.median()`    |
|   众数   |     `.mode()`     |
|   方差   |     `.var()`      |
|  标准差  |     `.std()`      |
|  最小值  |     `.min()`      |
|  最大值  |     `.max()`      |
|  分位数  | `.quantile(0.25)` |
|   偏度   |     `.skew()`     |
|   峰度   |     `.kurt()`     |

对整张表保留四位小数：

```python
stats_df.round(4)
```

## 核心代码

```python
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
```

*****

# 2026.03.18

——实现日期：2026年3月24日

## 1. 用 Python 实现正态分布可视化，验证描述性统计指标在正态分布中的特征
### scipy

**scipy** = Python 专业**科学计算 + 统计计算库**

**stats** = scipy 里专门管**各种概率分布**的模块（正态分布、二项分布、t 分布……）

**专门用来生成理论上的 “完美正态分布曲线”**

用来和你真实数据对比，看是不是符合正态分布。

### 生成正态分布数据

```python
np.random.normal(loc=50, scale=10, size=10000)
```

- `loc=50` → 均值 μ=50
- `scale=10` → 标准差 σ=10
- `size=10000` → 生成 1 万条数据

这是**模拟数据**，不是真实表格。

### 标准正态分布代码

```python
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
```

### 基于鸢尾花数据的业务场景下分析对比是否符合正态分布

==**在实际业务中，我们通过绘制数据的频率分布直方图，并拟合标准正态分布曲线，通过视觉对比判断数据是否近似服从正态分布。**==

#### 一、真实业务验证正态分布 = 3 张图 + 1 个测试

##### 1. 直方图 + 理论分布曲线（最常用、最直观）

- **蓝色柱子** = 你的真实业务数据（如用户金额、时长、体重）
- **红色曲线** = scipy 算出的**标准正态分布曲线**
- **看是否贴合** → 越贴合越服从正态

**企业最常用**。

##### 2. QQ 图（专业数据分析必用）

- 点越贴近对角线 → 越正态
- 业务用来判断：是否能用正态分布做异常检测、假设检验

##### 3.  Shapiro 检验 / K-S 检验（统计学验证）

###### Shapiro 检验（小样本首选）

- `p > 0.05` → **服从正态**
- `p < 0.05` → **不服从**

###### K-S 检验（大样本 / 拟合后检验）

- 用数据拟合后的均值、标准差做检验
- 同样看 **p 值是否 > 0.05**

*****

matplotlib库里的pyplot画图注意设置中文字体和解决负号问题

```python 
# 设置画图中文字体
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置中文字体为黑体
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
```

#### 核心代码

```python 
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
```

#### 代码Q&A

```txt
histplot解释一下这个函数的参数
并告诉我整个代码完成的逻辑流程与先前的模拟的代码有什么不同
# 拟合正态曲线（scipy 自动算均值、标准差）
mu, sigma = stats.norm.fit(data)
x = np.linspace(min(data), max(data), 100)
y = stats.norm.pdf(x, mu, sigma)
以及这部分代码还是不太懂，拟合？是否就不再是标准正态分布了
以及QQ图的逻辑以及原理是什么
以及Shapiro和K-S的原理逻辑
```

##### 一、先讲：sns.histplot 函数参数解释

```python
sns.histplot(data, bins=15, stat="density", color="skyblue", alpha=0.7)
```

###### 逐参数解释

- `data`：你的真实数据（花瓣长度）

- `bins=15`：把数据分成 **15 个柱子**（柱子越多越细）

- ```
  stat="density"
  ```

  ：纵轴变成密度，而不是计数

  ✅ 目的：让曲线和柱子

  同比例、能叠加在一起

- `color="skyblue"`：柱子颜色

- `alpha=0.7`：透明度，让图更好看

###### 一句话记住

`histplot` = **画真实数据的分布直方图**

##### 二、完整代码逻辑流程

###### 真实业务正态性验证 = 固定 4 步

1. **读取真实数据**（鸢尾花花瓣长度）
2. **画直方图 + 拟合正态曲线**（肉眼看形状）
3. **画 QQ 图**（专业看是否正态）
4. **Shapiro + K-S 检验**（统计学判断）

##### 三、和你之前模拟代码的区别

###### 1. 模拟代码

```python
data = np.random.normal(50,10,10000)
```

✅ 人工生成**完美正态数据**

###### 2. 现在的真实业务代码

```python
data = df["petal_l"].values
```

✅ **真实数据**（不是完美正态）

###### 核心区别

- 模拟代码：验证 “正态长什么样”
- 真实代码：**判断 “这个数据是不是正态”**
- 真实数据 ≠ 完美正态

##### 四、你最不懂的部分：拟合曲线（超重点）

```python
mu, sigma = stats.norm.fit(data)
x = np.linspace(min(data), max(data), 100)
y = stats.norm.pdf(x, mu, sigma)
```

###### 1. 什么叫 **拟合（fit）**？

大白话：

**用你的真实数据，算出最适合它的正态曲线**

自动计算：

- `mu` = 你的数据均值
- `sigma` = 你的数据标准差

###### 2. 还是标准正态分布吗？

**不是标准正态（标准正态 μ=0,σ=1）**

这是：

**【适配你数据的正态分布】**

###### 3. 为什么要这样做？

因为你的数据范围是 **1~7**

不能用 μ=0,σ=1 的标准正态对比

必须 **生成一条和你数据同范围、同中心的理论曲线**

###### 一句话总结

**拟合 = 给你的真实数据，量身定做一条最像的正态曲线，用来对比是否正态。**

##### 五、QQ 图原理（超级重要）

###### 一句话讲透

**QQ 图比较：你的数据分位数 VS 理论正态分布分位数**

###### 原理

1. 把你的数据从小到大排序
2. 把标准正态数据从小到大排序
3. 一一对应画点
4. **点越贴近对角线 → 越正态**
5. 点偏离 = 不正态

###### 直观理解

- 对角线 = **完美正态**
- 点在直线上 = 正态
- 点偏离直线 = 不正态

##### 六、Shapiro 检验 + K-S 检验 原理

###### 共同逻辑

**比较：真实数据的分布 VS 理论正态分布**

差异越小 → 越正态

差异越大 → 越不正态

###### 1. Shapiro 检验（小样本首选）

- 假设：数据服从正态
- 计算差异程度
- **p > 0.05 → 不能拒绝假设 → 正态**
- **p < 0.05 → 拒绝假设 → 不正态**

###### 2. K-S 检验（大样本 / 拟合后）

- 比较**累积分布**

- 看真实数据与正态分布的距离

- 同样：

  p > 0.05 ✅ 正态

  p < 0.05 ❌ 不正态

##### 七、终极总结（背会 = 精通）

###### 1. histplot：画真实数据直方图

###### 2. 拟合曲线 = 给你的数据生成最匹配的正态曲线（不是标准正态）

###### 3. QQ 图：点贴直线 = 正态，偏离 = 不正态

###### 4.  Shapiro/K-S：p>0.05 = 正态

###### 5. 真实业务数据大多不正态！

#### QQ图、Shapiro-Wilk 检验、K-S 检验原理

##### 一、QQ 图到底是什么？（最清晰解释）

全称：Quantile-Quantile Plot（分位数 - 分位数图）

###### 核心逻辑一句话

把你的真实数据的分位数，和 “理论正态分布应该有的分位数” 一一对应画点。

如果两个分布长得一样，点就会排成一条完美直线。

###### 1. 分位数是什么？

把数据从小到大排好，切成 N 等份，每一份的分界值就是分位数。

例如：

- 中位数 = 50% 分位数
- 25%、75% 四分位数

###### 2. QQ 图到底在做什么？

步骤非常简单：

1. 把你的**真实数据从小到大排序**
2. 生成一组**相同数量、服从完美正态分布**的理论数，也排序
3. 把**真实第 k 小的值** 对应 **理论第 k 小的值**，画一个点
4. 所有点画完，就成了 QQ 图

###### 3. 怎么判断？

- 所有点紧紧贴在对角直线上

  → 真实分布 ≈ 正态分布

- 点明显偏离直线，尤其是两头

  → 分布不正态

###### 直观理解

对角线 = **理想正态的影子**

你的点 = **真实数据的脚印**

脚印跟着影子走 = 正态

##### 二、Shapiro-Wilk 检验 原理（小样本正态检验神器）

###### 核心一句话

**计算你的数据 “有多像正态样本”，给出一个统计量 W，越接近 1 越正态。**

###### 1. 步骤逻辑

1. 把数据排序
2. 用一套专门的系数（ Shapiro 系数），计算一个**相关性统计量 W**
3. W 越接近 **1** → 数据越像正态
4. W 越小 → 越不正态

###### 2. p 值怎么来？

- 原假设 H₀：**数据服从正态分布**
- 如果数据真的是正态，W 应该很大
- 如果 W 异常小，p 值就会很小

###### 判断规则（永远不变）

- **p > 0.05：不拒绝 H₀ → 可认为正态**
- **p < 0.05：拒绝 H₀ → 显著不正态**

###### 3. 特点

- **小样本最准（n ＜ 50）**
- 机器学习、论文、实验数据最常用
- 比 K-S 更灵敏、更严格

##### 三、K-S 检验（Kolmogorov-Smirnov）原理

###### 核心一句话

**比较 “真实数据的累积分布” 与 “理论正态分布的累积分布”，看最大差距有多大。**

###### 1. 累积分布函数 CDF 是什么？

CDF (x) = 数据中 ≤x 的比例

画出来是一条从 0 爬到 1 的 S 形曲线。

###### 2. K-S 到底在比什么？

1. 算出你的**真实数据的累积分布 Fₙ(x)**
2. 算出**理论正态分布的累积分布 F (x)**
3. 找两条曲线之间**最大的垂直距离 D**
4. D 越大 → 越不像正态
5. D 越小 → 越像正态

###### 3. p 值含义

- H₀：两个分布相同
- 差距 D 越大，p 越小
- **p > 0.05：认为服从正态**
- **p < 0.05：不服从正态**

###### 4. 特点

- 可用于**任意分布**（正态、均匀、指数…）
- 对**大样本**较稳定
- 不如 Shapiro 灵敏

##### 四、三者最精炼对比（面试直接背）

###### 1. QQ 图

- 比较：**真实分位数 ↔ 正态分位数**
- 看点是否贴直线
- 直观、专业、必画

###### 2. Shapiro-Wilk

- 计算：**数据与正态的相关程度 W**
- W≈1 越正态
- **小样本最准**

###### 3. K-S 检验

- 比较：**两条累积分布曲线的最大差距 D**
- 差距越小越正态
- **通用、大样本常用**

##### 五、最终超级总结（最关键）

- **QQ 图 = 看图判断**
- **Shapiro = 小样本正态神器**
- **K-S = 通用分布比较工具**
- **p > 0.05 ✅ 正态；p < 0.05 ❌ 不正态**

******

##  2. 100字以内的业务应用场景总结

正态分布广泛用于用户行为、质量检测、金融风控。如用户消费金额、使用时长、身高体重、考试成绩均服从正态分布，多数数据集中在均值附近，极端值少。企业可通过3σ 法则识别异常用户、异常订单，实现精准监控与风险控制。



# 2026.03.19

## join的适用场景及5道子查询题

### 5 道 SQL 子查询经典练习题（含答案）

全部基于你熟悉的两张表，难度循序渐进：

- `Signups(user_id, time_stamp)`
- `Confirmations(user_id, action)`

------

#### 第 1 题（标量子查询）

查询每个用户的 ID，以及**所有用户的平均确认率**（只显示一个平均值在每行）

```sql
SELECT
  user_id,
  (
    SELECT ROUND(
      SUM(action='confirmed')/COUNT(*),2
    )
    FROM Confirmations
  ) AS avg_rate
FROM Signups;
```

------

#### 第 2 题（WHERE 子查询 + IN）

找出**至少有一次 confirmed** 的用户 ID

```sql
SELECT user_id
FROM Signups
WHERE user_id IN (
  SELECT user_id
  FROM Confirmations
  WHERE action = 'confirmed'
);
```

------

#### 第 3 题（关联子查询 + EXISTS）

找出**有确认记录**的用户

```sql
SELECT user_id
FROM Signups s
WHERE EXISTS (
  SELECT 1
  FROM Confirmations c
  WHERE c.user_id = s.user_id
);

```

------

#### 第 4 题（NOT EXISTS 高频面试题）

找出**从未发起过确认请求**的用户

```sql
SELECT user_id
FROM Signups s
WHERE NOT EXISTS (
  SELECT 1
  FROM Confirmations c
  WHERE c.user_id = s.user_id
);
```

------

#### 第 5 题（FROM 子查询，派生表）

先统计每个用户的确认率，再筛选出 **确认率 = 1.00** 的用户

```sql
SELECT user_id, confirmation_rate
FROM (
  SELECT
    s.user_id,
    ROUND(IFNULL(
      SUM(c.action='confirmed')/COUNT(c.user_id),0
    ),2) AS confirmation_rate
  FROM Signups s
  LEFT JOIN Confirmations c
    ON s.user_id = c.user_id
  GROUP BY s.user_id
) AS t
WHERE confirmation_rate = 1.00;
```

------

### 子查询 vs JOIN 适用场景（面试必背）

#### 一、适合用 **子查询** 的场景

1. 只需要

   判断存在性

   - 有没有订单？有没有登录？
   - 用 `EXISTS / NOT EXISTS`

2. 需要

   单个值

   （总数、平均值、最大值）

   - 标量子查询

3. 逻辑分层清晰，**只查一张表的结果**

4. 数据量小、逻辑简单，不想写多表连接

#### 二、适合用 **JOIN** 的场景

1. 要同时展示多张表的字段
   - 用户名 + 订单时间 + 金额
2. 需要分组统计、批量计算
   - 每个用户的订单数、成功率
3. **大数据量**下性能更好
4. 需要对关联结果**过滤、排序、分页**

#### 三、一句话总结

- **看存在性 → 子查询（EXISTS）**
- **看关联字段、做统计 → JOIN**
- **简单逻辑用子查询，复杂统计用 JOIN**

## pandas皮尔逊相关系数计算及热力图绘制

### 核心代码

```python
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
plt.show()
plt.savefig("pearson_correlation_heatmap.png", dpi=300)
```

### 结果

```txt
===== 皮尔逊相关系数矩阵 =====
seaborn自带数据集:              sepal_length  sepal_width  petal_length  petal_width
sepal_length          1.00        -0.12          0.87         0.82
sepal_width          -0.12         1.00         -0.43        -0.37
petal_length          0.87        -0.43          1.00         0.96
petal_width           0.82        -0.37          0.96         1.00
本地iris.data文件:              sepal_length  speal_width  petal_length  petal_width
sepal_length          1.00        -0.11          0.87         0.82
speal_width          -0.11         1.00         -0.42        -0.36
petal_length          0.87        -0.42          1.00         0.96
petal_width           0.82        -0.36          0.96         1.00
```

![pearson_correlation_heatmap](E:\系统默认\桌面\Plan\求职\实践\当日交付\picture\pearson_correlation_heatmap-1774594278463-2.png)

我给你**最完整、最易懂、一次性记牢**的

### **seaborn.heatmap 全参数超详细解析**

（你现在用的热力图函数，面试 + 工作必背）

```python
sns.heatmap(
    data,              # 1. 必须传：相关系数矩阵
    annot=True,        # 2. 是否在格子里显示数字
    cmap="RdBu_r",     # 3. 配色方案（最常用）
    vmax=1, vmin=-1,   # 4. 颜色映射的最大/最小值
    linewidths=0.5,    # 5. 格子之间的边框宽度
    fmt=".2f",         # 6. 显示数值的格式（保留2位小数）
    linecolor="white", # 7. 边框颜色（默认白色）
    cbar=True,         # 8. 是否显示右侧颜色条
    center=0,          # 9. 颜色映射中心值（皮尔逊必须设0）
    square=True        # 10. 让格子变成正方形（美观）
)
```

------

#### 🔥 逐参数 **大白话解释**

##### 1. `data`

- 必须传入一个**矩阵 / 表格**（如相关系数矩阵）
- 必须是**纯数字**
- 你的代码：`corr_matrix`

##### 2. `annot=True`

- **True = 在每个格子里写上相关系数数值**
- False = 只显示颜色，不写数字
- 做数据分析**必须写 True**

##### 3. `cmap="RdBu_r"`

- 配色系统（最关键的视觉参数）
- RdBu_r = 红 — 蓝配色
  - 红色 → 正相关
  - 蓝色 → 负相关
  - 白色 → 0 不相关
- 皮尔逊专用配色

##### 4. `vmax=1, vmin=-1`

- 颜色条的**最大值、最小值**
- 皮尔逊相关系数范围 **[-1, 1]**
- 必须写这两个参数，颜色才准确

##### 5. `linewidths=0.5`

- 格子与格子之间的**缝隙宽度**
- 数字越大，缝隙越宽

##### 6. `fmt=".2f"`

- 格子里数字的格式
- `.2f` = **保留两位小数**
- 必用，否则数字太长很难看

##### 7. `linecolor="white"`

- 格子分割线的颜色
- 默认白色，不用改

##### 8. `cbar=True`

- 是否显示**右边的颜色条**
- 建议 True，方便别人看图例

##### 9. `center=0`

- 颜色条**中心点设为 0**
- 皮尔逊相关系数必须用 `center=0`
- 让 0 是白色，>0 红，<0 蓝

##### 10. `square=True`

- 让每个格子变成**正正方形**
- 图会非常规整美观

------

#### 🎯 皮尔逊热力图 **最优参数模板**（背这个）

```python
sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="RdBu_r",
    vmin=-1, vmax=1,
    center=0,
    fmt=".2f",
    square=True,
    linewidths=0.5
)
```

------

#### 🚀 一句话记住所有参数

数据传入、annot 显示数字、cmap 配色、v 范围、

line 边框、fmt 小数、center 居中、square 正方形



# 2026.03.20

——实现日期：2026年3月27日

本周复习基础统计学脑图

![统计学基础](E:\系统默认\桌面\Plan\求职\实践\当日交付\picture\统计学基础.png)

# 2026.03.21

——实现日期：2026年3月27日

在jupyter notebook上实现泰坦尼克数据集的初步查看和理解

## 如何将虚拟环境转化为能在jupyter notebook上识别的kernel

### 1. 先激活你的虚拟环境（必须！）

#### 如果是 conda 环境

```bash
conda activate 你的环境名
```

#### 如果是 venv

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

------

### 2. 在虚拟环境里安装 ipykernel

```bash
pip install ipykernel
```

------

### 3. 把环境写入 Jupyter 内核（关键）

```bash
python -m ipykernel install --user --name=你想显示的名字
```

例子：

```bash
python -m ipykernel install --user --name=my_ml_env
```

## 一、数据集整体说明

- **数据集用途**：泰坦尼克号乘客生存预测
- **数据类型**：已完成**独热编码（One-Hot）**，全数值型，可直接建模
- 包含表：2 张
  1. `Taitan_onehot.csv`：乘客特征数据
  2. `gender_submission.csv`：乘客 ID + 生存标签

------

## 二、字段含义与说明

### 1）Taitan_onehot.csv（特征表）

|   字段名   | 类型 |                    字段含义                    |
| :--------: | :--: | :--------------------------------------------: |
|    Age     | 数值 |                    乘客年龄                    |
|   Pclass   | 数值 | 船舱等级（1 = 头等舱，2 = 二等舱，3 = 三等舱） |
|   SibSp    | 数值 |            同乘的兄弟姐妹 / 配偶数             |
|   Parch    | 数值 |              同乘的父母 / 子女数               |
|    Fare    | 数值 |                    乘客票价                    |
| Sex_female | 0/1  |              1 = 女性，0 = 非女性              |
|  Sex_male  | 0/1  |              1 = 男性，0 = 非男性              |
| Embarked_C | 0/1  |                  1=C 港口登船                  |
| Embarked_Q | 0/1  |                  1=Q 港口登船                  |
| Embarked_S | 0/1  |                  1=S 港口登船                  |
| Embarked_0 | 0/1  |            登船港口缺失 / 未知标记             |

### 2）gender_submission.csv（标签表）

|   字段名    | 类型 |      字段含义      |
| :---------: | :--: | :----------------: |
| PassengerId | 数值 |    乘客唯一 ID     |
|  Survived   | 0/1  | 1 = 存活，0 = 死亡 |

------

## 三、数据规模（行数 × 列数）

### 1）特征表 Taitan_onehot.csv

- **行数**：891
- **列数**：11
- **数据类型**：全为数值型（int64 /float64）

### 2）标签表 gender_submission.csv

- **行数**：891
- **列数**：2
- **与特征表一一对应**

------

## 四、缺失值情况（关键结论）

### 1）Taitan_onehot.csv

- **Age（年龄）**：存在缺失（约 20% 左右）
- **其他所有字段**：无缺失
- **独热编码列（Sex/Embarked）**：无缺失

### 2）gender_submission.csv

- **无任何缺失值**

------

## 五、数据统计概览（关键结论）

1. **年龄**：平均约 29 岁，主要集中在 20～30 岁
2. **舱位**：三等舱乘客最多
3. **票价**：分布不均，存在高价异常值（富人）
4. **性别**：男性多于女性
5. **登船港口**：S 港口人数最多
6. **存活率**：约 38% 乘客存活

------

## 六、可直接使用的报告总结（作业 / 面试直接复制）

本数据集包含**891 名乘客**的信息，共**11 个特征 + 1 个标签**。

数据已完成**独热编码**，无文字类型，可直接用于建模。

主要问题为**年龄存在缺失**，票价存在异常值。

影响生存的关键特征为：性别、舱位、票价。

# 2026.03.23



# 2026.03.24