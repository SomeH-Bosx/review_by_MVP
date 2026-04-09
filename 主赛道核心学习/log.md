# 2026.03.16 周一    

——实现日期：2026.03.18

## 数据库底层原理

### 1. 关系型数据库核心逻辑

* ## 1. 什么是关系型数据库（RDBMS）

  - 以 ** 关系（二维表）** 为核心存储结构
  - 数据按**行、列**存储，表与表之间通过**关系**关联
  - 遵循**ACID**，支持**事务**，保证数据安全可靠

  ## 2. 核心理论：关系模型三要素

  1. **实体**：现实中的对象（用户、订单、商品）

  2. **属性**：实体的特征（用户名、价格、时间）

  3. 关系

     ：实体之间的联系

     - 一对一（1:1）
     - 一对多（1:N）
     - 多对多（N:M）→ 必须拆成**中间关联表**

     

  ## 3. ACID 事务四大特性（必考）

  - **A（Atomicity）原子性**：要么全成功，要么全失败
  - **C（Consistency）一致性**：事务前后数据合法、完整
  - **I（Isolation）隔离性**：多个事务互不干扰
  - **D（Durability）持久性**：提交后永久生效

  ## 4. 三大范式（设计表的核心思想）

  ### 1NF（第一范式）

  - 列**不可再分**，每一列都是原子数据

  ### 2NF（第二范式）

  - 满足 1NF
  - **非主键字段完全依赖主键**，不能只依赖主键一部分（针对联合主键）

  ### 3NF（第三范式）

  - 满足 2NF
  - **非主键字段之间不能互相推导**，消除传递依赖

  > 面试一句话总结：
  >
  > **1NF 列不可分，2NF 非主键依赖全主键，3NF 非主键之间不依赖。**

### 2. ACID特性：事务的四大特性——原子性、一致性、隔离性、持久性

### 3. 表结构设计基础

* ## 1. 设计步骤（标准流程）

  1. 梳理**业务实体**
  2. 明确**实体关系**（1:1 / 1:N / N:M）
  3. 拆分表，确定**主键**
  4. 设计字段、类型、长度
  5. 加**约束、索引、外键（可选）**
  6. 考虑**扩展性、查询性能**

  ## 2. 必须掌握的关键字段设计

  ### 主键（Primary Key）

  - 唯一、非空、一张表一个
  - 推荐用**自增 ID / 雪花 ID**，不要用业务字段做主键

  ### 外键（Foreign Key）

  - 建立表与表之间的引用关系
  - 实际开发很多公司**物理外键不用，用逻辑外键**（代码保证）

  ### 必备公共字段（大厂通用）

  ```plaintext
  id            主键
  create_time   创建时间
  update_time   更新时间
  is_deleted    删除标记（0未删 1已删）
  ```

  ## 3. 常用字段类型（MySQL 为例）

  - 用户名称：`varchar(50)`
  - 手机号：`char(11)`
  - 金额：`decimal(10,2)`
  - 时间：`datetime / timestamp`
  - 状态：`tinyint`（0/1/2）
  - 长文本：`text`

  ## 4. 约束（Constraint）

  - `NOT NULL`：非空
  - `UNIQUE`：唯一
  - `PRIMARY KEY`：主键
  - `FOREIGN KEY`：外键
  - `DEFAULT`：默认值

  ## 5. 多对多关系处理（必考）

  例：学生 ↔ 课程

  - 不能直接放一张表

  - 必须拆成

    中间关联表

    - 学生表（student）
    - 课程表（course）
    - 学生课程关联表（student_course）
      - student_id
      - course_id

  ## 6. 设计三大原则（面试加分）

  1. **一张表只做一件事**（单一职责）
  2. **避免冗余字段**（符合 3NF）
  3. **优先考虑查询与扩展**，不要过度范式化

* # 三、面试常问的一句话答案

  - **为什么不用业务字段做主键？**

    业务可能变、可能重复、可能为空，主键必须稳定唯一。

  - **为什么不建议滥用外键？**

    影响插入 / 删除性能，耦合高，分布式不友好。

  - **三范式核心目的？**

    减少冗余、避免更新异常、保证数据一致。

## MySQL环境搭建+可视化工具（DBeaver/Navicat）安装调试

安装DBeaver

### 作用

数据库可视化工具（DBeaver/Navicat）是**替代命令行、用图形界面管理数据库**的核心工具，解决 “写 SQL 麻烦、看数据 / 结构不直观” 的痛点。

#### 核心用途

1. **连接与管理多数据库**：统一界面连接 MySQL、PostgreSQL、Oracle、SQL Server、MongoDB、Redis 等，不用切换工具。
2. 可视化操作：
   - 建库 / 建表 / 改字段：**拖拽 + 表单**，不用写 DDL。
   - 数据增删改查：表格直接编辑，支持批量操作。
   - 查看表结构、索引、外键、视图、存储过程等。
3. **SQL 开发**：语法高亮、自动补全、格式化、执行计划、多标签页、查询结果导出（Excel/CSV/JSON）。
4. **数据管理**：备份 / 恢复、数据导入导出、数据对比、ER 图生成（Navicat 更强）。
5. **运维与调试**：查看执行日志、慢查询、连接状态、权限管理。



