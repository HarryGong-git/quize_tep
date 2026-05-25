# SQL 编写代码题答题步骤

本文件针对 sample question 风格：给 table structure，让你写 `CREATE TABLE` 或 `SELECT` 查询。

## 一、通用答题框架

拿到 SQL 题先做 6 件事：

1. 圈出输出列：题目要求 display/show/list 什么。
2. 圈出主表：题目核心对象是什么，例如 transactions、customers、orders。
3. 圈出过滤条件：时间、支付方式、金额、状态、类别等。
4. 判断是否需要 join：输出列或过滤列是否来自不同表。
5. 判断是否需要 aggregation：题目是否出现 number of、total、average、for each、by category。
6. 判断是否需要 ranking/top N：题目是否出现 top five、most recent three、highest、latest。

然后按下面 SQL 顺序写：

```sql
SELECT ...
FROM ...
JOIN ... ON ...
WHERE ...
GROUP BY ...
HAVING ...
ORDER BY ...
LIMIT ...;
```

注意：这是书写顺序，不是逻辑执行顺序。逻辑上通常是 `FROM/JOIN` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY` → `LIMIT`。

## 二、CREATE TABLE 题步骤

题型示例：Write CREATE statement to create customer table: customer id, name, type of id document, id number, date of birth, annual income, occupation.

### 步骤

1. 选表名，例如 `Customer`。
2. 把题目中的每个字段变成 column。
3. 为每个 column 选 data type。
4. 找 primary key。
5. 添加 `NOT NULL`。
6. 添加 `UNIQUE`。
7. 添加 `CHECK` 约束，例如证件类型只能是 NRIC 或 Passport。
8. 如果题目给了引用关系，再添加 foreign key。

### 推荐答案模板

```sql
CREATE TABLE Customer (
  CustomerID VARCHAR(50) NOT NULL,
  Name VARCHAR(100) NOT NULL,
  IDDocumentType VARCHAR(20) NOT NULL,
  IDNumber VARCHAR(50) NOT NULL,
  DateOfBirth DATE,
  AnnualIncome DECIMAL(12,2),
  Occupation VARCHAR(100),
  CONSTRAINT PK_Customer PRIMARY KEY (CustomerID),
  CONSTRAINT UQ_Customer_IDNumber UNIQUE (IDNumber),
  CONSTRAINT CK_Customer_IDDocumentType
    CHECK (IDDocumentType IN ('NRIC', 'Passport'))
);
```

### 易错点

- 金额或收入用 `DECIMAL(12,2)`，不要用 `FLOAT`。
- `Name cannot be empty` 对应 `NOT NULL`。
- `id number has to be unique` 对应 `UNIQUE`。
- 固定取值用 `CHECK`。
- 如果数据库版本不严格执行 `CHECK`，考试写出来仍然是正确设计思路。

## 三、基础 SELECT / Top N 题步骤

题型示例：Find the top five “Cash” transactions based on transaction amount. Display only transaction date and time, merchant name, and amount.

### 判断

- 输出列：`TransDatetime`, `MerchantName`, `TransactionAmount`。
- 主表：`Transaction`。
- 过滤：`PaymentMethod = 'Cash'`。
- 排序：金额 higher better → `ORDER BY TransactionAmount DESC`。
- Top five → `LIMIT 5`。

### 答案模板

```sql
SELECT
  TransDatetime,
  MerchantName,
  TransactionAmount
FROM Transaction
WHERE PaymentMethod = 'Cash'
ORDER BY TransactionAmount DESC
LIMIT 5;
```

### 如果表名是保留字

`Transaction` 在一些数据库中可能是关键字。MySQL 可写：

```sql
SELECT
  TransDatetime,
  MerchantName,
  TransactionAmount
FROM `Transaction`
WHERE PaymentMethod = 'Cash'
ORDER BY TransactionAmount DESC
LIMIT 5;
```

## 四、JOIN + 日期过滤 + GROUP BY 聚合题步骤

题型示例：Find the number of transactions for each merchant category code in the period from 2019 July 1 to 2019 Sep 30. Display merchant category name, number of transactions, and total amount.

### 判断

- 输出列：merchant category name、number of transactions、total amount。
- 主表：`Transaction`。
- 需要 category name，来自 `MerchantCategory`。
- Join key：`MerchantCategoryCode`。
- 日期范围：2019-07-01 到 2019-09-30。
- `for each merchant category` → `GROUP BY`。
- number of transactions → `COUNT(*)`。
- total amount → `SUM(TransactionAmount)`。

### 日期范围写法

如果 `TransDatetime` 是 datetime，推荐半开区间：

```sql
WHERE TransDatetime >= '2019-07-01'
  AND TransDatetime < '2019-10-01'
