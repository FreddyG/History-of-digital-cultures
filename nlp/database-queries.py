import datetime
import mysql.connector


def __main__():
    # Connect to database
    cnx = mysql.connector.connect(user='root', database='testing')
    cursor = cnx.cursor(buffered=True)

    tables = []
    finaltables = []
    timestamps = []

    # Show tables
    table_cursor = show_tables(cursor)
    for i in table_cursor:
        tables.append(i[0])

    total_messages = 0
    # Select the tables on which the messages are greater than 10
    for t in tables:
        amount_cursor = get_total_amount_messages("`" + t + "`", cursor)
        for k in amount_cursor:
            total_messages += k[0]
            if k[0] >= 10:
                finaltables.append(t)

    print("Total messages: " + str(total_messages))

    # Query the tables and get first / last message of each café
    for new_tables in finaltables:
        cafe_first_last_messages_cursor = query_cafe_first_last_messages("`" + new_tables + "`", "desc", cursor)
        for messages in cafe_first_last_messages_cursor:
            print(
                messages[0] + ", " + messages[1] + ", timestamp: " + str(datetime.datetime.fromtimestamp(messages[2])))
            timestamps.append(messages[2])

    # Get oldest timestamp and newest timestamp + print it
    youngest_timestamp = min(timestamps)
    now = datetime.datetime.now().timestamp()
    oldest_timestamp = max(dt for dt in timestamps if dt < now)
    print(str(datetime.datetime.fromtimestamp(youngest_timestamp)) + ", " + str(datetime.datetime.fromtimestamp
                                                                                (oldest_timestamp)))

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

    # Get first and last message from designated cafe (asc or desc)
    cafe_first_last_messages_cursor = query_cafe_first_last_messages("`13`", "asc", cursor)
    for messages in cafe_first_last_messages_cursor:
        print(messages[0] + ", timestamp: " + str(messages[1]))

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


# Returns first or last message from cafe
def query_cafe_first_last_messages(cafe, mode, cursor):
    query = ("SELECT cafe, message, timestamp FROM " + cafe + " ORDER BY timestamp " + mode + " limit 1")
    cursor.execute(query)

    return cursor


def get_total_amount_messages(cafe, cursor):
    query = ("SELECT count(message) FROM " + cafe)
    cursor.execute(query)

    return cursor


if __name__ == '__main__':
    __main__()
