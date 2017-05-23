#! /usr/bin/env python3
import psycopg2
from datetime import datetime

# Init global variables to store connection details
conn = ""
cur = ""


def init_connection():
    global conn, cur
    conn = psycopg2.connect(database='news')
    cur = conn.cursor()


def close_connection():
    global conn, cur
    conn.commit()
    conn.close()


# Gets the N top articles in order from most views to least
def get_top_articles(number):
    global conn, cur
    init_connection()

    cur.execute("select * from top_articles LIMIT %s;", (number,))
    results = cur.fetchall()

    close_connection()
    return (results)


# Gets the authors and how many views each of them have in descending order
def get_author_views():
    global conn, cur
    init_connection()

    cur.execute("""select article_authors.name, SUM(top_articles.num) AS views
            FROM article_authors, top_articles
            WHERE article_authors.title = top_articles.title
            GROUP BY name ORDER BY views DESC;""")
    results = cur.fetchall()

    close_connection()
    return (results)


def get_error_number(percent):
    global conn, cur
    init_connection()

    cur.execute("SELECT day, percent FROM log_percentage_status_by_day " +
                "WHERE status != '200 OK' AND percent >= %s;", (percent,))
    results = cur.fetchall()

    close_connection()
    return (results)


def print_report_title():
    return """ _                  ______                      _
| |                 | ___ \                    | |
| |     ___   __ _  | |_/ /___ _ __   ___  _ __| |_
| |    / _ \ / _` | |    // _ \ '_ \ / _ \| '__| __|
| |___| (_) | (_| | | |\ \  __/ |_) | (_) | |  | |_
\_____/\___/ \__, | \_| \_\___| .__/ \___/|_|   \__|
              __/ |           | |
             |___/            |_|                   """

timestamp = datetime.now().strftime('%Y-%m-%d%H%M%S')
filename = "logReport" + timestamp + ".txt"
f = open(filename, 'w')
f.write(print_report_title())
f.write('\n\n')
f.write(datetime.now().strftime(
    'This report was created on %Y-%m-%d at %H:%M:%S'))

print("\nGenerating report to file " + filename + ", please wait...")

# Grab data from database
top3_articles = get_top_articles(3)
top_authors = get_author_views()
high_error_days = get_error_number(0.01)

f.write('\n\n')
f.write("The top three articles are:\n")
for i in top3_articles:
    f.write("Title: " + i[0] + "\t\tViews: " + str(i[1]))
    f.write('\n')

f.write('\n\n')
f.write("Article authors, sorted from most popular to least:\n")
for i in top_authors:
    f.write("Name: " + i[0] + "\t\t\tViews: " + str(i[1]))
    f.write('\n')

f.write('\n\n')
f.write("All dates when more than 1% of requeses led to errors:\n")
for i in high_error_days:
    f.write("date: " + i[0].strftime('%B %d, %Y') +
            "\t\t\tpercent: " + str(i[1]))
    f.write('\n')

f.close

print("\nDone!\n")