```

这样不会漏掉 2019-09-30 当天 23:59:59 的交易。

### 答案模板

```sql
SELECT
  mc.MerchantCategoryName,
  COUNT(*) AS NumTransactions,
  SUM(t.TransactionAmount) AS TotalAmount
FROM `Transaction` t
JOIN MerchantCategory mc
  ON t.MerchantCategoryCode = mc.MerchantCategoryCode
WHERE t.TransDatetime >= '2019-07-01'
  AND t.TransDatetime < '2019-10-01'
GROUP BY
  mc.MerchantCategoryCode,
  mc.MerchantCategoryName
ORDER BY
  mc.MerchantCategoryName;
```

### 易错点

- 输出 `MerchantCategoryName`，所以必须 join mapping table。
- 不要只 `GROUP BY MerchantCategoryName`，更稳的是 code + name 一起 group。
- 日期是 datetime 时，不建议写 `BETWEEN '2019-07-01' AND '2019-09-30'`，因为这通常只到 2019-09-30 00:00:00。

## 五、“每个客户最近三笔交易”题步骤

题型示例：For each customer, find their most recent three transactions. Display customer identifier, first name, last name, join date, and these three transactions’ details.

### 判断

- 每个 customer → 需要按 customer 分组/分区。
- 最近三笔 → 每组 top 3，不是全表 top 3。
- 输出客户信息 + 交易详情 → join Customer 和 Transaction。
- 排序依据：`TransDatetime DESC`。
- 最清晰写法：window function `ROW_NUMBER()`。

### MySQL 8+ 推荐答案

```sql
WITH ranked_transactions AS (
  SELECT
    t.*,
    ROW_NUMBER() OVER (
      PARTITION BY t.CustomerID
      ORDER BY t.TransDatetime DESC, t.Identifier DESC
    ) AS rn
  FROM `Transaction` t
)
SELECT
  c.Identifier AS CustomerIdentifier,
  c.FirstName,
  c.LastName,
  c.JoinDate,
  rt.Identifier AS TransactionIdentifier,
  rt.TransDatetime,
  rt.MerchantName,
  rt.MerchantCategoryCode,
  rt.TransactionAmount,
  rt.PaymentMethod
FROM Customer c
JOIN ranked_transactions rt
  ON c.Identifier = rt.CustomerID
WHERE rt.rn <= 3
ORDER BY
  c.Identifier,
  rt.TransDatetime DESC,
  rt.Identifier DESC;
```

### 为什么要加 `t.Identifier DESC`

如果同一客户两笔交易时间完全一样，`ORDER BY TransDatetime DESC` 可能无法稳定排序。加交易 ID 作为 tie-breaker，答案更严谨。

### 如果考试环境不支持 window function

可以用 correlated subquery 思路：统计同一客户中比当前交易更新的交易数，小于 3 就保留。

```sql
SELECT
  c.Identifier AS CustomerIdentifier,
  c.FirstName,
  c.LastName,
  c.JoinDate,
  t.Identifier AS TransactionIdentifier,
  t.TransDatetime,
  t.MerchantName,
  t.MerchantCategoryCode,
  t.TransactionAmount,
  t.PaymentMethod
FROM Customer c
JOIN `Transaction` t
  ON c.Identifier = t.CustomerID
WHERE (
  SELECT COUNT(*)
  FROM `Transaction` t2
  WHERE t2.CustomerID = t.CustomerID
    AND (
      t2.TransDatetime > t.TransDatetime
      OR (
        t2.TransDatetime = t.TransDatetime
        AND t2.Identifier > t.Identifier
      )
    )
) < 3
ORDER BY
  c.Identifier,
  t.TransDatetime DESC,
  t.Identifier DESC;
