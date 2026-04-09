[TOC]



# 2026.03.16

* **null要用is，而不能用=**

* length()：字符串长度函数



# 2026.03.17

## 进店却未进行过交易的顾客

* 问题描述

  表：`Visits`

  ```
  +-------------+---------+
  | Column Name | Type    |
  +-------------+---------+
  | visit_id    | int     |
  | customer_id | int     |
  +-------------+---------+
  visit_id 是该表中具有唯一值的列。
  该表包含有关光临过购物中心的顾客的信息。
  ```

  表：`Transactions`

  ```
  +----------------+---------+
  | Column Name    | Type    |
  +----------------+---------+
  | transaction_id | int     |
  | visit_id       | int     |
  | amount         | int     |
  +----------------+---------+
  transaction_id 是该表中具有唯一值的列。
  此表包含 visit_id 期间进行的交易的信息。
  ```

  有一些顾客可能光顾了购物中心但没有进行交易。请你编写一个解决方案，来查找这些顾客的 ID ，以及他们只光顾不交易的次数。

  返回以 **任何顺序** 排序的结果表。

  返回结果格式如下例所示。

* 示例

  ```
  输入:
  Visits
  +----------+-------------+
  | visit_id | customer_id |
  +----------+-------------+
  | 1        | 23          |
  | 2        | 9           |
  | 4        | 30          |
  | 5        | 54          |
  | 6        | 96          |
  | 7        | 54          |
  | 8        | 54          |
  +----------+-------------+
  Transactions
  +----------------+----------+--------+
  | transaction_id | visit_id | amount |
  +----------------+----------+--------+
  | 2              | 5        | 310    |
  | 3              | 5        | 300    |
  | 9              | 5        | 200    |
  | 12             | 1        | 910    |
  | 13             | 2        | 970    |
  +----------------+----------+--------+
  输出:
  +-------------+----------------+
  | customer_id | count_no_trans |
  +-------------+----------------+
  | 54          | 2              |
  | 30          | 1              |
  | 96          | 1              |
  +-------------+----------------+
  解释:
  ID = 23 的顾客曾经逛过一次购物中心，并在 ID = 12 的访问期间进行了一笔交易。
  ID = 9 的顾客曾经逛过一次购物中心，并在 ID = 13 的访问期间进行了一笔交易。
  ID = 30 的顾客曾经去过购物中心，并且没有进行任何交易。
  ID = 54 的顾客三度造访了购物中心。在 2 次访问中，他们没有进行任何交易，在 1 次访问中，他们进行了 3 次交易。
  ID = 96 的顾客曾经去过购物中心，并且没有进行任何交易。
  如我们所见，ID 为 30 和 96 的顾客一次没有进行任何交易就去了购物中心。顾客 54 也两次访问了购物中心并且没有进行任何交易。
  ```

* 经过再摸索，再分析，拆解表结构，以及字段含义，推测要用group by以及子查询

  ```sql
  -- 将Transactions表的visit_id字段提取出来，表示进行过消费的到访记录
  select visit_id from Transactions group by visit_id;
  
  -- 查询Visits表中不含上述visit_id值的记录
  select * from Visits where visit_id not in ();
  
  -- 根据题目要求修改查询结果表的字段
  select customer_id, count(customer_id) count_no_trans from Visits where visit_id not in
  (select visit_id from Transactions group by visit_id) group by customer_id;
  
  -- 通过看题解优化
  select customer_id, count(customer_id) count_no_trans from Visits where visit_id not in
  (select visit_id from Transactions ) group by customer_id;
  ```

  

## 上升的温度

* 问题描述

  表： `Weather`

  ```
  +---------------+---------+
  | Column Name   | Type    |
  +---------------+---------+
  | id            | int     |
  | recordDate    | date    |
  | temperature   | int     |
  +---------------+---------+
  id 是该表具有唯一值的列。
  没有具有相同 recordDate 的不同行。
  该表包含特定日期的温度信息
  ```

   

  编写解决方案，找出与之前（昨天的）日期相比温度更高的所有日期的 `id` 。

  返回结果 **无顺序要求** 。

  结果格式如下例子所示。

* 示例

  **示例 1：**

  ```
  输入：
  Weather 表：
  +----+------------+-------------+
  | id | recordDate | Temperature |
  +----+------------+-------------+
  | 1  | 2015-01-01 | 10          |
  | 2  | 2015-01-02 | 25          |
  | 3  | 2015-01-03 | 20          |
  | 4  | 2015-01-04 | 30          |
  +----+------------+-------------+
  输出：
  +----+
  | id |
  +----+
  | 2  |
  | 4  |
  +----+
  解释：
  2015-01-02 的温度比前一天高（10 -> 25）
  2015-01-04 的温度比前一天高（20 -> 30）
  ```

* 难点分析

  1. 如何表示前一天？跨月份那有该如何？date类型数据+1天如何计算？

     ```sql
     SELECT DATE_ADD('2023-01-01', INTERVAL 1 DAY);
     ```

* 解决：

  ```sql
  select w1.id from  Weather w1, Weather w2
  where w1.recordDate = DATE_ADD(w2.recordDate, INTERVAL 1 DAY) and w1.Temperature > w2.Temperature;
  ```

