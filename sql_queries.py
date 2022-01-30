"""
Code for practicing SQL queries in Python
"""

import pandas as pd
from pandasql import sqldf

## Functions
mysql = lambda q: sqldf(q, globals())

## Import datasets
consumption = pd.read_csv("./Mock dataset/Consumption.csv")
metermaster = pd.read_csv("./Mock dataset/MeterMaster.csv")
accounts = pd.read_csv("./Mock dataset/Accounts.csv")

## Run queries
#print(consumption.head())

select_query = mysql("SELECT * from metermaster LIMIT 5;")
#print(select_query)

join_query = '''
SELECT c.MeterID, c.Date, c.Usage, m.Eircode, m.City
FROM consumption AS c
INNER JOIN
metermaster AS m
ON c.MeterID = m.MeterID;
'''

print(mysql(join_query))