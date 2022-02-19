# SQL-Queries

Test SQL queries are run in Python using pandas data frames and the ```pandasql``` library.

The SQL queries can be found in the script "sql_queries.py". Join, aggregation and complex nested queries are shown.

Some SQL functions are described below. 

## SQL Guide

### Numeric Functions

| Function | Description |
| --- | --- |
| `AVG` | Returns the average value of an expression |
| `COUNT` | Returns the number of records returned by a SELECT query |
| `FLOOR` | Returns the largest integer value that is <= to a number |
| `LOG` | Returns the natural logarithm of a number |
| `LOG10` |	Returns the natural logarithm of a number to base 10 |
| `MAX` | Returns the maximum value in a set of values |
| `MIN` | Returns the minimum value in a set of values |
| `POWER` | Returns the value of a number raised to the power of another number |
| `ROUND` | Rounds a number to a specified number of decimal places |
| `SQRT` | Returns the square root of a number |
| `SQUARE` | Returns the square of a number |
| `SUM` | Calculates the sum of a set of values |

### String Functions

| Function | Description |
| --- | --- |
| `CONCAT(string1, string2, ...., string_n)` | Adds two or more strings together |
| `LEFT(string, number_of_chars)` | Extracts a number of characters from a string (starting from left) |
| `LEN` | Returns the length of a string |
| `LOWER` | Converts a string to lower-case |
| `LTRIM` | Removes leading spaces from a string |
| `REPLACE(string, old_string, new_string)` | Replaces all occurrences of a substring within a string, with a new substring |
| `REPLICATE(string, integer)` | Repeats a string a specified number of times |
| `REVERSE` | Reverses a string and returns the result |
| `RIGHT(string, number_of_chars)` | Extracts a number of characters from a string (starting from right) |
| `RTRIM` | Removes trailing spaces from a string |
| `STR` | Returns a number as a string |
| `SUBSTRING(string, start, length)` | Extracts some characters from a string |
| `TRIM` | Removes leading and trailing spaces from a string |
| `UPPER` | Converts a string to upper-case |

### Date Functions

| Function | Description |
| --- | --- |
| `DATEADD(interval, number, date)` | Adds a time/date interval to a date and then returns the date |
| `DATEDIFF(interval, date1, date2)` | Returns the difference between two dates |
| `DATEFROMPARTS(year, month, day)` | Returns a date from the specified parts (year, month, and day values) |
| `DATENAME(interval, date)` | Returns a specified part of a date (as string). The interval part represents a data string such as "yy" for year or "mm" for month. |
| `DATEPART(interval, date)` | Returns a specified part of a date (as integer). The interval part represents a data string such as "yy" for year or "mm" for month. |
| `DAY` | Returns the day of the month for a specified date |
| `GETDATE()` | Returns the current database system date and time |
| `ISDATE` | Checks an expression and returns 1 if it is a valid date, otherwise 0 |
| `MONTH` | Returns the month part for a specified date (a number from 1 to 12) |
| `YEAR` | Returns the year part for a specified date |

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

### Display data columns

```
## consumption table
  MeterID       Date  Hour     Usage
0    E101 2021-01-01     0  0.623588
1    E101 2021-01-01     1  0.412385
2    E101 2021-01-01     2  0.502635
3    E101 2021-01-01     3  0.411973
4    E101 2021-01-01     4  0.272102

## metermaster table
  MeterID  Eircode       City ServingUtility
0    E101  X35JU99  Dungarvan    Electricity
1    E201  YH9YA32  Waterford    Electricity
2    E301  Z11HJ34  Waterford    Electricity
3    E401  X72GW76  Dungarvan    Electricity

## accounts table
  MeterID AccountNumber CustomerID BillID  Rate ContractStart ContractEnd
0    E101           A01        C01   B001    20     1 01 2021         NaN
1    E201           A02        C02   B002    19     1 06 2015         NaN
2    E301           A03        C03   B003    28    13 01 2019   1 12 2020
3    E401           A04        C04   B004    26     1 01 2020         NaN

## customers table
  CustomerID FirstName Surname        Address       Town
0        C01      Mike   Kelly   123 Oak Road  Dungarvan
1        C02    Sandra  Murphy   34 Pine Wood  Waterford
2        C03   Francis   Burke  20 Town Court  Waterford
3        C04    Martin   Kelly  1 The Meadows  Dungarvan
```

### QUERY1: Find the average electricity usage for meters in the town of Dungarvan

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

#### QUERY1 Output

```
  MeterID  MeterUsage (kWh)
0    E101          0.496900
1    E401          0.500057
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

### QUERY: Find the second highest cumulative value

```python
second_highest_query = '''
SELECT c.MeterID AS MeterID, SUM(c.Usage) AS SecondHighest
FROM consumption AS c
GROUP BY c.MeterID
ORDER BY SUM(c.Usage) DESC
LIMIT 1 OFFSET 1
'''

print(mysql(second_highest_query))
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