## SQL基础：增删改查

1. insert
2. delete
3. update
4. select

### 一、核心前提（示例表）

先定义一个通用的用户表 `user`，后续所有示例都基于这个表，方便你理解：

```sql
CREATE TABLE `user` (
  `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
  `username` VARCHAR(50) NOT NULL COMMENT '用户名',
  `age` TINYINT COMMENT '年龄',
  `gender` TINYINT COMMENT '性别：1-男，2-女，0-未知',
  `phone` CHAR(11) UNIQUE COMMENT '手机号',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) COMMENT = '用户表';
```

------

## 二、增（CREATE）：插入数据

### 1. 基础插入（指定字段）

```sql
-- 插入单条数据（推荐：指定字段，字段顺序可调整）
INSERT INTO user (username, age, gender, phone)
VALUES ('张三', 25, 1, '13800138000');

-- 插入多条数据（面试常问：批量插入比单条插效率高）
INSERT INTO user (username, age, gender, phone)
VALUES 
('李四', 28, 1, '13800138001'),
('王五', 22, 2, '13800138002');
```

### 2. 特殊场景：插入所有字段（不推荐，耦合高）

```sql
-- 字段顺序必须和表结构完全一致
INSERT INTO user VALUES (NULL, '赵六', 30, 1, '13800138003', NOW());
-- 注：自增主键填NULL/0，数据库会自动生成
```

------

## 三、查（READ）：查询数据（面试重中之重）

### 1. 基础查询

```sql
-- 查询所有字段（生产环境慎用：字段多会慢，且可能泄露敏感数据）
SELECT * FROM user;

-- 查询指定字段（推荐）
SELECT username, age, phone FROM user;

-- 去重查询（DISTINCT）
SELECT DISTINCT gender FROM user; -- 只查不同的性别值

-- 别名（AS，可省略）
SELECT username AS 姓名, age 年龄 FROM user; -- 字段别名
SELECT u.username FROM user u; -- 表别名（多表联查必用）
```

### 2. 条件查询（WHERE）

```sql
-- 单条件
SELECT * FROM user WHERE age = 25;
SELECT * FROM user WHERE age > 20 AND gender = 2; -- 多条件且
SELECT * FROM user WHERE age BETWEEN 20 AND 30; -- 范围
SELECT * FROM user WHERE username LIKE '张%'; -- 模糊查询（张开头）
SELECT * FROM user WHERE phone IN ('13800138000', '13800138001'); -- 枚举值

-- 空值判断（面试易错：不能用=，必须用IS NULL/IS NOT NULL）
SELECT * FROM user WHERE age IS NULL;
SELECT * FROM user WHERE age IS NOT NULL;
```

### 3. 排序（ORDER BY）

```sql
-- 按年龄升序（ASC可省略），年龄相同按ID降序
SELECT * FROM user ORDER BY age ASC, id DESC;
```

### 4. 分页（面试高频：MySQL 用 LIMIT）

```sql
-- 跳过前10条，查10条（第11-20条，对应分页第2页，每页10条）
SELECT * FROM user LIMIT 10 OFFSET 10;
-- 简写（更常用）
SELECT * FROM user LIMIT 10, 10;
```

### 5. 聚合查询（常用统计）

```sql
SELECT 
  COUNT(*) AS 总用户数, -- 统计行数
  AVG(age) AS 平均年龄, -- 平均值
  MAX(age) AS 最大年龄, -- 最大值
  MIN(age) AS 最小年龄, -- 最小值
  SUM(age) AS 年龄总和  -- 求和
FROM user 
WHERE gender = 1; -- 只统计男性
```

### 6. 分组查询（GROUP BY）

```sql
-- 按性别分组，统计每组的用户数和平均年龄
SELECT gender, COUNT(*) AS 人数, AVG(age) AS 平均年龄
FROM user
GROUP BY gender
HAVING COUNT(*) > 1; -- 筛选分组后结果（面试：HAVING是分组后过滤，WHERE是分组前）
```

------

## 四、改（UPDATE）：更新数据

### 1. 基础更新

```sql
-- 修改单条数据（必须加WHERE，否则全表更新！面试必提醒）
UPDATE user SET age = 26 WHERE id = 1;

-- 修改多条字段
UPDATE user 
SET age = 29, phone = '13800138004' 
WHERE username = '李四';

-- 带条件的批量更新
UPDATE user SET age = age + 1 WHERE gender = 1; -- 所有男性年龄+1
```

### 2. 注意事项（面试必提）

- **必须加 WHERE 条件**：除非明确要更新全表，否则会导致所有数据被改，生产环境是重大事故；

- 事务保护：更新重要数据时，先开事务，确认无误再提交：

  ```sql
  BEGIN; -- 开启事务
  UPDATE user SET age = 26 WHERE id = 1;
  COMMIT; -- 提交（确认修改）
  -- ROLLBACK; -- 回滚（出错时撤销）
  ```

  

------

## 五、删（DELETE）：删除数据

### 1. 基础删除

```sql
-- 删除单条数据（必须加WHERE，否则全表删除！）
DELETE FROM user WHERE id = 3;