```

考试中如果老师没有讲 window function，可以写 CTE + `ROW_NUMBER()` 并在旁边解释“rank transactions within each customer”；如果担心不被接受，再补 correlated subquery。

## 六、聚合题万能模板

当题目出现这些词：

- number of
- count
- total
- sum
- average
- for each
- by category / by customer / by month
- group

基本就是聚合题。

### 模板

```sql
SELECT
  group_col_1,
  group_col_2,
  COUNT(*) AS row_count,
  SUM(amount_col) AS total_amount,
  AVG(amount_col) AS avg_amount
FROM main_table mt
JOIN lookup_table lt
  ON mt.lookup_id = lt.lookup_id
WHERE row_level_condition
GROUP BY
  group_col_1,
  group_col_2
HAVING aggregate_condition
ORDER BY
  total_amount DESC;
```

### 判断 WHERE 还是 HAVING

用这个规则：

- 条件针对原始行：`WHERE`。
- 条件针对聚合结果：`HAVING`。

例子：

```sql
-- 只统计 2019 年交易：WHERE
WHERE TransDatetime >= '2019-01-01'
  AND TransDatetime < '2020-01-01'

-- 只显示总金额超过 10000 的类别：HAVING
HAVING SUM(TransactionAmount) > 10000
```

## 七、JOIN 题万能模板

当题目输出列来自多个表，或需要 code 转 name，通常需要 join。

```sql
SELECT
  a.col1,
  b.col2
FROM table_a a
JOIN table_b b
  ON a.b_id = b.id
WHERE ...
```

### 选 JOIN 类型

- 只要匹配记录：`INNER JOIN`。
- 即使没有交易/没有匹配也要保留左表对象：`LEFT JOIN`。
- 要找没有匹配的记录：`LEFT JOIN ... WHERE right_table.key IS NULL`。

例子：找没有信用卡的存款客户。

```sql
SELECT d.*
FROM deposit d
LEFT JOIN creditcard c
  ON d.customer_id = c.customer_id
WHERE c.customer_id IS NULL;
```

## 八、Subquery / CTE 题步骤

当题目需要“和整体平均值比较”“先算每组数量，再跟平均数量比较”“复杂中间结果”时，用 subquery 或 CTE。

### Subquery 模板

```sql
SELECT name, population
FROM country
WHERE population > (
  SELECT AVG(population)
  FROM country
);
```

### CTE 模板

```sql
WITH group_summary AS (
  SELECT
    group_col,
    COUNT(*) AS cnt
  FROM table_name
  GROUP BY group_col
),
avg_summary AS (
  SELECT AVG(cnt) AS avg_cnt
  FROM group_summary
)
SELECT gs.*
FROM group_summary gs, avg_summary a
WHERE gs.cnt > a.avg_cnt;
```

### 答题选择

- 简单单值比较：subquery。
- 多步报表、需要复用中间结果：CTE。

## 九、日期题固定写法

### 某一天

```sql
WHERE TransDatetime >= '2019-07-01'
  AND TransDatetime < '2019-07-02'
```

### 某个月

```sql
WHERE TransDatetime >= '2019-07-01'
  AND TransDatetime < '2019-08-01'
```

### 某季度

```sql
WHERE TransDatetime >= '2019-07-01'
  AND TransDatetime < '2019-10-01'
```

### 计算年龄

```sql
SELECT
  Name,
  DateOfBirth,
  TIMESTAMPDIFF(YEAR, DateOfBirth, CURDATE()) AS Age
FROM Customer;
```

## 十、考试时 SQL 代码检查清单

交卷前检查：

- `SELECT` 只显示题目要求的列。
- 每个表都有 alias，列名前缀清楚。
- Join condition 是否完整，是否漏了 `ON`。
- 日期范围是否覆盖完整日期。
- 金额排序 top N 是否 `DESC`。
- `LIMIT` 是否放在最后。
- 需要 category name 时是否 join mapping table。
- 聚合列是否用了 `COUNT/SUM/AVG`。
- 非聚合输出列是否都在 `GROUP BY`。
- aggregate 过滤是否用了 `HAVING`。
- 每组 top N 是否用了 `PARTITION BY`，而不是全表 `LIMIT`。
- 表名如果是 `Transaction`，是否需要用反引号。