* 题解学习

  * Q：如何比较日期数据？针对于日期类型数据Date

    【解题思路】

    1.交叉联结

    首先我们来复习一下之前课程《从零学会sql》里讲过的交叉联结（corss join）的概念。

    使用交叉联结会将两个表中所有的数据两两组合。如下图，是对表“text”自身进行交叉联结的结果：

    ![image-20260317144538690](E:\系统默认\桌面\Plan\求职\实践\leetcode\MySQL\picture\image-20260317144538690.png)


    直接使用交叉联结的业务需求比较少见，往往需要结合具体条件，对数据进行有目的的提取，本题需要结合的条件就是“前一天”。
    
    2.本题的日销表交叉联结的结果（部分）如下。这个交叉联结的结果表，可以看作左边三列是表a，右边三列是表b。
    
    ![image-20260317144556639](E:\系统默认\桌面\Plan\求职\实践\leetcode\MySQL\picture\image-20260317144556639.png)


    红色框中的每一行数据，左边是“当天”数据，右边是“前一天”的数据。比如第一个红色框中左边是“当天”数据（2号），右边是“前一天”的数据（1号）。
    
    题目要求，销售额条件是：“当天” > “昨天”（前一天）。所以，对于上面的表，我们只需要找到表a中销售额（当天）大于b中销售额（昨天）的数据。
    
    3.另一个需要着重去考虑的，就是如何找到 “昨天”（前一天），这里为大家介绍两个时间计算的函数：
    datediff(日期1, 日期2)：
    得到的结果是日期1与日期2相差的天数。
    如果日期1比日期2大，结果为正；如果日期1比日期2小，结果为负。
    
    例如：日期1（2019-01-02），日期2（2019-01-01），两个日期在函数里互换位置，就是下面的结果
    
    ![image-20260317144626293](E:\系统默认\桌面\Plan\求职\实践\leetcode\MySQL\picture\image-20260317144626293.png)
    
    另一个关于时间计算的函数是：
    timestampdiff(时间类型, 日期1, 日期2)
    这个函数和上面diffdate的正、负号规则刚好相反。
    日期1大于日期2，结果为负，日期1小于日期2，结果为正。
    
    在“时间类型”的参数位置，通过添加“day”, “hour”, “second”等关键词，来规定计算天数差、小时数差、还是分钟数差。示例如下图：
    
    ![image-20260317144642161](E:\系统默认\桌面\Plan\求职\实践\leetcode\MySQL\picture\image-20260317144642161.png)
    
    【解题步骤】
    1.将日销表进行交叉联结
    
    ![image-20260317144931666](E:\系统默认\桌面\Plan\求职\实践\leetcode\MySQL\picture\image-20260317144931666.png)


    2.选出上图红框中的“a.日期比b.日期大一天”
    
    可以使用“diffdate(a.日期, b.日期) = 1”或者“timestampdiff(day, a.日期, b.日期) = -1”，以此为基准，提取表中的数据，这里先用diffdate进行操作。
    
    代码部分：
    
    ```sql
    select *
    from 日销 as a cross join 日销 as b 
         on datediff(a.日期, b.日期) = 1;
    ```
    
    得到结果：
    
    ![image-20260317144956889](E:\系统默认\桌面\Plan\求职\实践\leetcode\MySQL\picture\image-20260317144956889.png)


    3.找出a中销售额大于b中销售额的数据
    
    where a.销售额（万元） > b.销售额（万元）
    
    得到结果：
    
    ![image-20260317145022549](E:\系统默认\桌面\Plan\求职\实践\leetcode\MySQL\picture\image-20260317145022549.png)


    4.删掉多余数据
    
    题目只需要找销售额大于前一天的ID、日期、销售额，不需要上表那么多数据。所以只需要提取中上表的ID、日期、销售额（万元）列。
    结合一开始提到的两个处理时间的方法，最终答案及结果如下：
    
    ```sql
    select a.ID, a.日期, a.销售额（万元）
    from 日销 as a cross join 日销 as b 
         on datediff(a.日期, b.日期) = 1
    where a.销售额（万元） > b.销售额（万元）;
    ```
    
    或者
    
    ```sql
    select a.ID, a.日期, a.销售额（万元）
    from 日销 as a cross join 日销 as b 
         on timestampdiff(day, a.日期, b.日期) = -1
    where a.销售额（万元） > b.销售额（万元）;
    ```
    
    ![image-20260317145044715](E:\系统默认\桌面\Plan\求职\实践\leetcode\MySQL\picture\image-20260317145044715.png)
    
    【本题考点】
    1）考察逻辑思维能力，可以使用课程《分析方法》中的逻辑树分析方法将复杂问题拆解成一个一个可以解决的子问题
    2）考察多表联结
    3）针对时间的处理语句是在业务中经常用到的，需要熟练掌握。
    4） 尤其考察对不同sql数据格式处理的掌握程度
    
    作者：猴子数据分析
    链接：https://leetcode.cn/problems/rising-temperature/solutions/50468/tu-jie-sqlmian-shi-ti-ru-he-bi-jiao-ri-qi-shu-ju-b/
    来源：力扣（LeetCode）

  * 举一反三：题解参考答案

    ```sql
    select a.ID, a.date
    from weather as a cross join weather as b 
         on datediff(a.date, b.date) = 1
    where a.temp > b.temp;
    ```

    或者

    ```sql
    select a.ID, a.date
    from weather as a cross join weather as b 
         on timestampdiff(day, a.date, b.date) = -1
    where a.temp > b.temp;
    ```

    

    

    

    

# 2026.03.18-

# 2026.03.19-

# 2026.03.20

## 每台机器的进程平均运行时间

* 如何保留三位小数？

  * 直接用round()函数

  * **ROUND 与 TRUNC 的区别**：

    - `ROUND` 是四舍五入（符合日常计数习惯）；
    - `TRUNC` 是直接截断（适合不需要四舍五入的场景，如财务精准计算）。

  * 使用例子

    * ```sql
      -- 示例：保留 2 位小数
      SELECT 
        ROUND(3.14159, 2) AS num1,  -- 结果：3.14
        TRUNC(3.14999, 2) AS num2,  -- 结果：3.14（截断，不四舍五入）
        ROUND(3.145, 2) AS num3     -- 结果：3.15
      FROM DUAL;
      ```