-- 批量删除
DELETE FROM user WHERE age < 20;
```

### 2. 清空表（两种方式，面试必问区别）

```sql
-- 方式1：DELETE（可回滚，有日志，慢）
DELETE FROM user; -- 清空数据，自增主键不重置

-- 方式2：TRUNCATE（不可回滚，无日志，快）
TRUNCATE TABLE user; -- 清空数据，自增主键重置为1
```

### 3. 软删除（实战常用，面试加分）

生产环境很少物理删除数据，而是用**逻辑删除**（标记删除）：

```sql
-- 先加删除标记字段
ALTER TABLE user ADD COLUMN is_deleted TINYINT DEFAULT 0 COMMENT '0-未删，1-已删';

-- 删除时只更新标记，不删数据
UPDATE user SET is_deleted = 1 WHERE id = 3;

-- 查询时过滤已删除数据
SELECT * FROM user WHERE is_deleted = 0;
```

------

### 总结

1. **查（SELECT）是核心**：面试重点考 WHERE、ORDER BY、LIMIT、GROUP BY/HAVING 的用法，尤其注意空值判断（IS NULL）和模糊查询（LIKE）；
2. **增删改注意事项**：INSERT 批量插效率高，UPDATE/DELETE 必须加 WHERE，生产环境优先用软删除；
3. **面试易错点**：NULL 不能用 = 判断、HAVING vs WHERE、TRUNCATE vs DELETE 的区别。

# 2026.03.17 周二

——实现日期：2026年3月23日

## SQL进阶

* where条件过滤
* group by 聚合
* having筛选
* order by排序

### 一、SQL 进阶核心语法（高频必考）

#### 1. WHERE 条件过滤

**作用**：对**原始数据行**进行筛选，在分组前过滤数据

```sql
SELECT * FROM users 
WHERE age >= 18 
  AND gender = '男'
  AND create_time > '2025-01-01';
```

常用运算符：

- `=`、`!=`/`<>`、`>`、`<`、`>=`、`<=`
- `AND`、`OR`、`NOT`
- `IN (值1,值2)`、`BETWEEN 起始 AND 结束`
- `LIKE '%关键词%'` 模糊匹配
- `IS NULL` / `IS NOT NULL` 判断空值

#### 2. GROUP BY 分组聚合

**作用**：按某一列 / 多列分组，搭配聚合函数做统计

常用聚合函数：

- `COUNT(*)`：计数
- `SUM(字段)`：求和
- `AVG(字段)`：平均值
- `MAX(字段)`：最大值
- `MIN(字段)`：最小值

示例：按性别统计人数、平均年龄

```sql
SELECT 
  gender,
  COUNT(*) AS 人数,
  AVG(age) AS 平均年龄
FROM users
WHERE age > 0
GROUP BY gender;
```

#### 3. HAVING 分组后筛选

**作用**：对**分组后的结果**过滤，只能用在 GROUP BY 后面

```sql
SELECT 
  dept_id,
  AVG(salary) AS 平均工资
