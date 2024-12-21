import mysql.connector
from mysql.connector.cursor import MySQLCursorAbstract

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

# root, password

def insertTransactions(connector, cursor: MySQLCursorAbstract, transactionData):
    print("insertTransaction")
    # print("Inserting Transaction Data into database...")
    # print(cursor, transactionData)
    # sql = f"INSERT INTO {TABLE} (date, type, category, amount) VALUES (?, ?, ?, ?)"
    for i in range(len(transactionData)):
        print(transactionData[i][0])
    #     cursor.execute(sql, transactionData[i])
    # cursor.executemany(sql, transactionData)
    print("Finished inserting data")

def setupDatabase(connector, cursor: MySQLCursorAbstract):
    cursor.execute("DROP DATABASE IF EXISTS budget_app")
    cursor.execute("CREATE DATABASE IF NOT EXISTS budget_app")
    print("Created budget_app database")
    connector.database = "budget_app"
    cursor.execute("DROP TABLE IF EXISTS transactions")
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS transactions (
                        id INT AUTO_INCREMENT PRIMARY KEY, 
                        date VARCHAR(100),
                        type VARCHAR(100),
                        category VARCHAR(100),
                        amount FLOAT)
                    """)
    print("Created transactions table")
    connector.commit()

def getData():
    return 
