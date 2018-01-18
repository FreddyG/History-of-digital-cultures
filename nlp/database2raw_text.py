import datetime
import mysql.connector
from calendar import monthrange
import sys
import os
import time


def __main__():
    # Connect to database
    cnx = mysql.connector.connect(user='root', database='nebu', password="sudowoodo")
    cursor = cnx.cursor(buffered=True)

    # check if data folder exists
    if not os.path.exists('data'):
        os.makedirs('data')

    # get tables
    table_cursor = show_tables(cursor)
    cafes = []
    for table in table_cursor:
        cafes.append(table[0])

    for cafe in cafes:
        # go through month by month
        for year in range(1994, 1997):
            for month in range(1, 13):
                start = datetime.datetime(year, month, 1, 00, 00, 00).timestamp()
                end = datetime.datetime(year, month, monthrange(year, month)[1], 23, 59, 59).timestamp()
                sql_result = query_cafe_between_timestamps(cafe, start, end, cursor)

                if sql_result.rowcount == 0:
                    continue

                f = open('data/{}-{}-{}.txt'.format(cafe, year, month), 'w')
                for messages in sql_result:
                    f.write(messages[0]+'\n')
                f.close()

    cursor.close()
    cnx.close()


# Shows tables
def show_tables(cursor):
    query = "show tables"
    cursor.execute(query)

    return cursor


# Returns messages between timestamps
def query_cafe_between_timestamps(cafe, timestampbegin, timestampend, cursor):
    query = "SELECT message FROM `{}` WHERE timestamp BETWEEN {} AND {}".format(cafe, timestampbegin, timestampend)
    cursor.execute(query)
    return cursor


if __name__ == '__main__':
    __main__()