* 发生报错：Every derived table must have its own alias**【每个派生表都必须有自己的别名】**

  * 在 SQL 中，**派生表** 指的是通过 `SELECT` 语句生成的临时结果集（通常出现在 `FROM` 子句中，比如子查询），数据库引擎需要给这个临时表分配一个唯一的别名来识别它，否则会报这个错误。

  * ### 常见触发场景

    1. `FROM` 子句中直接使用子查询作为数据源，但未加别名；
    2. `JOIN` 关联的子查询（派生表）未加别名；
    3. 嵌套子查询中，内层查询作为派生表未命名（比如多层 `FROM (SELECT ...)` 结构）。

* 题解学习

  * 更快更简单的做法

    * ```sql
      select t1.machine_id, round(avg(t2.timestamp - t1.timestamp), 3) processing_time
      from activity t1, activity t2
      where t1.machine_id = t2.machine_id 
          and t1.process_id = t2.process_id 
          and t1.activity_type = 'start' 
          and t2.activity_type = 'end'
      group by t1.machine_id
      ```


# 2026.03.21-

# 2026.03.22-

# 2026.03.23

## 学生们参加各科测试的次数

* 如何查找两张表的所有组合？

  * ——“笛卡尔积”

    ```sql
    select * from table1, table2 (where...);  -- 平时用where来删除多余的笛卡尔积
    ```

  * 用“cross join”生成全组合

* 如何给查询字段增加默认值？

  * 在 SQL 中给查询字段设置默认值，核心是利用**条件函数**（如 `IFNULL`/`COALESCE`/`CASE WHEN`）处理字段为 `NULL` 的情况，或用 `AS` 直接给固定值字段命名。不同数据库的函数略有差异，以下以最常用的 MySQL 为例讲解，同时补充通用方案。

    ### 具体场景及代码示例

    #### 场景 1：处理 NULL 值，设置默认值（最常用）

    当字段值为 `NULL` 时（比如左连接后无匹配数据），用 `IFNULL` 或 `COALESCE` 替换为指定默认值。

    **示例**：基于你之前的考试次数查询，给 `attended_exams` 字段设置默认值 0（无考试记录时显示 0）：

    ```sql
    SELECT 
      s.student_id,
      s.student_name,
      s.subject_name,
      -- 核心：IFNULL(字段, 默认值)，字段为NULL时返回默认值
      IFNULL(e.attended_exams, 0) AS attended_exams
    FROM (
      SELECT student_id, student_name, subject_name 
      FROM Students, Subjects 
      ORDER BY student_id ASC, subject_name
    ) AS s 
    LEFT JOIN (
      SELECT student_id, subject_name, COUNT(student_id) AS attended_exams 
      FROM Examinations 
      GROUP BY student_id, subject_name
    ) AS e 
    ON s.student_id = e.student_id AND s.subject_name = e.subject_name;
    ```

    #### 场景 2：新增固定默认值字段

    查询时新增一个字段，所有行都显示同一个默认值（比如标记数据来源）：

    ```sql
    SELECT 
      student_id,
      student_name,
      -- 新增字段，默认值为'未毕业'
      '未毕业' AS status,
      -- 新增数字类型默认值
      1 AS is_valid
    FROM Students;
    ```

    #### 场景 3：多条件默认值（CASE WHEN）

    根据字段值动态设置默认值（比如分数 <60 时显示 “不及格”，否则显示实际分数）：

    ```sql
    SELECT 
      student_id,
      subject_name,
      -- CASE WHEN 实现多条件默认值
      CASE 
        WHEN score IS NULL THEN 0  -- 无分数时默认0
        WHEN score < 60 THEN '不及格'  -- 分数<60显示文字
        ELSE score  -- 其他情况显示实际分数
      END AS score_result
    FROM Examinations;
    ```

    #### 场景 4：通用方案（COALESCE，适配多数据库）

    `COALESCE` 是 ANSI 标准函数，支持多个参数，返回第一个非 NULL 值，适配 MySQL、Oracle、SQL Server 等：

    ```sql
    SELECT 
      student_id,
      -- 优先取nickname，无则取name，仍无则取'未知'
      COALESCE(nickname, name, '未知') AS real_name
    FROM Students;
    ```

    ### 不同数据库的默认值函数对比

    |   数据库   |         处理 NULL 的函数          |        示例        |
    | :--------: | :-------------------------------: | :----------------: |
    |   MySQL    |       IFNULL (字段，默认值)       |  IFNULL(score, 0)  |
    |   Oracle   |        NVL (字段，默认值)         |   NVL(score, 0)    |
    | SQL Server |       ISNULL (字段，默认值)       |  ISNULL(score, 0)  |
    |    通用    | COALESCE (字段 1, 字段 2, 默认值) | COALESCE(score, 0) |

## 题解学习

豆包生成的代码更快：

```sql
SELECT
  s.student_id,
  s.student_name,
  sub.subject_name,
  IFNULL(e.attended_exams, 0) AS attended_exams
FROM Students s
CROSS JOIN Subjects sub
LEFT JOIN (
  -- 预聚合：先统计每个学生-科目的考试次数
  SELECT student_id, subject_name, COUNT(*) AS attended_exams
  FROM Examinations
  GROUP BY student_id, subject_name
) e ON s.student_id = e.student_id AND sub.subject_name = e.subject_name
ORDER BY s.student_id, sub.subject_name;
```

对比我的第一版代码：

