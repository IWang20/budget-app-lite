import mysql.connector
from mysql.connector.cursor import MySQLCursorAbstract
from dateutil import parser

DATABASE = "budget_app"
TABLE = "transactions"


def connect(host, user, password):
    print("Connecting to Host: {host} Database: transactions")
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    cursor = mydb.cursor()

    if not mydb:
        print("Error: Did not connect to MySql")
    else:
        print("Successfully connected to MySql")

    return mydb, cursor


def insertTransactions(connector, cursor: MySQLCursorAbstract, transactionData):
    for i in range(len(transactionData)):
    #     print(transactionData[i][0])
    #     cursor.execute(sql, transactionData[i])
    # cursor.executemany(sql, transactionData)
        print(transactionData[i])
        date = parser.parse(transactionData[i][0])
        type = transactionData[i][1]
        category = transactionData[i][2]
        amount = transactionData[i][3]

        # print(f"Inserting: {date.date()}, {type}, {category}, {amount}")
        sql = f"INSERT INTO transactions (date, type, category, amount) VALUES (%s, %s, %s, %s);"
        cursor.execute(sql, (date.date(), type, category, amount))
    query = f"SELECT COUNT(*) FROM transactions;"
    cursor.execute(query)

    rows = cursor.fetchone()[0]
    print(f"Finished inserting data, {rows} transactions inserted")
    connector.commit()

def setupDatabase(connector, cursor: MySQLCursorAbstract):
    cursor.execute("DROP DATABASE IF EXISTS budget_app")
    cursor.execute("CREATE DATABASE IF NOT EXISTS budget_app")
    print("Created budget_app database")
    connector.database = "budget_app"
    cursor.execute("DROP TABLE IF EXISTS transactions")
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS transactions (
                        id INT AUTO_INCREMENT PRIMARY KEY, 
                        date DATE,
                        type VARCHAR(100),
                        category VARCHAR(100),
                        amount FLOAT)
                    """)
    print("Created transactions table")
    connector.commit()

def getData():
    return 
