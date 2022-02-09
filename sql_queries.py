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

## Run queries
#print(consumption.head())

## SELECT queries

select_query = mysql("SELECT * from metermaster LIMIT 5;")
#print(select_query)

select_query2 = '''
SELECT * 
FROM consumption
WHERE Date BETWEEN '10/01/2021' AND '13/01/2021'
'''

#print(mysql(select_query2))

## JOIN queries

inner_join = '''
SELECT c.MeterID, c.Date, c.Usage, m.Eircode, m.City
FROM consumption AS c
INNER JOIN
metermaster AS m
ON c.MeterID = m.MeterID;
'''

left_join = '''
SELECT c.MeterID, c.Date, c.Usage, m.Eircode, m.City
FROM consumption AS c
LEFT JOIN
metermaster AS m
ON c.MeterID = m.MeterID
WHERE m.City = "Dungarvan";
'''

#print(mysql(left_join))

## Aggregate query

### Aggregate query including a JOIN
aggregate_query = '''
SELECT c.MeterID, AVG(c.Usage) AS 'MeterUsage (kWh)'
FROM consumption AS c
INNER JOIN
metermaster AS m
ON c.MeterID = m.MeterID
WHERE m.City = "Dungarvan"
GROUP BY c.MeterID;
'''

#print(mysql(aggregate_query))

## Find the name of the customer with the greatest electricity consumption in January

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
    WHERE co.Date BETWEEN '01/01/2021' AND '31/01/2021'
    GROUP BY co.MeterID
    ) AS s2
ON s1.MeterID = s2.MeterID;
'''

print(mysql(highest_customer_query))