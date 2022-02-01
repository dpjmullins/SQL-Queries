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

## Run queries
#print(consumption.head())

## SELECT query

select_query = mysql("SELECT * from metermaster LIMIT 5;")
#print(select_query)

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


print(mysql(aggregate_query))