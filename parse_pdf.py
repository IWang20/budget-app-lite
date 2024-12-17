from pypdf import PdfReader
from pathlib import Path
import re
import pandas as pd
from pandasgui import show 
from create_data import write_clean_data

import os

directory_path = './pdfs'
out_file = ''

# print(temp)
# (Beginning balance on )?(\d{1,2}\/\d{1,2})(.*?)(\d{1,2}\/\d{1,2})(.*?)(\d{1,}\.\d{2})# # (\d{1,2}\/\d{1,2})(.*?) (\d{1,}\.\d{2})
# https://regex101.com/r/jsCfJi/1

# This format is used for DataFrame
transactionData = {
    "date": [],
    "type": [],
    "category": [],
    "amount": []
}

metaData = {
    "startDate": "",
    "endDate": "",
    "beginningBalance": 0.0,
    "endingBalance": 0.0
}


def stringifyDirs(path: str):
    """
        Takes a path to a bunch of pdfs, OCR the text, combines them all to a single string for cleaning
    """
    pdfStr = ""
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)

        reader = PdfReader(file_path)
        print("reading", file_path)
        pages = reader.pages[1:-2]
        temp = ""
        # print(len(pages))
        for page in range(len(pages)):
            # print("Page", page)
            temp += pages[page].extract_text()
            temp = temp.replace('\n', ' ')
            pdfStr += temp
    #     print(temp)
    
    # file_path = "./pdfs/010824 WellsFargo.pdf"

    # reader = PdfReader(file_path)
    # print("reading", file_path)
    # pages = reader.pages[1:-2]
    # temp = ""
    # # print(len(pages))
    # for page in range(len(pages)):
    #     # print("Page", page)
    #     temp += pages[page].extract_text()
    # # print(temp)
    
    
    return pdfStr

def removeNoise(text: str):
    """
        Removes numbers, lone characters, extra spaces 
    """
    patterns = [(r"[0-9#*-]+", ""), (r"( [A-Za-z] )|  ", " "), (r"( [ ]+)", " ")]
    temp = text
    for remove_pattern, sub in patterns:
        temp = re.sub(remove_pattern, sub, temp)
    return temp

def extractPattern(transaction: str):
    """
        Extract matched text and inserts it into the DataFrame
        - Most of the text is already matched, but the category (splitTrans[3]) needs further extraction
    """
    success = False

    splitTrans = list(transaction[0])
    splitTrans[1] = splitTrans[1].strip()
    splitTrans[-2] = splitTrans[-2].strip()
    transactionData.get("date").append(splitTrans[2])
    
    type = splitTrans[1].split()
    if type[-1] == "authorized":
        transactionData.get("type").append(" ".join(type[0:-1]))
    else:
        transactionData.get("type").append(" ".join(type))
    
    catPattern = r"(.*?\b)  ?(?:[S|P]\d+ Card 1848)"
    clean_category = re.findall(catPattern, splitTrans[3])
    # print(clean_category)
    if clean_category:
        splitTrans[3] = removeNoise(clean_category[0])
        success = True
    else:
        # ATM, Zelle 
        if "ATM" in splitTrans[1]:
            splitTrans[3] = re.findall(r"(.*?\b)(ATM ID.*)", splitTrans[3])
            success = True
        elif "Zelle" in splitTrans[1]:
            splitTrans[3] = removeNoise(re.sub(r"Ref\s*#\s*\S+", "", splitTrans[3]).strip())
            success = True
        else:
            # Error: Albertsons #0597 Irvine CA S624065475280122 Card
            print(f"Extract Error: {splitTrans[3]}")

        if splitTrans[3] == "":
            splitTrans[3] = "personal"
        
    transactionData.get("category").append(splitTrans[3])
    transactionData.get("amount").append(splitTrans[4])

    return success


def removeRef(text: str):
    return re.sub(r"Ref\s*#\s*\S+", "", text).strip()

def removeCard(text: str):
    return re.sub(r"xxxxxx\d{4}", "", text)

def removeNums(text: str):
    return re.sub(r"( \d+ \d+)|( \d+ )", "", text)

def extractMisc(transaction: str):
    """
        Some pattern matching may fail, this is used to extract remainders
    """
    re.sub(r"Ref\s*#\s*\S+", "", transaction)
    transaction = re.sub(r"( [ ]+)", " ", removeRef(removeCard(transaction)))
    print(f"-{transaction}-")
    return transaction
    


def clean(text: str):
    """
        Captures transactions
        Split into two major categories:
            1. transactions that have a date in the middle 
            2. transactions that don't have a date OR have a date at the end

        -- ATTENTION!! --
        The OCR can return a string that has the date and the amount stuck together, which is unable to be captured!!
        Examples:
        - ********** ***** Rent769.00
        - Ref #********* on 12/10/2350.00 101.44
    """
    pattern = r"(Beginning balance on )?(\d{1,2}\/\d{1,2})(.*?)(\d{1,2}\/\d{1,2})?(.*?)(\d{1,}\.\d{2})"
    # finditer instead of findmatch() so it returns the captured string and not the groups
    transactions = re.finditer(pattern, text)

    tPattern = r"(\d{1,2}\/\d{1,2})(.*?) on (\d{2}\/\d{2}) (.*?)(\d{1,}\.\d{2})"

    # what about the amount withdrawn
    # (\d{1,2}\/\d{1,2})(.*?)(\d{1,},?\d{1,}\.\d{2})

    error_count = 0
    transaction_errors = []
    total = 0

    for transaction in transactions:
        total += 1
        transactionString = transaction.group()
        segements = re.findall(tPattern, transactionString)

        if segements:
            # {Date} {Type} {Date} {Anything} {Amount}
            extractPattern(segements)
        else:
            pass
            # Without date in the middle
            # Zelle, Online Transfer, Start/End Date and values
            # some end of dates are being stuck to the price
            # ((Beginning balance on )?(\d{1,2}\/\d{1,2})\s+\$?([\d{1,},]+\.\d{2}))|((\d{1,2}\/\d{1,2})(.*?)(on)?(\s+\d{2}\/\d{2}\/\d{2}\s+)?(\d{1,}\.\d{2}))
            # error_count += 1

            # Offer a way for people to enter the data manually 
            # print("Error:", transactionString)


    print(f"""Text extraction complete!!\n
          Total Transactions parsed: {total}\n
          Error Count: {error_count}""")        
            

    # pypdf behavior: (is it consistent?)
    #  - first row is beginning balance
    #  - second row is ending balance
    #  - [-2] is ending balance
    #  - [-1] is Standard montly service fee line

    # text = ""
    # for i in range(len(transactionData['type'])):
        
    #     temp = f"{transactionData['type'][i]} {transactionData['category'][i]}\n"
    #     text += temp

    # clean the text
    # write_clean_data("sample data fixed", transactionData)
    # label the text
    # pass it into create_csv() for organization 
    # create_csv("sample training", "sample_training_labeled")


"""
    1. Put it in a data frame for viewing
    2. Write cleaned data to a file 
    3. Label it all (somehow)
    4. train/test split it 
    5. train it/test it
"""

def main():
    clean(stringifyDirs(directory_path))
    df = pd.DataFrame(transactionData)
    show(df)

if __name__ == "__main__":
    main()