FROM employee
GROUP BY dept_id
HAVING AVG(salary) > 8000;
```

> WHERE：过滤原始行
>
> HAVING：过滤分组结果

#### 4. ORDER BY 排序

```sql
SELECT * FROM orders
ORDER BY create_time DESC, amount ASC;
```

- `DESC`：降序（从大到小）
- `ASC`：升序（默认，从小到大）

## 统计学基础

* 描述性统计核心指标
  * 均值
  * 中位数
  * 众数
  * 方差
  * 标准差
  * 分位数

### 二、统计学描述性统计核心指标

#### 1. 集中趋势（数据 “中心” 在哪）

1. **均值（平均数）**

   所有数相加 ÷ 个数

   xˉ=nx1+x2+...+xn

2. **中位数**

   数据从小到大排列，**中间那个数**

   偶数个：中间两个的平均

3. **众数**

   出现**次数最多**的数（可多个）

#### 2. 离散程度（数据散不散）

1. **方差**

   每个数与均值差的平方的平均

   s2=n∑(xi−xˉ)2

2. **标准差**

   方差开根号，单位和原数据一致，更直观

3. **极差**

   最大值 − 最小值

#### 3. 分位数（位置指标）

- 四分位数

  - Q1：25% 分位（前 25% 位置）
  - Q2：50% 分位 = 中位数
  - Q3：75% 分位

- 四分位距 IQR = Q3 − Q1

  常用于识别异常值

## 极简速记版

- **WHERE**：先筛行
- **GROUP BY**：再分组统计
- **HAVING**：筛分组结果
- **ORDER BY**：最后排序
- **均值 / 中位数 / 众数**：看中心
- **方差 / 标准差**：看波动
- **分位数**：看位置分布

# 2026.03.18 周三

——实现日期：2026年3月24日

## 一、SQL 多表联查 JOIN 核心复习

### 1. 通用理解

- **多表联查本质**：把多张表按 ** 共同字段（关联键）** 拼在一起
- **关联键**：通常是 id，比如 user_id、order_id、class_id 等
- **语法结构**

```sql
SELECT 字段
FROM 表A
JOIN 表B ON 表A.字段 = 表B.字段
```

###  2. INNER JOIN（内连接）

**含义**：取**两张表的交集**

- 只保留**两边都能匹配上**的数据
- 任何一边没有对应数据，整行丢弃
- **最常用、最安全**

**场景举例**

- 查询**既有订单又有用户信息**的数据
- 查询**既有学生又有班级**的数据

**记忆口诀**

> 两边都有才显示，缺一边就不要

### 3. LEFT JOIN（左连接）

**含义**：左表**全部保留**，右表能匹配就显示，匹配不上填 NULL

- 左表 = 主表，一条都不会丢
- 右表 = 附表，匹配不到就 NULL

**场景举例**

- 查**所有用户**，以及他们的订单（没下单的用户也要显示）
- 查**所有商品**，以及它们的销量（没卖过也要显示）

**记忆口诀**

> 左表全要，右表随缘，没有就空着

### 4. RIGHT JOIN（右连接）

**含义**：右表全部保留，左表能匹配就显示，否则 NULL

- 基本等价于把 LEFT JOIN 左右表互换
- 实际工作**很少用**，习惯用 LEFT JOIN 改表顺序

**场景举例**

- 查**所有订单**，以及对应用户（哪怕用户被删除也要保留订单）

### 5. 三张图秒懂区别

- **INNER**：只留中间重叠部分
- **LEFT**：左圈全保留 + 重叠部分
- **RIGHT**：右圈全保留 + 重叠部分

### 6. 高频面试坑点（必记）

1. **LEFT JOIN 后加 WHERE 会变成 INNER JOIN**

```sql
-- 本来是左连接
FROM user
LEFT JOIN order ON user.id=order.uid
-- 但下面这句会过滤掉 NULL，等于内连接
WHERE order.amount > 100
```

* 正确保留 LEFT JOIN 效果：条件写在 ON 里面

```sql
LEFT JOIN order
ON user.id = order.uid AND order.amount > 100
```

【相当于先做了order的条件判断，再进行左连接】

✅ **左表用户全保留**

✅ 有订单且 > 100 → 显示订单

✅ 没订单 / 订单≤100 → 显示 NULL

这才是 **真正的 LEFT JOIN**。

*****

* 错误写法（写在 WHERE 里 → 变 INNER JOIN）

```sql
LEFT JOIN order ON user.id = order.uid
WHERE order.amount > 100
```

❌ **所有 order 为 NULL 的行全部被丢掉**

❌ **只剩下两边都匹配的行**

❌ **等同于 INNER JOIN**

2. **一对多连接会导致行数膨胀（重复数据）**

- 1 个用户对应 5 条订单 → 连接后会出现 5 行
- 统计时要注意**去重或分组**

==**左表过滤放 WHERE，右表过滤放 ON**==

*****

## 二、统计学：概率分布核心复习

### 1. 正态分布（高斯分布）

**形状**：中间高、两边低、左右对称，像一口钟

**核心特征**

- 均值 = 中位数 = 众数
- 大部分数据集中在中间，极端值很少
- 68-95-99.7 法则
  - 68% 在 ±1σ 内
  - 95% 在 ±2σ 内
  - 99.7% 在 ±3σ 内

**业务场景**

- 身高、体重、考试分数
- 用户平均使用时长、平均订单金额
- 质量检测、异常识别（偏离 3σ 视为异常）

**一句话记忆**

> 正常现象大多是正态分布，中间多两头少，越靠近均值越常见

### 2. 二项分布（n 次独立实验）

**前提**

- 只有两种结果：成功 / 失败
- 每次独立
- 概率固定

**核心**

- 做 n 次实验，**成功 k 次的概率**

**业务场景**

- 投放 100 个广告，有 10 个人点击的概率
- 100 个用户，5 个流失的概率
- 一批产品，出现次品数量的概率

**一句话记忆**

> 是 / 否、有 / 无、成功 / 失败，重复多次 → 二项分布

## 三、极简速记总结

### SQL JOIN

- **INNER**：交集，两边都有才要
- **LEFT**：左表全要，右表匹配
- **RIGHT**：右表全要，左表匹配
- **一对多会行数膨胀**

### 概率分布

- **正态**：连续、对称、钟形，自然 / 测量数据常用
- **二项**：离散、是 / 否、n 次实验，计数类场景常用

# 2026.03.19 周四

——实现日期：2026年3月24日

——实现日期：2026年3月27日

## 今日复习内容完整总结（精简好记版）

### 一、SQL 部分

#### 1. 多表联查核心

- **INNER JOIN**：只保留两边都匹配的数据（交集）
- **LEFT JOIN**：左表全保留，右表无匹配为 NULL（最常用）
- **RIGHT JOIN**：右表全保留，实际很少用
- 大坑：`LEFT JOIN` 后在 `WHERE` 里过滤右表非 NULL 字段，会变成内连接

#### 2. 子查询 & 关联子查询

- 子查询：查询嵌套查询，内层先执行
- **关联子查询**：依赖外层字段，外层一行执行一次
- **EXISTS**：只判断是否存在记录，找到即停，比 IN 更快
- **NOT EXISTS**：查 “不存在” 的记录（无订单 / 无确认用户）

#### 3. 子查询 vs JOIN

- **EXISTS/IN**：适合判断存在性
- **JOIN**：适合多字段展示、分组统计、大数据量性能更好

#### 4. 实战题型

- 计算用户确认率：`SUM(条件)/COUNT` + `LEFT JOIN` + `ROUND`
- 查有 / 无确认记录用户：`EXISTS / NOT EXISTS`

### 二、统计学基础

#### 1. 正态分布

- 钟形对称，均值 = 中位数 = 众数
- 3σ 原则：68-95-99.7
- 业务：用户时长、消费金额、异常检测

#### 2. 正态性验证（全套）

- 看图：直方图 + 拟合正态曲线
- QQ 图：点贴对角线 = 正态
- 检验：Shapiro（小样本）、K-S（大样本）
- 判断：**p > 0.05 服从正态**

#### 3. 皮尔逊相关系数

- 范围 [-1,1]，衡量**线性相关程度**
- 正相关：同增同减；负相关：此消彼长
- 只反映线性关系，不代表因果

### 三、一句话串起来

**SQL 用 JOIN 做统计、用 EXISTS 判断存在；统计用正态看分布、用相关看关系，业务落地做异常识别与指标分析。**

*****

## 1. SQL 进阶：子查询 & 嵌套查询

### （1）什么是子查询

- **查询里面套查询**，内层先执行，结果给外层用
- 按位置：`SELECT / FROM / WHERE` 子查询
- 按结果：标量、单行、多行、关联子查询

### （2）常用写法

- **WHERE 子查询**（筛选）

```sql
SELECT * FROM A WHERE id IN (SELECT id FROM B)
```

- **FROM 子查询**（先算临时表）

```sql
SELECT * FROM (SELECT ...) AS t
```

- **关联子查询**（逐行匹配）

```sql
SELECT ... FROM A WHERE EXISTS (SELECT 1 FROM B WHERE A.id=B.id)
```

### （3）优化逻辑（核心）

1. **少用关联子查询**（逐行循环，慢），优先 `JOIN`
2. **FROM 子查询 > WHERE 子查询**（减少扫描行数）
3. 能用 `JOIN` 实现绝不嵌套
4. 子查询结果尽量小，加索引、加 LIMIT
5. `EXISTS` 优于 `IN`（尤其大数据）

------

## 2. 统计学：皮尔逊相关系数

### （1）核心逻辑

- 衡量 **两个连续变量线性相关程度**
- 取值范围：**[-1, 1]**

### （2）解读规则

- **=1**：完全正相关
- **>0**：正相关（同增同减）
- **=0**：无线性关系
- **<0**：负相关（你增我减）
- **=-1**：完全负相关

### （3）业务解读

- 广告花费 ↑ → 销售额 ↑ → **正相关**
- 价格 ↑ → 销量 ↓ → **负相关**
- 用户年龄 ↑ → APP 使用时长 无规律 → **不相关**
- 只看**线性关系**，非线性相关会误判

## 一句话总结

- **SQL**：子查询先内后外，能用 JOIN 别嵌套，EXISTS 优于 IN
- **统计**：皮尔逊看线性，正同增、负此消彼长，范围 [-1,1]

## 进一步解释关联子查询以及exists的含义及用法

### 一、什么是关联子查询？

#### 定义

子查询**不是独立运行**的，它**依赖外层表的字段**，需要**逐行拿外层数据进去匹配**。

一句话：

**外层每查一行，就跑一次子查询。**

#### 示例结构

```sql
SELECT *
FROM 表A a
WHERE EXISTS (
    SELECT 1
    FROM 表B b
    WHERE a.user_id = b.user_id   -- 用了外层a的字段
);
```

特点：

- 不能单独执行子查询
- 执行效率取决于外层行数
- 适合 “判断是否存在” 的场景

### 二、EXISTS 到底是什么？

#### 核心含义

**EXISTS (子查询) → 判断：子查询有没有返回至少一行数据**

- 有返回 → TRUE
- 没返回 → FALSE

它**不关心返回什么内容**，只关心**有没有行**。

所以 EXISTS 里永远写：

```sql
SELECT 1
```

就行，不用写具体字段。

### 三、EXISTS 怎么用？（最经典场景）

#### 需求：找出**有订单的用户**

##### 写法 1：IN（简单但大数据慢）

```sql
SELECT *
FROM user
WHERE user_id IN (SELECT user_id FROM order);
```

##### 写法 2：EXISTS（推荐，更快）

```sql
SELECT *
FROM user u
WHERE EXISTS (
    SELECT 1
    FROM order o
    WHERE u.user_id = o.user_id
);
```

#### 执行逻辑（非常关键）

1. 从 user 取一条记录
2. 把 user_id 带入子查询
3. 看 order 里有没有匹配的
4. 有 → 保留这行；没有 → 丢掉
5. 继续下一行

这就是**关联子查询 + EXISTS**的工作方式。

### 四、NOT EXISTS 用法（高频）

#### 需求：找出**没有订单的用户**

```sql
SELECT *
FROM user u
WHERE NOT EXISTS (
    SELECT 1
    FROM order o
    WHERE u.user_id = o.user_id
);
```

业务场景极常用：

- 没下单的用户
- 没签到的用户
- 没评论的帖子
- 没回复的消息

### 五、EXISTS 为什么比 IN 快？（面试必问）

#### IN 的逻辑

- 子查询先一次性查出所有 id
- 外层再逐个匹配
- 子查询结果很大时 → 巨慢

#### EXISTS 的逻辑

- **找到一条匹配就立刻停止**，不继续查
- 不需要保存全部结果
- 有索引时极快

口诀：

**数据量大用 EXISTS，数据量小用 IN**

### 六、关联子查询 VS 普通子查询

#### 普通子查询（不相关）

子查询可以**单独运行**，只执行一次。

```sql
SELECT * FROM user
WHERE age > (SELECT AVG(age) FROM user);
```

#### 关联子查询

子查询**依赖外层字段**，外层多少行，子查询就跑多少次。

```sql
SELECT * FROM user u
WHERE EXISTS (SELECT 1 FROM order o WHERE u.id=o.uid);
```

### 七、最强总结（背这个）

#### 关联子查询

- 子查询用到**外层表字段**
- 外层一行，子查询执行一次
- 常用于**存在性判断**

#### EXISTS

- 判断子查询**是否返回至少一行**
- 返回 1/0，不关心内容
- 比 IN **更快**，尤其大数据
- 搭配 NOT EXISTS 查 “不存在” 的记录

### 万能模板

```sql
-- 查存在
WHERE EXISTS (SELECT 1 FROM 表B WHERE 表A.id = 表B.id)

