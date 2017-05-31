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


def articleTitleAuthor():
# Displays all article titles and their authors

    connect()

    # SQL command
    c.execute("""
        select title, name
        from articles, authors
        where articles.author = authors.id;
    """)

    # Display Result
    reportResults("All article titles and their authors", " ")

    # Disconect from database
    conn.close()


def topArticles(): 
# Displays the top three articles of all time. Most popular article at the top.

    connect()

    # SQL command
    c.execute("""
        select title, count(path) as num
        from articles, log
        where slug = substr(path, 10) group by title order by num desc limit 3;
    """)

    # Display Result
    reportResults("Top 3 Articles of All Time", "views")

    # Disconect from database
    conn.close()


def topAuthors():
# Displays the most popular article authors of all time. Most popular author at the top.

    connect()

    # SQL command
    c.execute("""
        select name, count(path) as num
        from authors, log, articles
        where author = authors.id and slug = substr(path, 10) 
        group by name order by num desc limit 3;
    ;""")

    # Display Result
    reportResults("Top 3 Authors of All Time", "views")

    # Disconect from database
    conn.close()


def errorCheck():
# Displays which days had more than 1% of requests lead to errors.

    connect()

    # SQL command
    c.execute("""
        select extract(day from time), round((error * 100.0) / (count(substr(status, 1, 3))), 2)
        from (
            select extract(day from log.time) as day, count(substr(status, 1, 3)) as error
            from log
            where substr(status, 1, 3) = '404' group by day
            ) as sub, log
        where substr(status, 1, 3) = '200'
        group by extract(day from log.time), error
        """)

    # Display Result
    reportResults("Days where more than 1% of requests lead to errors", " ")

    # Disconect from database
    conn.close()

articleTitleAuthor()
topArticles()
topAuthors()
errorCheck()