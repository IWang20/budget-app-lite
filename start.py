from parse_pdfs import startParse
from db import connect, insertTransactions, setupDatabase

PDF_DIRECTORY = "./pdfs"
HOST = "localhost"
USER = "budget-app"
PASSWORD = "password"


# get the formatted dictionary 
# call db on formatted dictionary 


def main():
    """
        connects to MySQL, extracts trasactions from PDF_DIRECTORY, sets up the database, and inserts the transactions  
    """
    connector, cursor = connect(HOST, USER, PASSWORD)
    transactionData = startParse(PDF_DIRECTORY)
    setupDatabase(connector, cursor)
    # insertTransactions(connector, cursor, transactionData)



if __name__ == "__main__":
    main()