```sql
select 
s.student_id, s.student_name, s.subject_name, coalesce(e.attended_exams, 0) as attended_exams 
from 
(select student_id, student_name, subject_name from Students, Subjects ) as s 
left join 
(select student_id, subject_name, count(student_id) attended_exams 
from 
Examinations 
group by 
student_id, subject_name) as e 
on 
s.student_id = e.student_id 
and 
s.subject_name=e.subject_name 
order by 
s.student_id asc, s.subject_name;
```

*****

# 2026.03.24

## 确认率

——能跑的出来但是很繁琐，同一个表做了多次查询同一列

```sql
select s.user_id, ifnull(c.confirmation_rate, 0.00) as confirmation_rate
from 
Signups s 
left join
 (select 
c1.user_id,  round(ifnull(c2.confirmed, 0) / c1.total, 2) as confirmation_rate
from 
(select user_id, count(action) as total from Confirmations group by user_id) as c1 
left join 
(select user_id, count(action) as confirmed from Confirmations where action = 'confirmed' group by user_id) as c2
on c1.user_id=c2.user_id) c 
on
s.user_id=c.user_id 
order by confirmation_rate desc;
```

![image-20260324152636827](E:\系统默认\桌面\Plan\求职\实践\leetcode\MySQL\picture\image-20260324152636827.png)

### 题解学习

#### 题解1：28%——avg聚合函数

```sql
SELECT
    s.user_id,
    ROUND(IFNULL(AVG(c.action='confirmed'), 0), 2) AS confirmation_rate
FROM
    Signups AS s
LEFT JOIN
    Confirmations AS c
ON
    s.user_id = c.user_id
GROUP BY
    s.user_id
```

#### 题解2：47%【豆包】

```sql
SELECT
    s.user_id,
    ROUND(
        -- 如果总请求数为0，返回0；否则 成功数/总数
        IFNULL(SUM(c.action = 'confirmed') / COUNT(c.action), 0),
        2
    ) AS confirmation_rate
FROM Signups s
LEFT JOIN Confirmations c
ON s.user_id = c.user_id
GROUP BY s.user_id;
```

# 2026.03.25-

# 2026.03.26-

# 2026.03.27

## 有趣的电影

* 如何算奇数？
  * 对2取余数=1
  * mod()取模【余】函数——**【性能更高一些】**

## 平均售价

* 如何判断一个date是否在另外两个date之间呢？

  在 SQL 里判断一个日期是否在**另外两个日期之间**，有两种最常用写法，**MySQL 通用**。

  ------

  ## 1. 最标准、最通用写法：`>=` 和 `<=`

  ```sql
  WHERE date_col >= start_date
    AND date_col <= end_date
  ```

  示例：

  ```sql
  SELECT *
  FROM orders
  WHERE order_time >= '2025-01-01'
    AND order_time <= '2025-01-31'
  ```

  ------

  ## 2. 更简洁写法：`BETWEEN ... AND ...`

  ```sql
  WHERE date_col BETWEEN start_date AND end_date
  ```

  等价于：

  ```sql
  date_col >= start_date AND date_col <= end_date
  ```

  示例：

  ```sql
  SELECT *
  FROM orders
  WHERE order_time BETWEEN '2025-01-01' AND '2025-01-31'
  ```

  ------

  ## 3. 重要注意点（必看）

  - **BETWEEN 是闭区间**：包含起止日期这两天

  - 如果你想

    不包含结束那一天

    ，就不要用 BETWEEN

    ```sql
    WHERE order_time >= '2025-01-01'
      AND order_time <  '2025-02-01'
    ```

  - 日期字段如果带时间（`datetime`），**直接用 BETWEEN 也没问题**

  ------

  ## 4. 放到你之前的题目里举例

  比如筛选 2021 年的确认记录：

  ```sql
  SELECT *
  FROM Confirmations
  WHERE time_stamp BETWEEN '2021-01-01' AND '2021-12-31'
  ```

  ------

  一句话总结：

  - **闭区间（包含头尾）**：`BETWEEN A AND B`
  - **灵活区间**：`>= A AND < B`（最稳妥，适合 datetime）

