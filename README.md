Logs-Analysis-Tool
==================
Server-End Python reporting tool that uses SQL queries to print out reports (in plain text) based on the data in the database.


To Run
------

1. Ensure python is installed
2. Navigate to the script directory
3. Load the data into your local database with:  psql -d news -f newsdata.sql
4. Run "reporting_tool.py"


Description
-------------

This program will first attempt connection to the "news" database which stores articles, authors, and HTTP logs. Then run four different SQL queries that will provide answers to some key questions. These questions include:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

Lastly, the program serves the answers back to the user through print statements.


