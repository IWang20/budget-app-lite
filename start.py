from parse_pdfs import startParse
from db import connect, insertTransactions, setupDatabase
from embedding import load_model, categorize, write_data

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
    # connector, cursor = connect(HOST, USER, PASSWORD)
    transactionData = startParse(PDF_DIRECTORY)
    write_data("data.txt", set([transaction[2] for transaction in transactionData]))
    # setupDatabase(connector, cursor)
    # insertTransactions(connector, cursor, transactionData)
    # model = load_model("budget-0.bin")
    # pred = categorize("Purchase Chipotle Online Chipotle.Com", model)
    # print(pred)



if __name__ == "__main__":
    main()