* 输出结果与预期不符？

  ```txt
  select u.product_id,round(sum(u.units * p.price) / sum(u.units), 2) as average_price
  from UnitsSold u
  left join 
  Prices p
  on
  u.product_id = p.product_id
  and
  u.purchase_date between p.start_date and p.end_date
  group by u.product_id
  ;
  对于上述SQL代码，如果输入是：
  Prices =
  | product_id | start_date | end_date   | price |
  | ---------- | ---------- | ---------- | ----- |
  | 1          | 2023-01-01 | 2023-01-31 | 10    |
  | 2          | 2023-01-01 | 2023-01-31 | 20    |
  UnitsSold =
  | product_id | purchase_date | units |
  | ---------- | ------------- | ----- |
  解释为什么结果是：
  | product_id | average_price |
  | ---------- | ------------- |
  如何达到预期输出结果：
  | product_id | average_price |
  | ---------- | ------------- |
  | 1          | 0             |
  | 2          | 0             |
  ```

  * 解释

    # 🔥 超级清晰解释：为什么你的 SQL 结果**空了** + 如何改成输出 0

    我直接把**原理 + 错误原因 + 正确代码**一次性讲透！

    ------

    ## 一、先看你的输入

    **Prices 表：有产品 1、2**

    **UnitsSold 表：空表（没有任何销售记录）**

    你的 SQL：

    ```sql
    select 
        u.product_id,
        round(sum(u.units * p.price) / sum(u.units), 2) as average_price
    from UnitsSold u
    left join Prices p
      on u.product_id = p.product_id
      and u.purchase_date between p.start_date and p.end_date
    group by u.product_id;
    ```

    ------

    # 二、为什么结果是空的？（核心关键）

    ### 因为：

    **主表是 UnitsSold（空表）**

    ```sql
    FROM UnitsSold u
    ```

    → 主表**一条记录都没有**

    → `LEFT JOIN` 也不会凭空生成记录

    → `GROUP BY` 没有数据可以分组

    → **最终结果 = 空**

    ------

    # 三、你想要的结果：

    ```plaintext
    product_id | average_price
    1          | 0
    2          | 0
    ```

    要实现这个，必须满足：

    1. **所有产品都出现（从 Prices 表取）**
    2. 没销量 → 平均价格 = 0

    ------

    # 四、正确 SQL（必背）

    ## 正确逻辑：

    **主表必须是 Prices（所有产品）**

    LEFT JOIN 销售记录

    没销量 → 返回 0

    ```sql
    SELECT
        p.product_id,
        ROUND(
            IFNULL(
                SUM(u.units * p.price) / SUM(u.units),
                0
            ),
            2
        ) AS average_price
    FROM Prices p                  -- 主表换成 Prices（保证产品都在）
    LEFT JOIN UnitsSold u
        ON p.product_id = u.product_id
        AND u.purchase_date BETWEEN p.start_date AND p.end_date
    GROUP BY p.product_id;
    ```

    ------

    # 五、为什么这样就对了？

    1. FROM Prices

       保证产品 1、2 一定会出现

    2. LEFT JOIN UnitsSold

       没销量 → u 表字段全部为 NULL

    3. IFNULL(..., 0)

       ```plaintext
       SUM(u.units)
       ```

        为 NULL → 变成 0

    4. 最终输出：

    ```plaintext
    1 → 0
    2 → 0
    ```

    ------

    # 六、终极总结（面试必背）

    ## 你的错误：

    **主表用了空表 UnitsSold → 结果为空**

    ## 正确原则：

    - **要显示所有商品 → 主表必须是商品表（Prices）**
    - **要显示没销量的商品 → 必须用 IFNULL 把 NULL 变 0**

    ------

    ## 最终正确输出

    ```plaintext
    product_id | average_price
    1          | 0.00
    2          | 0.00
    ```

# 2026.04.09

## 各赛事的用户注册率

### 题目描述

用户表： `Users`

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| user_id     | int     |
| user_name   | varchar |
+-------------+---------+
user_id 是该表的主键(具有唯一值的列)。
该表中的每行包括用户 ID 和用户名。
```

 注册表： `Register`

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| contest_id  | int     |
| user_id     | int     |
+-------------+---------+
(contest_id, user_id) 是该表的主键(具有唯一值的列的组合)。
该表中的每行包含用户的 ID 和他们注册的赛事。
```

 编写解决方案统计出各赛事的用户注册百分率，保留两位小数。

返回的结果表按 `percentage` 的 **降序** 排序，若相同则按 `contest_id` 的 **升序** 排序。

返回结果如下示例所示。

 **示例 1：**

```
输入：
Users 表：
+---------+-----------+
| user_id | user_name |
+---------+-----------+
| 6       | Alice     |
| 2       | Bob       |
| 7       | Alex      |
+---------+-----------+

Register 表：
+------------+---------+
| contest_id | user_id |
+------------+---------+
| 215        | 6       |
| 209        | 2       |
| 208        | 2       |
| 210        | 6       |
| 208        | 6       |
| 209        | 7       |
| 209        | 6       |
| 215        | 7       |
| 208        | 7       |
| 210        | 2       |
| 207        | 2       |
| 210        | 7       |
+------------+---------+
输出：
+------------+------------+
| contest_id | percentage |
+------------+------------+
| 208        | 100.0      |
| 209        | 100.0      |
| 210        | 100.0      |
| 215        | 66.67      |
| 207        | 33.33      |
+------------+------------+
解释：
所有用户都注册了 208、209 和 210 赛事，因此这些赛事的注册率为 100% ，我们按 contest_id 的降序排序加入结果表中。
Alice 和 Alex 注册了 215 赛事，注册率为 ((2/3) * 100) = 66.67%
Bob 注册了 207 赛事，注册率为 ((1/3) * 100) = 33.33%
```

### Q&A

为啥运行这行sql代码会发生报错

```sql
select r.contest_id, count(r.user_id)/count(u.*)
from Register r
left join
Users u
on r.user_id = u.user_id
group by r.contest_id;
```

* **解释**

  * ### 一、你的代码错误分析

    #### 1. 语法错误：`COUNT(u.*)` 不合法

    SQL 中 `COUNT` 函数的参数仅支持两种形式：

    - `COUNT(*)`：统计所有行数（包含 NULL 值）；

    - `COUNT(列名/表达式)`：统计指定列 / 表达式非 NULL的行数。

      你写的 `COUNT(u.*)`==**试图用 “表别名.*” 作为参数，这是 SQL 语法不允许的，会直接导致报错**==。

    #### 2. 逻辑错误：无法正确计算 “总用户数”

    题目要求的是「**某赛事的注册用户数 ÷ 所有用户总数**」，但你的代码逻辑存在两个问题：

    - 用 `LEFT JOIN Register r ON Users u` 后按 `r.contest_id` 分组，此时每个分组内的数据仅与 “该赛事的注册用户” 相关，**无法通过 `COUNT(u.\*)` 得到全表的总用户数**；
    - 由于 `Register` 表的主键是 `(contest_id, user_id)`，本身已保证无重复注册，其实不需要 `JOIN Users` 表来验证用户有效性（题目逻辑中注册用户必然存在于 Users 表）。

    ### 二、正确解决方案

    根据题目需求（统计百分率、保留两位小数、排序），SQL 代码如下：

    ```sql
    SELECT
      contest_id,
      -- 计算百分比：注册用户数 / 总用户数 * 100，保留两位小数
      ROUND(COUNT(user_id) * 100.0 / (SELECT COUNT(*) FROM Users), 2) AS percentage
    FROM Register
    GROUP BY contest_id
    -- 按 percentage 降序，若相同则按 contest_id 升序
    ORDER BY percentage DESC, contest_id ASC;
    ```

    ### 三、代码解释

    1. **总用户数计算**：用子查询 `(SELECT COUNT(*) FROM Users)` 直接获取所有用户总数，这是一个固定值；
    2. **注册用户数计算**：`COUNT(user_id)` 统计每个赛事的注册用户数（因 `Register` 主键无重复，直接计数即可）；
    3. **百分比计算**：`COUNT(user_id) * 100.0 / 总用户数` 确保结果为小数（`*100.0` 避免整数除法），再用 `ROUND(..., 2)` 保留两位小数；
    4. **排序**：`ORDER BY percentage DESC, contest_id ASC` 满足题目排序要求。