-- 查不存在
WHERE NOT EXISTS (SELECT 1 FROM 表B WHERE 表A.id = 表B.id)
```

# 2026.03.20 周五

——实现日期：2026年3月27日

## SQL 窗口函数速背（ROW_NUMBER / RANK / DENSE_RANK）

超级精简、面试必考、一看就会

------

### 一、通用语法

```sql
窗口函数() OVER (
    PARTITION BY 分组字段
    ORDER BY 排序字段 DESC/ASC
)
```

- **PARTITION BY**：按某字段分组（类似 GROUP BY，但不合并行）
- **ORDER BY**：组内排序
- 三个函数只区别**排名规则**

------

### 二、三个函数核心区别（最重要）

假设有成绩：90、90、80

#### 1. ROW_NUMBER()

- **行号，永不重复，连续**
- 结果：1、2、3
- 即使值相同，也强行给不同排名

#### 2. RANK()

- **跳跃排名**
- 相同值同排名，下一名跳过
- 结果：1、1、3

#### 3. DENSE_RANK()

- **密集排名，不跳跃**
- 相同值同排名，下一名连续
- 结果：1、1、2

------

### 三、一句话记忆

- **ROW_NUMBER：不管重复，挨个排**
- **RANK：同分同名，然后跳号**
- **DENSE_RANK：同分同名，不跳号**

------

### 四、最经典业务场景（面试必考）

#### 场景 1：每个分类下取 TOP N

```sql
SELECT *
FROM (
    SELECT
        product_id,
        sale,
        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY sale DESC
        ) AS rn
    FROM sales
) t
WHERE rn <= 3;
```

#### 场景 2：成绩排名

```sql
SELECT
    name,
    score,
    RANK()       OVER (ORDER BY score DESC) AS rk,
    DENSE_RANK() OVER (ORDER BY score DESC) AS drk,
    ROW_NUMBER() OVER (ORDER BY score DESC) AS rn
