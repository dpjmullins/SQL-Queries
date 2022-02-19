"""
Code for practicing SQL queries in Python
"""

import pandas as pd
from pandasql import sqldf
from sqlalchemy import outerjoin

## Functions
mysql = lambda q: sqldf(q, globals())

## Import datasets
consumption = pd.read_csv("./Mock dataset/Consumption.csv")
metermaster = pd.read_csv("./Mock dataset/MeterMaster.csv")
accounts = pd.read_csv("./Mock dataset/Accounts.csv")
customers = pd.read_csv("./Mock dataset/Customers.csv")

consumption['Date'] = pd.to_datetime(consumption['Date']) ## convert Date column to datatime format

# print(consumption.head())
# print(metermaster.head())
# print(accounts.head())
# print(customers.head())

# Run queries

## SELECT queries

select_query = mysql("SELECT * from metermaster LIMIT 5;")
#print(select_query)

### Subset the consumption table for specific dates
select_query2 = '''
SELECT * 
FROM consumption
WHERE Date BETWEEN '10/01/2021' AND '13/01/2021'
'''

### Find the number of readings per meter per month

select_query3 = '''
SELECT c.MeterID AS MeterID, strftime('%m', c.Date) AS Month, COUNT(c.Usage) AS NumberOfReadings
FROM consumption AS c
GROUP BY Month, MeterID
'''

#print(mysql(select_query3))

## JOIN queries

### Add the metadata variables Eircode and City to the consumption table
inner_join = '''
SELECT c.MeterID, c.Date, c.Usage, m.Eircode, m.City
FROM consumption AS c
INNER JOIN metermaster AS m ON c.MeterID = m.MeterID;
'''

### Find the first names of and account IDs of customers residing in Dungarvan
inner_join2 = '''
SELECT c.FirstName, a.AccountNumber
FROM customers AS c
INNER JOIN accounts AS a ON c.CustomerID = a.CustomerID
WHERE c.Town = "Dungarvan"
'''

### Add the metadata variables Eircode and City to the consumption table and subset for meters in Dungarvan
left_join = '''
SELECT c.MeterID, c.Date, c.Usage, m.Eircode, m.City
FROM consumption AS c
LEFT JOIN metermaster AS m ON c.MeterID = m.MeterID
WHERE m.City = "Dungarvan";
'''

#print(mysql(left_join))

## Aggregate query

### Aggregate query including a Join
### It finds the average meter usage for meters in the town of Dungarvan
aggregate_query = '''
SELECT c.MeterID, AVG(c.Usage) AS 'MeterUsage (kWh)'
FROM consumption AS c
INNER JOIN metermaster AS m ON c.MeterID = m.MeterID
WHERE m.City = "Dungarvan"
GROUP BY c.MeterID;
'''

### Find the monthly average usage by town
aggregate_query2 = '''
SELECT strftime('%m', co.Date) AS Month, cu.Town AS Town, AVG(co.Usage) AS AverageUsage
FROM consumption AS co
INNER JOIN accounts AS a ON co.MeterID = a.MeterID
INNER JOIN customers as cu ON a.CustomerID = cu.CustomerID
GROUP BY Month, cu.Town
'''

### Find the second highest cumulative value
second_highest_query = '''
SELECT c.MeterID AS MeterID, SUM(c.Usage) AS SecondHighest
FROM consumption AS c
GROUP BY c.MeterID
ORDER BY SUM(c.Usage) DESC
LIMIT 1 OFFSET 1
'''

print(mysql(aggregate_query))

### Find the name of the customer with the greatest electricity consumption in January

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
    WHERE co.Date BETWEEN '2021/01/01' AND '2021/31/01'
    GROUP BY co.MeterID
    ) AS s2
ON s1.MeterID = s2.MeterID;
'''

#print(mysql(highest_customer_query))