* 其他方法【cross join——强制组合】

  * ### 一、不用子查询的解法：`CROSS JOIN + 窗口函数`

    可以通过**交叉连接（CROSS JOIN）\**将用户总表的信息 “带到” 注册表中，再结合\**窗口函数**计算总用户数，完全避免子查询：

    ```sql
    SELECT DISTINCT
      r.contest_id,
      ROUND(
        -- 每个赛事的注册用户数（去重）
        COUNT(DISTINCT r.user_id) OVER(PARTITION BY r.contest_id) * 100.0 / 
        -- 总用户数（全局去重）
        COUNT(DISTINCT u.user_id) OVER(), 
        2
      ) AS percentage
    FROM Register r
    -- 交叉连接：将注册表的每一行与用户表的每一行组合
    CROSS JOIN Users u
    ORDER BY percentage DESC, r.contest_id ASC;
    ```

    #### 代码逻辑解释：

    1. ==**`CROSS JOIN Users u`**：将 `Register` 表的每一行与 `Users` 表的每一行强制组合（比如示例中 `Register` 有 12 行，`Users` 有 3 行，交叉连接后生成 `12×3=36` 行），目的是让 “总用户数” 的信息能出现在每一行中；==
    2. 窗口函数计算：
       - `COUNT(DISTINCT r.user_id) OVER(PARTITION BY r.contest_id)`：按赛事分组，统计每个赛事的**去重注册用户数**；
       - `COUNT(DISTINCT u.user_id) OVER()`：全局统计，得到**总用户数**；
    3. **`DISTINCT` 去重**：由于交叉连接后每个赛事会重复出现多行，用 `DISTINCT` 保留每个赛事的唯一结果。

    ### 二、为什么左外连接（LEFT JOIN）不行？

    你之前的写法是 `Register r LEFT JOIN Users u ON r.user_id = u.user_id`，这种左连接无法满足需求，核心原因有两个：

    #### 1. 左连接的结果集 “缺少全局用户信息”

    左连接的逻辑是：**保留左表（Register）的所有行，右表（Users）匹配不到则为 NULL**。

    以示例数据为例，左连接后的结果集只有 `Register` 表的 12 行（仅包含注册过赛事的用户），**完全没有未注册该赛事的用户信息**。

    当你按 `r.contest_id` 分组时，每个组里只有 “该赛事的注册用户”，根本无法通过 `COUNT()` 得到 “所有用户总数”—— 因为总用户数的信息根本没在结果集里。

    #### 2. 即使语法修复，逻辑也不对

    假设你把 `COUNT(u.*)` 改成合法的 `COUNT(u.user_id)`，结果也只是 “该赛事中同时存在于 Users 表的注册用户数”（由于注册逻辑保证用户一定存在，这其实就是 `COUNT(r.user_id)`），但总用户数还是拿不到。

    简单说：左连接只能 “补充用户信息”，不能 “把所有用户的全局信息带到每个赛事分组里”，而这正是计算 “注册率” 必须的。