FROM student;
```

------

### 五、高频坑点

- **ORDER BY 必须写**，否则排名无意义
- **PARTITION BY 不写 = 全表一起排名**
- 想要**不重复、严格顺序** → 用 ROW_NUMBER
- 想要**正常排名，允许并列** → 用 DENSE_RANK
- 想要**考试排名那种跳名次** → 用 RANK

------

### 六、终极口诀

行号连续不重复，

排名跳跃同分驻，

密集排名不跳步，

分区排序窗口助。





# 2026.03.21 周六

——实现2026年3月27日

## 拿到一个数据集，如何完成数据集的初步查看与理解

# 拿到数据集 → 初步查看与理解（极简可背诵版）

## 1. 先看整体长啥样

```python
df.head()      # 前5行
df.tail()      # 后5行
df.sample(5)   # 随机5行（更真实）
df.shape       # 行数、列数
df.columns     # 字段名
df.info()      # 字段类型、是否缺失
```

## 2. 看缺失值 & 异常

```python
df.isnull().sum()           # 每列缺失数量
df.isnull().mean() * 100    # 缺失百分比
df.duplicated().sum()       # 重复行数
```

## 3. 看数值型变量统计

```python
df.describe().T  # 均值、分位数、最大最小、标准差
```

快速判断：

- 最大 / 最小是否离谱（异常值）
- 均值和中位数差距大不大（偏态）

## 4. 看类别型变量

```python
df.select_dtypes(include='object').nunique()  # 多少类别
df['category_col'].value_counts()              # 各类别数量
```

## 5. 看变量间关系（相关性）

```python
df.corr()            # 相关系数
sns.heatmap(...)     # 热力图
```

## 6. 简单可视化（快速理解分布）

```python
df.hist(figsize=(12,10))        # 数值分布
sns.boxplot(data=df)            # 异常值
sns.pairplot(df)                # 两两关系
```



# 2026.03.23 周一

——实现日期：2026.04.08

——2026年4月9日

## 一、SQL 窗口函数进阶

### 1. 基础聚合窗口函数（SUM/AVG/MIN/MAX）

窗口函数格式：

```sql
聚合函数() OVER (
    PARTITION BY 分组字段
    ORDER BY 排序字段
    [ROWS/RANGE 窗口范围]
)
```

#### 常用聚合窗口

- `SUM() OVER(...)`：累计求和
- `AVG() OVER(...)`：累计 / 分组均值
- `MIN() / MAX() OVER(...)`：分组内极值

示例（按部门累计销售额）：

```sql
SELECT
    dept_id,
    sale_date,
    amount,
    SUM(amount) OVER(PARTITION BY dept_id ORDER BY sale_date) AS cum_amount
