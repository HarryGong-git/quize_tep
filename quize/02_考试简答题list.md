# 考试简答题 List

下面按“题目 + 答题要点”的方式整理。复习时建议先遮住答案，用 3-5 句话口述，再看要点补漏。

## Chapter 1: Database / OLTP / Relational Model / ERD / Normalization

### 1. What is data? What is information?

答题要点：

- Data 是关于事物和事件的 raw facts。
- Information 是经过转换、整理、汇总后，对 decision making 有价值的数据。
- Data 通常更细、更原始；information 通常更聚合、更有业务含义。

### 2. What is OLTP?

答题要点：

- OLTP = Online Transaction Processing。
- 用于支持日常业务交易，例如订单、付款、ATM 取款。
- 特征是大量短小快速的 insert/update/query。
- 数据库通常高度 normalized，以支持一致性和更新效率。

### 3. Why are transactions important in OLTP?

答题要点：

- Transaction 是一组作为一个 unit of work 执行的数据库操作。
- 要么全部成功并 `COMMIT`，要么失败并 `ROLLBACK`。
- 事务保证业务操作可靠，避免并发和故障导致数据丢失或不一致。

### 4. What is DBMS?

答题要点：

- DBMS 是支持数据采集、存储、维护、查询、格式化和传播的软件系统。
- 它为应用程序提供数据访问能力。
- 企业 DBMS 还提供 concurrency control、recovery、backup、安全控制等能力。

### 5. What is the relational model?

答题要点：

- Relational model 把数据库表示为一组 relations / tables。
- 表由 rows 和 columns 组成。
- 数据结构、integrity constraints 和 data manipulation operators 是关系模型的核心。
- SQL 查询结果也可以看成一张 table。

### 6. What is a primary key?

答题要点：

- Primary key 是唯一标识表中每一行的 column 或 column combination。
- Primary key 必须 unique 且 not null。
- 它支持 entity integrity，保证每个实体可被追踪和区分。

### 7. What is a foreign key?

答题要点：

- Foreign key 是一个表中的 column 或 column combination，用来引用另一个表的 primary key 或 unique key。
- 它表达表之间的关系。
- 它支持 referential integrity，保证引用的对象真实存在。

### 8. Compare primary key and foreign key.

答题要点：

- Primary key 标识本表记录；foreign key 引用其他表记录。
- Primary key 必须 unique 且 not null；foreign key 可以重复，是否允许 null 取决于业务规则。
- Primary key 保证 entity integrity；foreign key 保证 referential integrity。

### 9. What are the primary types of integrity constraints?

答题要点：

- Entity integrity: primary key unique and not null。
- Referential integrity: foreign key values must match referenced table。
- Domain integrity: column values must satisfy type/range/format/domain。
- User-defined integrity: custom business rules。

### 10. What is an ERD and why is it useful?

答题要点：

- ERD = Entity-Relationship Diagram。
- 它描述特定业务领域中的 entities、attributes 和 relationships。
- 用于设计数据库、理解表之间联系、帮助业务和技术沟通。

### 11. How do you convert an ERD to relational tables?

答题要点：

- 为每个 entity 建表。
- 为每张表确定 primary key 和 attributes。
- 选择合适 data types。
- 1:N 关系通常在 N 端添加 foreign key。
- M:N 关系通常用 junction table，包含两边 foreign keys。
- 添加 `NOT NULL`, `UNIQUE`, `CHECK`, `FOREIGN KEY` 等 constraints。

### 12. What is normalization?

答题要点：

- Normalization 是组织 tables 和 attributes 的关系数据库建模过程。
- 目标是减少 data redundancy，提高 data integrity。
- 它通过把大表逐步拆成小表，使属性正确依赖 primary key。

### 13. Explain 1NF, 2NF, and 3NF.

答题要点：

- 1NF: 每个 data item atomic，每行唯一。
- 2NF: 没有 partial dependency，非 key 属性依赖整个 key。
- 3NF: 没有 transitive dependency，非 key 属性只依赖 key，不依赖其他非 key 属性。

### 14. Why is normalized design suitable for OLTP but not always good for analytics?

答题要点：