* over()函数是什么？用法又是什么？

  * ## 1. 一句话解释

    `OVER()` = **开窗函数**

    作用：**在不把多行合并成一行的前提下，计算统计值（总数、平均值、排名等）**

    对比你最熟悉的：

    - `GROUP BY`：**合并行**，必须分组，行数变少
    - `OVER()`：**不合并行**，直接在每一行后面附上计算结果，行数不变

    ------

    ## 2. 最核心用法（你这道题要用的）

    ### 用法 1：`OVER()` 空括号 = 全局统计（整张表算一个总数）

    ```sql
    COUNT(user_id) OVER()
    ```

    意思：**计算整张表的总用户数，把结果贴到每一行上**

    示例：

    | contest_id | user_id | 总用户数 (OVER ()) |
    | :--------: | :-----: | :----------------: |
    |    208     |    6    |         3          |
    |    208     |    2    |         3          |
    |    208     |    7    |         3          |

    每一行都能拿到**总用户数**，这就是你题目需要的！

    ------

    ### 用法 2：`OVER(PARTITION BY 列)` = 分组统计（类似 group by，但不合并行）

    ```sql
    COUNT(user_id) OVER(PARTITION BY contest_id)
    ```

    意思：**按 contest_id 分组，计算每个赛事的注册人数**

    示例：

    | contest_id | user_id | 每个赛事注册数 |
    | :--------: | :-----: | :------------: |
    |    208     |    6    |       3        |
    |    208     |    2    |       3        |
    |    207     |    2    |       1        |

    ------

    ## 3. 为什么你的题目必须用 OVER ()？

    因为你需要**同时拿到两个数**：

    1. 每个赛事的注册人数
    2. 全表总用户数

    `OVER()` 可以**一行代码同时算出来**，不用子查询！

    ------

    ## 4. 你这道题的完美版（不用子查询、纯窗口函数）

    ```sql
    SELECT DISTINCT
      contest_id,
      ROUND(
        COUNT(user_id) OVER(PARTITION BY contest_id) * 100.0 
        / COUNT(DISTINCT user_id) OVER(),
      2) AS percentage
    FROM Register
    ORDER BY percentage DESC, contest_id ASC;
    ```

    这是**最兼容所有 MySQL 版本**的写法，逻辑最简单，绝对不报错：

    ```sql
    SELECT
        r.contest_id,
        ROUND(
            COUNT(DISTINCT r.user_id) * 100.0 / u.total_users,
            2
        ) AS percentage
    FROM Register r
    -- 只关联一次总用户数（CROSS JOIN 无ON条件）
    CROSS JOIN (
        SELECT COUNT(user_id) AS total_users
        FROM Users
    ) u
    GROUP BY r.contest_id, u.total_users
    ORDER BY percentage DESC, contest_id ASC;
    ```

    ### 拆解公式：

    ```
    COUNT(user_id) OVER(PARTITION BY contest_id)
    → 每个赛事注册人数
    
    COUNT(DISTINCT user_id) OVER()
    → 全平台总用户数
    ```

    ------

    ## 5. 超简单总结（背会这两句就行）

    1. **`OVER()` = 全局统计**（总数、平均值…）
    2. **`OVER(PARTITION BY 列)` = 分组统计**
    3. **不合并行，不改变原表行数**
    4. 专门解决：**既要明细行，又要统计值** 的场景

*****

### 性能分析

* # 这道题的 **3 种解法**（和上题结构完全一样）

  ## 解法 1：GROUP BY + 子查询（✅ 最优、最高效）

  ```sql
  SELECT
      contest_id,
      ROUND(COUNT(user_id) * 100.0 / (SELECT COUNT(*) FROM Users), 2) AS percentage
  FROM Register
  GROUP BY contest_id
  ORDER BY percentage DESC, contest_id ASC;
  ```

  ### 为什么最优？

  - **只扫描两次表**：一次 Register，一次 Users
  - **一次分组**，计算最快
  - **最简洁、最不容易错**
  - **数据库最喜欢这种写法**

  ------

  ## 解法 2：GROUP BY + CROSS JOIN（不用子查询，也高效）

  ```sql
  SELECT
      r.contest_id,
      ROUND(COUNT(r.user_id) * 100.0 / u.total, 2) AS percentage
  FROM Register r
  CROSS JOIN (SELECT COUNT(*) AS total FROM Users) u
  GROUP BY r.contest_id
  ORDER BY percentage DESC, contest_id ASC;
  ```

  **性能和解法 1 几乎一样**。

  ------

  ## 解法 3：窗口函数（可以用，但**效率最差**）

  ```sql
  SELECT DISTINCT
      contest_id,
      ROUND(
          COUNT(user_id) OVER(PARTITION BY contest_id) * 100.0
          / COUNT(DISTINCT user_id) OVER(),
      2) AS percentage
  FROM Register
  ORDER BY percentage DESC, contest_id ASC;
  ```

  ### 缺点：

  - 要计算多个窗口
  - 最后还要 DISTINCT 去重
  - **数据量大时明显更慢**
  - **低版本 MySQL 还不支持**

  ------

  # 四、最重要结论：哪种方法 **SQL 优化层面最高效？**

  ## **第一名：GROUP BY + 子查询（最优）**

  ## **第二名：CROSS JOIN（同样优秀）**

  ## **第三名：窗口函数（最差，不推荐）**





*****

## 查询结果的质量和占比

### 题目描述

### 错答如何更正？

```sql
-- ❌️错答❌️
select 
query_name,
 avg(rating / position) as quality,
 (select 
 round(count(rating)/(count(position)) * 100, 2) 
 from Queries 
 group by query_name 
 having rating < 3
 ) as poor_query_percentage
from Queries
```

![image-20260409153027964](E:\系统默认\桌面\Plan\求职\实践\leetcode\MySQL\picture\image-20260409153027964.png)

*****

### 正确答案：

----普通分组统计版

```sql
SELECT
    query_name,
    ROUND(AVG(rating / position), 2) AS quality,
    ROUND(SUM(rating < 3) / COUNT(*) * 100, 2) AS poor_query_percentage
FROM Queries
GROUP BY query_name;
```

-----窗口函数

```sql
SELECT DISTINCT
    query_name,
    -- 按查询名分组，计算 quality（平均值）
    ROUND(AVG(rating / position) OVER (PARTITION BY query_name), 2) AS quality,
    -- 按查询名分组，计算劣质率
    ROUND(
        SUM(CASE WHEN rating < 3 THEN 1 ELSE 0 END) 
        OVER (PARTITION BY query_name) 
        / COUNT(*) OVER (PARTITION BY query_name) * 100,
        2
    ) AS poor_query_percentage
FROM Queries;
```

-----子查询

```sql
SELECT
    query_name,
    ROUND(quality,2) quality,
    ROUND(poor/Total*100,2) poor_query_percentage
FROM (
    SELECT
        query_name,
        AVG(rating/position) quality,
        SUM(rating<3) poor,
        COUNT(*) Total
    FROM Queries
    GROUP BY query_name
) t;
```

*****

#### 性能分析

