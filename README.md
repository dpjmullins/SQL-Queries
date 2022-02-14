# SQL-Queries

Test SQL queries are run in Python using pandas data frames and the ```pandasql``` library.

The SQL queries can be found in the script "sql_queries.py". Join, aggregation and complex nested queries are shown.

Some SQL functions are described below. 

## SQL Guide

### JOIN Queries

Different Types of SQL JOINs
Here are the different types of the JOINs in SQL:

(INNER) JOIN: Returns records that have matching values in both tables

LEFT (OUTER) JOIN: Returns all records from the left table, and the matched records from the right table

RIGHT (OUTER) JOIN: Returns all records from the right table, and the matched records from the left table

FULL (OUTER) JOIN: Returns all records when there is a match in either left or right table

![inner_join](/SQL_Joins/sql_innerjoin.gif)
![left_join](/SQL_Joins/sql_leftjoin.gif)
![right_join](/SQL_Joins/sql_rightjoin.gif)
![full_outer_join](/SQL_Joins/sql_fullouterjoin.gif)

### Date and time with pandasql library in Python

Pandasql needs to use the python function ```strftime('%Y', date)``` to extract time or date strings from a date in a SQL query. 

### DROP TABLE and TRUNCATE TABLE

```DROP TABLE``` deletes a table in the database.

```TRUNCATE TABLE``` deletes the data inside a table, but not the table itself. 

## Example SQL queries use

### First create a lambda function for running the SQL queries

```python
mysql = lambda q: sqldf(q, globals())
```

### Import data using pandas

```python
consumption = pd.read_csv("./Mock dataset/Consumption.csv")
metermaster = pd.read_csv("./Mock dataset/MeterMaster.csv")
accounts = pd.read_csv("./Mock dataset/Accounts.csv")
customers = pd.read_csv("./Mock dataset/Customers.csv")
```

### QUERY: Find the average electricity usage for meters in the town of Dungarvan

```python
## Specify the query string
aggregate_query = '''
SELECT c.MeterID, AVG(c.Usage) AS 'MeterUsage (kWh)'
FROM consumption AS c
INNER JOIN metermaster AS m ON c.MeterID = m.MeterID
WHERE m.City = "Dungarvan"
GROUP BY c.MeterID;
'''

## Run the SQL query
print(mysql(aggregate_query))
```

### QUERY: Find the monthly average electricity usage by town

```python
aggregate_query2 = '''
SELECT strftime('%m', co.Date) AS Month, cu.Town AS Town, AVG(co.Usage) AS AverageUsage
FROM consumption AS co
INNER JOIN accounts AS a ON co.MeterID = a.MeterID
INNER JOIN customers as cu ON a.CustomerID = cu.CustomerID
GROUP BY Month, cu.Town
'''

print(mysql(aggregate_query2))
```

### QUERY: Find the name of the customer with the greatest electricity consumption in January

```python
highest_customer_query = '''
SELECT s1.FirstName, s1.Surname, MAX(s2.SummedUsage) AS Usage
FROM 
    (   
    SELECT co.MeterID AS MeterID, cu.FirstName AS FirstName, cu.Surname AS Surname
    FROM consumption AS co
    LEFT JOIN accounts AS a ON co.MeterID = a.MeterID 
    LEFT JOIN customers AS cu ON a.CustomerID = cu.CustomerID
    GROUP BY co.MeterID
    ) AS s1
INNER JOIN 
    (
    SELECT co.MeterID AS MeterID, SUM(co.Usage) AS SummedUsage
    FROM consumption AS co
    WHERE co.Date BETWEEN '2021/01/01' AND '2021/01/31'
    GROUP BY co.MeterID
    ) AS s2
ON s1.MeterID = s2.MeterID;
'''

print(mysql(highest_customer_query))
```