- OLTP 需要频繁 insert/update，normalized design 能减少冗余和更新异常。
- Analytics 查询通常跨很多业务维度，需要汇总大量历史数据。
- 高度 normalized 会导致分析时 join 很多表，查询慢且 SQL 复杂。
- 因此 DW/OLAP 更常用 denormalized dimensional model。

## Chapter 2: SQL

### 15. What are common SQL statement categories?

答题要点：

- Definitional / DDL: `CREATE TABLE`, `CREATE VIEW`。
- Manipulation / DML: `SELECT`, `INSERT`, `UPDATE`, `DELETE`。
- Transaction control: `COMMIT`, `ROLLBACK`。
- Access control: `GRANT`, `REVOKE`。

### 16. Why use DECIMAL instead of FLOAT for money?

答题要点：

- `FLOAT` 用二进制近似表示，会产生 rounding errors。
- `DECIMAL` 用精确十进制表示。
- 金额、会计、精确测量应使用 `DECIMAL(W,R)`。

### 17. What is the role of constraints in CREATE TABLE?

答题要点：

- Constraints 用来保证数据质量和完整性。
- `PRIMARY KEY` 保证唯一且非空。
- `FOREIGN KEY` 保证引用有效。
- `UNIQUE` 防止重复。
- `NOT NULL` 防止缺失值。
- `CHECK` 限制取值范围或枚举。

### 18. What is a JOIN?

答题要点：

- JOIN 用来基于相关列组合两个或多个表的行。
- 最常见 join condition 是 primary key = foreign key。
- JOIN 是关系数据库查询的核心，因为数据通常存储在多个相关表中。

### 19. Compare INNER JOIN and LEFT JOIN.

答题要点：

- `INNER JOIN` 只返回两边都匹配的行。
- `LEFT JOIN` 返回左表所有行；右表匹配不到时，右表列为 null。
- 如果题目要求“包括没有交易/没有匹配记录的客户”，通常用 `LEFT JOIN`。

### 20. What is Cartesian join and why is it dangerous?

答题要点：

- Cartesian join / cross join 没有 join condition。
- 它返回两个表所有行的组合。
- 结果数量可能爆炸，性能很差，通常是忘写 join condition 的错误。

### 21. What is SQL aggregation?

答题要点：

- Aggregation 是对一组值执行计算，返回 summary value。
- 常用于统计总金额、平均值、数量、最大最小值。
- 常见函数包括 `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`。

### 22. What is GROUP BY?

答题要点：

- `GROUP BY` 把具有相同 group key 的 rows 组织成 groups。
- 每个 group 输出一行 summary。
- `SELECT` 中非聚合列必须出现在 `GROUP BY` 中。

### 23. Compare WHERE and HAVING.

答题要点：

- `WHERE` 在分组前过滤 individual rows。
- `HAVING` 在分组后过滤 groups。
- 涉及 aggregate function 的过滤，例如 `SUM(amount) > 1000`，应放在 `HAVING`。

### 24. Difference between JOIN operation and SET operation.

答题要点：

- JOIN works on columns，用横向拼接方式组合表。
- SET operation works on rows，用纵向集合方式合并、求交集或差集。
- Set operators 要求两边 query 列数相同、对应列类型兼容。

### 25. Difference between UNION and UNION ALL.

答题要点：

- `UNION` 合并结果并去除重复行。
- `UNION ALL` 合并结果但保留重复行。
- `UNION ALL` 通常更快，但只有在需要保留重复时使用。

### 26. What is a subquery?

答题要点：

- Subquery 是嵌套在另一个 SQL query 中的 query。
- 可以出现在 `SELECT`, `FROM`, `WHERE`, `HAVING`。
- 用于计算中间结果，例如平均值、最大值、过滤集合。

### 27. What is a CTE and why is it useful?

答题要点：

- CTE = Common Table Expression，用 `WITH` 定义临时命名结果集。
- 它让复杂 SQL 更可读。
- 可以把多步逻辑拆成清晰阶段。
- 可在主 query 中复用。

## Chapter 3: Data Warehouse / OLAP / Dimensional Model

### 28. Why not build BI dashboard directly on OLTP databases?