FROM sales;
```

------

### 2. 滑动窗口（行窗口 / 范围窗口）

#### （1）行窗口 ROWS

```sql
ROWS BETWEEN 起始 AND 结束
```

常用写法：

- `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`：从第一行到当前行（默认累计）
- `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`：前 2 行 + 当前行
- `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING`：前后各 1 行（共 3 行滑动）

#### （2）范围窗口 RANGE

按**值范围**而非行数，常用于连续数值 / 日期。

示例：3 日滑动平均

```sql
AVG(amount) OVER(
    PARTITION BY dept_id
    ORDER BY sale_date
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
) AS moving_avg_3d
```

------

## 二、统计学：推断统计核心

### 1. 推断统计核心逻辑

- 目的：用**样本**推断**总体**
- 核心思想：**抽样误差 + 概率规律**
- 两大分支：
  1. **参数估计**：估计总体未知参数（均值、比例等）
  2. **假设检验**：对总体参数做假设并判断是否成立

------

### 2. 参数估计

两种形式：

1. **点估计**

   用一个值估计总体参数

   例：样本均值 `x̄` → 估计总体均值 `μ`

2. **区间估计**

   给出一个区间，使总体参数以一定概率落在其中

   → 即**置信区间**

------

### 3. 置信区间

- 定义：在**置信水平 1−α**下，总体参数的估计区间
- 常见置信水平：90%、95%、99%
- 公式（大样本正态近似）：估计值±zα/2×标准误
- 含义：重复抽样多次，构造的区间中有 (1−α)×100% 包含真实总体参数

*****

## ———例子说明———

## 一、SQL 窗口函数进阶（统一测试数据）

先创建一张销售表，所有例子都基于这张表：

```sql
-- 测试数据：2个部门，6条销售记录
CREATE TABLE sales (
    dept_id INT,    -- 部门ID
    sale_date DATE, -- 销售日期
    amount INT      -- 销售额
);

