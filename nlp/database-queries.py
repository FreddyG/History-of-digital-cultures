import datetime
import mysql.connector


def __main__():
    # Connect to database
    cnx = mysql.connector.connect(user='root', database='testing')
    cursor = cnx.cursor(buffered=True)

    # Show tables
    table_cursor = show_tables(cursor)
    for i in table_cursor:
        print(i[0])

    # Get all messages from the designated cafe
    query_cafe_cursor = query_cafe("europa", cursor)
    for messages in query_cafe_cursor:
        print(messages[0])

    # Get messages from designated cafe with the specified timestamps
    cafe_with_timestamp_cursor = query_cafe_with_timestamp("`13`",
                                                           datetime.datetime(1994, 1, 1, 12, 00, 00).timestamp(),
                                                           datetime.datetime(1995, 10, 1, 21, 00, 00).timestamp(),
                                                           cursor)
    for messages in cafe_with_timestamp_cursor:
        print(messages[0])

    cursor.close()
    cnx.close()


# Shows tables
def show_tables(cursor):
    query = "show tables"
    cursor.execute(query)

    return cursor


# Returns messages from selected cafe
def query_cafe(cafe, cursor):
    query = ("SELECT message FROM " + cafe)
    cursor.execute(query)

    return cursor


# Returns messages between timestamps
def query_cafe_with_timestamp(cafe, timestampbegin, timestampend, cursor):
    query = ("SELECT message FROM " + cafe + " WHERE timestamp BETWEEN %s AND %s")
    cursor.execute(query, (timestampbegin, timestampend))

    return cursor


if __name__ == '__main__':
    __main__()
