# Sample Questions 参考答案

## Q1. What is Primary Key and what is Foreign Key?

Primary key 是表中用于唯一标识每一行记录的列或列组合。它必须 unique，并且不能为 null，用来保证 entity integrity。

Foreign key 是一个表中的列或列组合，用来引用另一个表的 primary key 或 unique key。它用来表达表之间的关系，并保证 referential integrity。

简短对比：

- Primary key 标识本表记录。
- Foreign key 引用其他表记录。
- Primary key 通常唯一且非空。
- Foreign key 可以重复，是否允许 null 取决于业务规则。

## Q2. Is the statement correct? “Data warehouse has less data than operational database because it only contains summarized data.”

This statement is not necessarily correct.

Data warehouse does not only contain summarized data. It can contain detailed historical data, integrated data from multiple operational systems, cleaned data, reconciled data, and aggregate tables. A data warehouse may even contain more data than a single operational database because it stores long-term history and data from multiple sources.

A better statement is: a data warehouse may contain summarized data for performance, but it often also stores detailed historical data for analysis.

## Q3. What is ETL? What is the data staging area in ETL? Why is data staging area needed?

ETL means Extract, Transform, Load.

- Extract: collect relevant data from source systems.
- Transform: clean, convert, integrate, deduplicate, generate keys, and aggregate data.
- Load: load the transformed data into the data warehouse.

Data staging area is a temporary storage area used during ETL. Extracted data is stored there before being loaded into the data warehouse. Transformations and cleansing are often performed in the staging area.

Data staging area is needed because ETL usually handles large volumes of data and complex transformations. It makes the process easier to restart, audit, debug, and monitor. It also helps preserve lineage and prevents complex transformation workloads from directly affecting source systems or final warehouse tables.

## Q4. CREATE TABLE for customer

题目字段：

- customer id
- name
- type of id document
- id number
- date of birth
- annual income
- occupation

参考答案：

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

说明：

- `CustomerID` 是 primary key。
- `Name` 不应为空，所以写 `NOT NULL`。
- `IDNumber` 应唯一，所以写 `UNIQUE`。
- `IDDocumentType` 只能是 NRIC 或 Passport，所以写 `CHECK`。
- `AnnualIncome` 是金额/收入，用 `DECIMAL` 比 `FLOAT` 更合适。

## Q5A. Top five Cash transactions by amount

题目：Find the top five “Cash” transactions based on transaction amount. Display only transaction date and time, merchant name, and amount.

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

答题逻辑：

- Cash transactions → `WHERE PaymentMethod = 'Cash'`。
- Higher amount is better → `ORDER BY TransactionAmount DESC`。
- Top five → `LIMIT 5`。
- Display only three columns → `SELECT` 只放这三列。

## Q5B. Transactions by merchant category in 2019 Q3

题目：Find the number of transactions for each merchant category code in the period from 2019 July 1 to 2019 Sep 30. Display merchant category name, number of transactions, and total amount.

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

答题逻辑：

- Merchant category name 来自 `MerchantCategory`，所以要 join。
- 交易数量用 `COUNT(*)`。
- 总金额用 `SUM(TransactionAmount)`。
- for each merchant category → `GROUP BY`。
- `TransDatetime` 是 datetime，所以用半开区间覆盖完整 7 月 1 日到 9 月 30 日。

## Q5C. Most recent three transactions for each customer

题目：For each customer, find their most recent three transactions. Display customer identifier, first name, last name, when he/she became customer, and these three transactions’ details.

MySQL 8+ 参考答案：

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

答题逻辑：

- “For each customer” 表示每个客户内部排序，不是全表排序。
- “Most recent three” 表示按 `TransDatetime DESC` 排名前 3。
- 用 `ROW_NUMBER() OVER (PARTITION BY CustomerID ORDER BY TransDatetime DESC)` 给每个客户的交易编号。
- 外层查询保留 `rn <= 3`。
- Join Customer 是因为输出需要 first name、last name、join date。

如果不能使用 window function，可用 correlated subquery：

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
