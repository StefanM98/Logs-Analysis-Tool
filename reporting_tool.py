#!/usr/bin/env python2
import psycopg2


def connect():
    # Establishes connection to the database

    global conn
    global c

    # Attempt connection to database
    try:
        conn = psycopg2.connect("dbname=news")
    except:
        print "Unable to connect to the database"

    # Initialize cursor
    c = conn.cursor()


def reportResults(Name, type):
    # Prints results of queries back into the console

    result = c.fetchall()
    print "\n", Name, ":\n"
    for row in result:
        print ' ', row[0], ' - ', row[1], type


# Attempt connection to database
connect()


def articleTitleAuthor():
    # Displays all article titles and their authors

    # SQL command
    c.execute("""
        select title, name
        from articles, authors
        where articles.author = authors.id;
    """)

    # Display Result
    reportResults("All article titles and their authors", " ")


def topArticles():
    # Displays the top three articles of all time.
    # Most popular article at the top.

    # SQL command
    c.execute("""
        select title, count(path) as num
        from articles, log
        where slug = substr(path, 10) group by title order by num desc limit 3;
    """)

    # Display Result
    reportResults("Top 3 Articles of All Time", "views")


def topAuthors():
    # Displays the most popular article authors of all time.
    # Most popular author at the top.

    # SQL command
    c.execute("""
        select
            name,
            count(path) as num
        from
            authors, log, articles
        where author = authors.id and slug = substr(path, 10)
        group by name
        order by num desc;
    ;""")

    # Display Result
    reportResults("Top Authors of All Time", "views")


def errorCheck():
    # Displays which days had more than 1% of requests lead to errors.

    # SQL command
    c.execute("""

    select
        PercentErrored.LogDate,
        to_char((round(PercentErrored.PercentageOf404, 2)), '999D99%')

    from
    (
        select
            Errored.LogDate,
            Errored.HTTPStatus404Total,
            (Errored.HTTPStatus404Total / Totaled.total) * 100 as PercentageOf404
            from
            (
                select
                    time::date as LogDate,
                    count(*) * 1.0 as HTTPStatus404Total
                from log
                where substr(status, 1, 3) = '404'
                group by time::date order by LogDate
            ) as Errored,
            (
                select time::date as LogDate,
                count(*) * 1.0 as total
                from log
                group by time::date order by LogDate
            ) as Totaled
        where Errored.LogDate = Totaled.LogDate
    ) as PercentErrored
    where PercentErrored.PercentageOf404 > 1
    """)

    # Display Result
    reportResults("Days where more than 1% of requests lead to errors",
                  "errored")


articleTitleAuthor()
topArticles()
topAuthors()
errorCheck()

# Disconect from database
conn.close()