答题要点：

- OLTP 要支持日常业务，复杂分析查询可能影响业务系统性能。
- OLTP 通常 normalized，分析查询需要 join 很多表。
- 分析需要大量历史数据，OLTP 保存全部历史会增加负担。
- 因此需要 data warehouse 把数据提前整合并优化查询。

### 29. What is a data warehouse?

答题要点：

- Data warehouse 是 diverse data 的 stored collection。
- 它是面向分析的 single repository。
- 它 subject-oriented、保存历史、non-volatile、更新不频繁。
- 它为 OLAP、BI、decision support 提供数据基础。

### 30. Is this statement correct: “Data warehouse has less data than operational database because it only contains summarized data.” Why?

答题要点：

- 不一定正确，通常是错误或过度简化。
- Data warehouse 不只保存 summarized data，也可以保存 detailed historical data。
- DW 往往保存多个源系统、长时间历史、清洗整合后的数据，数据量可能比单个 operational database 更大。
- DW 可能包含 summary/aggregate tables，但这不是它唯一的数据。

### 31. Compare OLTP and OLAP.

答题要点：

- OLTP 支持 daily operations；OLAP 支持 analysis and decision support。
- OLTP mostly updates；OLAP mostly reads。
- OLTP normalized；OLAP often denormalized。
- OLTP 查询短小简单；OLAP 查询长且复杂。
- OLTP 保存 current snapshot；OLAP 保存 full history。

### 32. What is a data mart?

答题要点：

- Data mart 是 data warehouse 的子集。
- 通常面向某个部门、业务线或团队。
- 优点是范围小、上线快；缺点是长期跨部门集成可能复杂。

### 33. What is dimensional modeling?

答题要点：

- Dimensional modeling 是围绕业务概念组织数据的技术。
- 它关注 measures and dimensions。
- 相比 ER model 描述 entities and relationships，dimensional model 更适合分析和报表。

### 34. What are measures and dimensions?

答题要点：

- Measures 是被分析的数值指标，例如 sales amount、quantity、number of rentals。
- Dimensions 是描述 measure 上下文的业务参数，例如 time、product、store、customer。
- 分析常见形式是 measure by dimensions。

### 35. What is a fact table?

答题要点：

- Fact table 保存业务过程的 measurements。
- 它包含 measures 和指向 dimension tables 的 foreign keys。
- Fact table 的 grain 决定每行代表什么业务细节。

### 36. What is a dimension table?

答题要点：

- Dimension table 保存业务描述性属性。
- 它用于筛选、分组、汇总和报表标签。
- 常见 dimensions 包括 date、customer、product、store、merchant category。

### 37. What is star schema?

答题要点：

- Star schema 是一个 fact table 位于中心，多个 dimension tables 围绕它。
- Dimension tables 通常 denormalized。
- 优点是直观、join 少、查询性能好、适合 OLAP。

### 38. What is snowflake schema?

答题要点：

- Snowflake schema 是把 star schema 的 dimension tables 进一步 normalized。
- 它减少冗余，可能更易维护。
- 但查询更复杂、join 更多、性能可能更差。
- 一般 DW 推荐 star schema，除非有明确维护或空间需求。

### 39. What is grain and why is it important?

答题要点：

- Grain 定义 fact table 每一行代表的详细程度。
- 例如“一张收据的一条 line item”或“每天每店每类别的租赁数量”。
- Grain 决定可用 measures、dimension keys 和查询粒度。
- 选择正确 grain 是 dimensional model 最重要步骤。

### 40. Why use surrogate keys in dimension tables?

答题要点：

- Surrogate key 是 DW 内部生成的 artificial key。
- 它比 source natural key 更稳定。
- 它能整合多个 source system 中不同 key。
- 它支持 dimension change 和历史追踪，尤其是 SCD Type 2。

### 41. What is a date dimension and why is it important?

答题要点：

- Date dimension 保存 date、day、month、quarter、year、holiday、fiscal period 等属性。
- 几乎所有 DW 都需要 date dimension，因为分析通常是 time series。
- 它可独立生成，不一定来自 OLTP source。

### 42. Why separate date dimension and time dimension?

答题要点：