* # 二、最重要的问题：**哪种效率最高？**

  ## ✅ **第一名：GROUP BY 分组查询（最优）**

  ## ✅ **第二名：窗口函数 + DISTINCT（中等）**

  ## ❌ **第三名：子查询（最差）**

  ------

  # 三、为什么 GROUP BY 最高效？（核心原理）

  ## 1. GROUP BY 只做 **1 次扫描 + 1 次分组计算**

  数据库做的事：

  - 读表 → 按 query_name 分组 → 一次性算出 avg、sum、count
  - **内存占用最小、计算次数最少**

  ## 2. 窗口函数要做 **多次计算 + 最后去重**

  窗口函数：

  - 每行都要计算 3 个窗口函数（avg、sum、count）
  - 最后还要用 DISTINCT 对全表去重
  - **计算量比 GROUP BY 多很多**

  ## 3. 子查询多一层嵌套，多一次临时表，更慢

  ------

  # 四、终极结论（你一定要记住）

  ### **在分组统计场景下：GROUP BY 永远比窗口函数更快、更高效！**

  ### 适用场景口诀：

  - **要统计结果（每组一行）→ 用 GROUP BY（最快）**
  - **要保留原表所有行 + 附加统计 → 用窗口函数**

*****

### Q&A

* SUM()能换成COUNT()嘛？

  * # 答案：**可以！完全可以用 COUNT 代替 SUM**

    我给你讲**最清晰、最安全、最通用**的写法，让你彻底搞懂！

    ------

    ## 原来的写法（用 SUM）

    ```sql
    SUM(rating < 3)
    ```

    因为 MySQL 里：

    - `rating < 3` 成立 → **1**

    - 不成立 → 0

      所以 SUM 就是把所有 1 加起来 = 总数。

    ------

    ## 改成 COUNT 的正确写法

    ### 方法 1（最通用、所有数据库都支持 ✅）

    ```sql
    COUNT(CASE WHEN rating < 3 THEN 1 END)
    ```

    ### 方法 2（MySQL 专属写法 ✅）

    ```sql
    COUNT(rating < 3 OR NULL)
    ```

    这两种**都能完美替代 `SUM(rating <3)`**

    ------

    ## 为什么不能直接写 `COUNT(rating < 3)`？

    因为：

    - `COUNT(值)` 只**统计非 NULL 的行数**

    - `rating <3` 不成立时会返回 **0**

    - 0 不是 NULL

      ，会被 COUNT 算进去

      

      → 结果变成 

      全部都计数

      ，就错了！

    所以必须用：

    ```sql
    COUNT(CASE WHEN rating <3 THEN 1 END)
    ```

    不满足条件时返回 **NULL**，COUNT 就不会统计，结果正确。

    ------

    ## 完整正确 SQL（COUNT 版）

    ```sql
    SELECT
        query_name,
        ROUND(AVG(rating / position), 2) AS quality,
        ROUND(
            COUNT(CASE WHEN rating < 3 THEN 1 END) 
            / COUNT(*) * 100, 
            2
        ) AS poor_query_percentage
    FROM Queries
    GROUP BY query_name;
    ```

    ------

    ## 超级总结

    - **SUM (条件)** → 简单、快
    - **COUNT (CASE WHEN 条件 THEN 1 END)** → 通用、标准、所有数据库都支持
    - **千万不要直接 COUNT (条件)** → 会错！

*****

## 每月交易

### 题目描述

表：`Transactions`

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| country       | varchar |
| state         | enum    |
| amount        | int     |
| trans_date    | date    |
+---------------+---------+
id 是这个表的主键。
该表包含有关传入事务的信息。
state 列类型为 ["approved", "declined"] 之一。
```

编写一个 sql 查询来查找每个月和每个国家/地区的事务数及其总金额、已批准的事务数及其总金额。

以 **任意顺序** 返回结果表。

查询结果格式如下所示。

**示例 1:**

```
输入：
Transactions table:
+------+---------+----------+--------+------------+
| id   | country | state    | amount | trans_date |
+------+---------+----------+--------+------------+
| 121  | US      | approved | 1000   | 2018-12-18 |
| 122  | US      | declined | 2000   | 2018-12-19 |
| 123  | US      | approved | 2000   | 2019-01-01 |
| 124  | DE      | approved | 2000   | 2019-01-07 |
+------+---------+----------+--------+------------+
输出：
+----------+---------+-------------+----------------+--------------------+-----------------------+
| month    | country | trans_count | approved_count | trans_total_amount | approved_total_amount |
+----------+---------+-------------+----------------+--------------------+-----------------------+
| 2018-12  | US      | 2           | 1              | 3000               | 1000                  |
| 2019-01  | US      | 1           | 1              | 2000               | 2000                  |
| 2019-01  | DE      | 1           | 1              | 2000               | 2000                  |
+----------+---------+-------------+----------------+--------------------+-----------------------+
```

### 我的解答【通过】

```sql
select 
DATE_FORMAT(trans_date, '%Y-%m') as month,
country,
count(id) trans_count,
sum(state="approved") as approved_count,
sum(amount) as trans_total_amount,
sum(case when state="approved" then amount else 0 end) as approved_total_amount
from Transactions
group by country,month;
```

### Q&A

* 如何==**提取date数据的年月日**==

  * 我给你**最简单、最实用、最常考**的提取年月方法，**直接背这 3 个函数就够了**！

    # 一、提取 **年份**

    ```sql
    YEAR(date)   → 得到 2025
    ```

    # 二、提取 **月份**

    ```sql
    MONTH(date)  → 得到 3
    ```

    # 三、提取 **年月组合（最常用！）**

    ```sql
    DATE_FORMAT(date, '%Y-%m')   → 得到 2025-03
    ```

    
