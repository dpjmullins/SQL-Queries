# SQL-Queries

Test SQL queries are run in Python using pandas data frames and the pandasql library.

The SQL queries can be found in the script "sql_queries.py". Join, aggregation and complex nested queries are shown.

Some SQL functions are described below. 

## JOIN Queries

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

## DROP TABLE and TRUNCATE TABLE

```DROP TABLE``` deletes a table in the database.

```TRUNCATE TABLE``` deletes the data inside a table, but not the table itself. 