- 如果把 time 到 second level 放入 date dimension，一年会产生 31,536,000 行。
- Date 和 time 的业务粒度和属性不同。
- Time dimension 应根据用户需求设计，例如 hour 或 hour range。

### 43. What is a “not applicable” row in a dimension table?

答题要点：

- 当 fact 的维度值未知或不适用时，用特殊维度行表示。
- 因为 fact table 的 foreign key 不应为 null。
- 例子包括 `Non Member Customer`, `Date unknown`, `Does not have insurance`。

### 44. What is a degenerate dimension?

答题要点：

- Degenerate dimension 是没有 attributes 的 dimension。
- 常见是 transaction number、invoice number、order number。
- 它通常直接放在 fact table 中，不单独建 dimension table。

### 45. What is a conformed dimension?

答题要点：

- Conformed dimension 是被多个 fact tables 共享的 dimension。
- 它保证跨业务过程分析时维度口径一致。
- 例如多个 fact tables 都使用同一个 `DimDate` 或 `DimCustomer`。

### 46. What is slowly changing dimension?

答题要点：

- SCD 是属性随时间缓慢变化的 dimension。
- Type 1 覆盖旧值，不保留历史。
- Type 2 新增一行，新 surrogate key，保留历史。
- Type 3 增加 previous value 列，保留有限历史。

## Chapter 4: ETL

### 47. What is ETL?

答题要点：

- ETL = Extract, Transform, Load。
- Extract 从 source systems 抽取数据。
- Transform 清洗、转换、整合、去重、生成 key、聚合。
- Load 把处理后的数据加载到 data warehouse。

### 48. What is the data staging area in ETL?

答题要点：

- Data staging area 是 ETL 过程中的中转存储区域。
- 它用于暂存抽取的数据，并执行清洗和转换。
- 通常不面向终端用户查询。

### 49. Why is data staging area needed?

答题要点：

- ETL 处理大数据量，需要分阶段执行。
- Staging area 让流程更容易重启、调试和审计。
- 可以保存中间结果、lineage 和质量检查结果。
- 它减少 source systems 和 DW 被复杂转换直接影响的风险。

### 50. What are common ETL design constraints?

答题要点：

- Business needs and KPIs。
- Compliance and security。
- Data quality。
- Data integration and conformed dimensions。
- Data latency。
- Archiving and lineage。
- BI delivery interface。
- Available skills and legacy licenses。

### 51. Explain Extract in ETL.

答题要点：

- Extract 是从 source systems 快速抽取 relevant data。
- 可用 SQL extract、DB unload tools 或 extract applications。
- 大型系统通常不每次全量抽取，而是抽取 delta。

### 52. Explain Transform in ETL.

答题要点：

- Transform 是把 source data 变成 DW 需要的格式和语义。
- 包括类型转换、编码转换、日期格式转换、清洗、去重、filter、join、aggregate。
- 还包括生成 surrogate keys 和维护 production key 到 DW key 的 mapping。

### 53. Explain Load in ETL.

答题要点：

- Load 是把转换后的数据加载进 DW。
- 要追求高效加载，避免大量 row-by-row SQL update。
- 可用 load tools，例如 MySQL `LOAD DATA`。
- 常先加载 dimensions，再加载 facts。

### 54. Compare initial load and incremental update.

答题要点：

- Initial load 是 DW 第一次建立时加载全部历史数据。
- 它数据量大，可能很慢，也可能历史数据难以修复。
- Incremental update 是之后周期性加载变化数据。
- Incremental update 数据量较小，但需要识别 delta。

### 55. Why must dimensions be loaded before facts?

答题要点：

- Fact table 包含指向 dimension tables 的 foreign keys。
- 新 fact 记录需要找到对应 dimension rows 和 surrogate keys。
- 如果 dimension 不存在，fact 的 referential integrity 会失败。

### 56. What is the main logic of building a fact table in ETL?

答题要点：

- 先定义 fact table grain。
- 从 source tables 抽取与 grain 对应的原始数据。
- Join dimension tables，把 source natural keys 转成 DW surrogate keys。
- 按 grain 聚合 measures。
- Load 到 fact table。

