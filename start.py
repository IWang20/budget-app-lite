from parse_pdfs import startParse
from db import connect, insertTransactions, setupDatabase
from embedding import load_model, categorize, write_data, train, test_pred

PDF_DIRECTORY = "./pdfs"
HOST = "localhost"
USER = "budget-app"
PASSWORD = "password"


# FIX!!!! START PARSE DOESN'T RETURN A LIST ANYMORE 


def main():
    """
        connects to MySQL, extracts trasactions from PDF_DIRECTORY, sets up the database, and inserts the transactions  
    """
    connector, cursor = connect(HOST, USER, PASSWORD)
    transactionData = startParse(PDF_DIRECTORY)
    # write_data("data.txt", set([transaction[2] for transaction in transactionData]))
    setupDatabase(connector, cursor)
    # insertTransactions(connector, cursor, transactionData)
    # model = load_model("budget-1.bin")
    # model = train("labeled_data.txt", "budget-1.bin")
    # test_pred("labeled_data.txt", model)
    # pred = categorize("chipotle", model)
    # print(pred)



if __name__ == "__main__":
    main()