INSERT INTO sales VALUES
(1, '2024-01-01', 100),
(1, '2024-01-02', 200),
(1, '2024-01-03', 300),
(2, '2024-01-01', 150),
(2, '2024-01-02', 250),
(2, '2024-01-03', 350);
```

### 1. 基础聚合窗口函数（对比 3 种写法）

#### 写法 1：无 PARTITION BY + 无 ORDER BY

```sql
SELECT *, SUM(amount) OVER() AS total_amount FROM sales;
```

**输出结果**：

|                           dept_id                            | sale_date  | amount | total_amount |
| :----------------------------------------------------------: | :--------: | :----: | :----------: |
|                              1                               | 2024-01-01 |  100   |     1350     |
|                              1                               | 2024-01-02 |  200   |     1350     |
|                              1                               | 2024-01-03 |  300   |     1350     |
|                              2                               | 2024-01-01 |  150   |     1350     |
|                              2                               | 2024-01-02 |  250   |     1350     |
|                              2                               | 2024-01-03 |  350   |     1350     |
| **解释**：整个表作为一个窗口，计算所有行的总和，每行都显示全局总和。 |            |        |              |

#### 写法 2：有 PARTITION BY + 无 ORDER BY

```sql
SELECT *, SUM(amount) OVER(PARTITION BY dept_id) AS dept_total FROM sales;
```

**输出结果**：

|                           dept_id                            | sale_date  | amount | dept_total |
| :----------------------------------------------------------: | :--------: | :----: | :--------: |
|                              1                               | 2024-01-01 |  100   |    600     |
|                              1                               | 2024-01-02 |  200   |    600     |
|                              1                               | 2024-01-03 |  300   |    600     |
|                              2                               | 2024-01-01 |  150   |    750     |
|                              2                               | 2024-01-02 |  250   |    750     |
|                              2                               | 2024-01-03 |  350   |    750     |
| **解释**：按部门分组，每个部门作为一个独立窗口，计算部门内总和。 |            |        |            |

#### 写法 3：有 PARTITION BY + 有 ORDER BY（最常用）

```sql
SELECT *, SUM(amount) OVER(PARTITION BY dept_id ORDER BY sale_date) AS cum_amount FROM sales;
```

**输出结果**：

|                           dept_id                            | sale_date  | amount | cum_amount |
| :----------------------------------------------------------: | :--------: | :----: | :--------: |
|                              1                               | 2024-01-01 |  100   |    100     |
|                              1                               | 2024-01-02 |  200   |    300     |
|                              1                               | 2024-01-03 |  300   |    600     |
|                              2                               | 2024-01-01 |  150   |    150     |
|                              2                               | 2024-01-02 |  250   |    400     |
|                              2                               | 2024-01-03 |  350   |    750     |
| **解释**：按部门分组，组内按日期排序，**从第一行累计到当前行**（这是默认窗口范围）。 |            |        |            |

### 2. 滑动窗口计算（核心难点）

#### 例子 1：3 日滑动平均（ROWS 行窗口）

计算 "当天 + 前 2 天" 的平均销售额（共 3 天）：

```sql
SELECT
    *,
    AVG(amount) OVER(
        PARTITION BY dept_id
        ORDER BY sale_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg_3d
FROM sales;
```

**输出结果**：

|  dept_id   | sale_date  | amount | moving_avg_3d |
| :--------: | :--------: | :----: | :-----------: |
|     1      | 2024-01-01 |  100   |     100.0     |
|     1      | 2024-01-02 |  200   |     150.0     |
|     1      | 2024-01-03 |  300   |     200.0     |
|     2      | 2024-01-01 |  150   |     150.0     |
|     2      | 2024-01-02 |  250   |     200.0     |
|     2      | 2024-01-03 |  350   |     250.0     |
| **解释**： |            |        |               |

- 1 月 1 日：只有自己 → 平均 100
- 1 月 2 日：1 日 + 2 日 → (100+200)/2=150
- 1 月 3 日：1 日 + 2 日 + 3 日 → (100+200+300)/3=200

#### 例子 2：ROWS vs RANGE 关键区别（必懂）

**ROWS**：按**行数**计算窗口

**RANGE**：按**值的范围**计算窗口

修改测试数据，加入一个重复日期：

```sql
INSERT INTO sales VALUES (1, '2024-01-03', 400);
```

对比两个查询：

```sql
-- ROWS：前1行 + 当前行（共2行）
SELECT *, SUM(amount) OVER(ORDER BY sale_date ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS sum_rows FROM sales;

-- RANGE：日期相同的所有行 + 前1个日期的所有行
SELECT *, SUM(amount) OVER(ORDER BY sale_date RANGE BETWEEN 1 PRECEDING AND CURRENT ROW) AS sum_range FROM sales;
```

**输出对比**：

|   sale_date    | amount | sum_rows | sum_range |
| :------------: | :----: | :------: | :-------: |
|   2024-01-01   |  100   |   100    |    100    |
|   2024-01-02   |  200   |   300    |    300    |
|   2024-01-03   |  300   |   500    |    900    |
|   2024-01-03   |  400   |   700    |    900    |
| **关键区别**： |        |          |           |

- ROWS：严格按行数，300 那行只加了前一行 200 → 500
- RANGE：按日期值，所有 1 月 3 日的行都加 1 月 2 日的 200 → 200+300+400=900

------

## 二、推断统计核心（用 "估计全校学生身高" 举例）

### 1. 推断统计核心逻辑

**问题**：想知道某大学 10000 名学生的平均身高（总体均值 μ），不可能一个个测。

**推断过程**：

1. 随机抽取 100 名学生（样本）

2. 计算这 100 人的平均身高（样本均值 x̄=168cm）

3. 用样本均值 x̄推断总体均值 μ

   

   核心思想

   ：抽样误差不可避免，但我们可以用概率来量化这个误差。

### 2. 参数估计：点估计 vs 区间估计

#### 点估计

用一个具体数值估计总体参数：

- 点估计值：168cm
- 优点：简单明确
- 缺点：完全没有考虑抽样误差，几乎不可能正好等于真实值

#### 区间估计（置信区间）

给出一个区间，说明总体参数有多大可能落在这个区间里。

**完整计算例子**：

已知：

- 样本量 n=100
- 样本均值 x̄=168cm
- 样本标准差 s=5cm
- 置信水平 95% → 对应的 z 值 = 1.96（记住这个常用值）

**计算标准误**：

SE=ns=1005=0.5

**计算 95% 置信区间**：

xˉ±zα/2×SE=168±1.96×0.5=[167.02,168.98]

### 3. 置信区间的正确含义（90% 的人都理解错了！）

❌ **错误理解**："全校学生的平均身高有 95% 的概率落在 [167.02, 168.98] 这个区间里"

✅ **正确理解**："如果我们重复抽样 100 次，每次都计算一个 95% 置信区间，那么这 100 个区间中，大约有 95 个会包含真实的全校平均身高"

**通俗解释**：

置信区间不是说 "真实值在这个区间里的概率是 95%"，而是说 "我们用这个方法构造的区间，有 95% 的概率能抓住真实值"。真实值是固定的，变的是我们构造的区间。
