from pypdf import PdfReader
from pathlib import Path
import re
import pandas as pd
# from pandasgui import show 
from write_data import write_clean_data
from datetime import datetime
from dateutil import parser

import os

directory_path = './pdfs'
out_file = ''
state_abbreviations = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

# for DataFrame 
# transactionData = {
#     "date": [],
#     "type": [],
#     "category": [],
#     "amount": []
# }

# for MySQL .executemany() multiple-row syntax
transactionData = []

# data = {
#     "startDate": "",
#     "endDate": "",
#     "beginningBalance": 0.0,
#     "endingBalance": 0.0,
#     "transactions": None
# }
data = []


def stringifyPdf(path):
    """
        Takes a path to a pdf, OCR the text, and returns it as a string
    """
    pdfStr = ""
    reader = PdfReader(path)
    print("reading", path)
    pages = reader.pages[0:-1]

    for page in range(len(pages)):
        pdfStr += pages[page].extract_text()
    pdfStr = pdfStr.replace('\n', ' ')
    
    return pdfStr



def extractPattern(transaction: str, billingPeriod):
    """
        Extract Pattern 1: date in the middle 
    """
    date = None
    type = None
    category = None
    amount = None
    
    splitTrans = list(transaction[0])

    splitTrans[1] = splitTrans[1].strip()
    splitTrans[-2] = splitTrans[-2].strip()
    
    date = convertDateFormat(assignYear(splitTrans[2], billingPeriod))

    # remove "authorized" if there is one in the string
    tempType = splitTrans[1].split()
    if tempType[-1] == "authorized":
        type = " ".join(tempType[0:-1])
    else:
        type = " ".join(tempType)

    catPattern = r"(.*?\b)  ?(?:[S|P]\d+ Card 1848)"
    cleanCategory = re.findall(catPattern, splitTrans[3])
    if cleanCategory:
        category = removeNoise(cleanCategory[0])
    else:
        # ATM, Zelle
        if "ATM" in splitTrans[1]:
            # [('4511 Campus Dr Irvine CA  0002392 ', 'ATM ID 9821A Card 1848')]
            # just take the first of the group list and clean it 
            category = removeNums(re.findall(r"(.*?\b)(ATM ID.*)", splitTrans[3])[0][0])

            # print(category)
            # deal with ATM
        elif "Zelle" in splitTrans[1]:
            category = removeNoise(re.sub(r"Ref\s*#\s*\S+", "", splitTrans[3]).strip())
        else:
            # Error: Albertsons #0597 Irvine CA S624065475280122 Card
            print(f"Extract Error: {splitTrans[3]}")

        if category == "":
            category = "personal"
    
    amount = splitTrans[4]

    return date, type, category, amount



def extractOtherPattern(transaction: str, billingPeriod):
    """
        Extract Pattern 2: transaction with no date, date at the end
    """
    otherPattern = r"(\d{1,2}\/\d{1,2})(.+?)(on)?(\s+\d{2}\/\d{2}\/\d{2}\s+)? (\d{0,},?\d{1,}\.\d{2})"
    matchstr = re.fullmatch(otherPattern, transaction)
    
    date = None
    type = None
    category = None
    amount = None

    if matchstr:
        if matchstr.group(4): 
            date = convertDateFormat(matchstr.group(4))
        else:
            date = convertDateFormat(assignYear(matchstr.group(1), billingPeriod))
        
        type = "Bills and Transfers"
        category = removeNoise2(matchstr.group(2))
        amount = matchstr.group(5)
        # print(date, type, category, amount)
    return date, type, category, amount

def removeRef(text: str):
    """
        removes transaction reference number
    """
    return re.sub(r"Ref\s*#\s*\S+", "", text).strip()

def removeCard(text: str):
    return re.sub(r"xxxxxx\d{4}", "", text)

def removeNums(text: str):
    return re.sub(r"( \d+ \d+)|( \d+ )", " ", text)

def removeState(text: str):
    return re.sub(r"AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY", "", text)

def removeExtraSpace(text: str):
    return re.sub(r"( [ ]+)", " ", text)

def removeIdentifiers(text: str):
    """
        begin with a hash, phone numbers, consecutive numbers
        
    """
    return re.sub(r"[0-9#*-]+", "", text)

def removeDate(text: str):
    """
        removes 'on {date}' 
    """
    return re.sub(r" on \d{1,}\/\d{2}\/\d{2}", "", text)

def removeNoise(text: str):
    """
        Removes numbers, card #, ref #, state, identifiers, extra space 
    """
    removeFunc = [removeNums, removeCard, removeRef, removeState, removeIdentifiers, removeExtraSpace]
    temp = text
    for func in removeFunc:
        temp = func(temp)
    return temp

def removeNoise2(text: str):
    """
        Removes numbers, card #, ref #, state, extra space (no identifiers)
    """
    removeFunc = [removeNums, removeCard, removeRef, removeState, removeDate, removeExtraSpace]
    temp = text
    for func in removeFunc:
        temp = func(temp)
    # print(temp)
    return temp

def toFloat(amount):
    if "," in amount:
        return float("".join(amount.split(",")))
    else:
        return float(amount)

# for Dataframe
# def addEntryData(date, type, category, amount):
#     """
#         Add entry to transactionData in DataFrame format
#     """
#     transactionData.get("date").append(date)
#     transactionData.get("type").append(type)
#     transactionData.get("category").append(category)
#     transactionData.get("amount").append(amount)

def addEntryStatement(date: str, type: str, description: str, amount: float):
    """
        Add entry to transactionData in multiple row format
    """
    # print(f"Adding {tuple([date, type, category, amount])}")
    transactionData.append(tuple([date, type, description, amount]))

def assignYear(date, billingPeriod):
    """
        takes a MM/DD date and a billing period (MM/DD/YYYY, MM/DD/YYYY)
        returns the appropriate YYYY/MM/DD
    """
    start = billingPeriod[0].split("/")
    end = billingPeriod[1].split("/")
    startMonth = start[0]
    # if int month match, then return the start year, if not return end year 
    month = date.split("/")[0]

    if int(month) == int(startMonth):
        return start[2] + "/" + date
    else:
        return end[2] + "/" + date

def convertDateFormat(date: str):
    """
        Change a YYYY/MM/DD to YYYY-MM-DD for MySQL 
    """
    return date.replace("/", "-")


def clean(text: str, billingPeriod):
    """
        Captures transactions from stringified PDF, adds them to transactionData

        Split into two major categories:
            1. transactions that have a date in the middle 
            2. transactions that don't have a date OR have a date at the end

        -- ATTENTION!! --
        The OCR can return a string that has the date and the amount stuck together, which is unable to be captured!!
        Examples:
        - ********** ***** Rent769.00
        - Ref #********* on 12/10/2350.00 101.44
    """
    cleanedTransactions = []

    pattern = r"(Beginning balance on )?(\d{1,2}\/\d{1,2})(.*?)(\d{1,2}\/\d{1,2})?(.*?)(\d{1,}\.\d{2})"
    # finditer instead of findmatch() so it returns the captured string and not the groups
    transactions = re.finditer(pattern, text)

    tPattern = r"(\d{1,2}\/\d{1,2})(.*?) on (\d{2}\/\d{2}) (.*?)(\d{1,}\.\d{2})"

    total = 0
    added = 0

    for transaction in transactions:
        total += 1
        transactionString = transaction.group()
        segements = re.findall(tPattern, transactionString)

        date = None
        type = None
        description = None
        amount = None

        if segements:
            date, type, description, amount = extractPattern(segements, billingPeriod)
        else:
            date, type, description, amount = extractOtherPattern(transactionString, billingPeriod)
        

        # check if returned strings are valid
        if all([True if i is not None else False for i in [date, type, description, amount]]):
            added += 1
            amount = toFloat(amount)
            cleanedTransactions.append(tuple([date, type, description, amount]))
        else:
            # print(f"clean() Error '{transactionString}': {date}, {type}, {category}, {amount}")
            pass


    print(f"Total items parsed: {total}\nAmount of transactions added: {added}")
    print("")

    return cleanedTransactions, total, added

def getBillingData(text: str):
    """
        returns tuples containing the beginning amount, ending amount, the period of time between them
    """
    startPattern = r"(Beginning balance) on (\d{1,}\/\d{1,})\s+\$((\d{1,},?)*.\d{2})"
    endPattern = r"(Ending balance) on (\d{1,}\/\d{1,})\s+\$((\d{1,},?)*.\d{2})"
    startMatch = re.findall(startPattern, text)[0][0:3]
    endMatch = re.findall(endPattern, text)[0][0:3]

    yearPattern = r"Fee period (\d{2}\/\d{2}\/\d{4}) - (\d{2}\/\d{2}\/\d{4})"
    
    yearMatch = re.findall(yearPattern, text)

    return startMatch, endMatch, yearMatch[0]


def processText(text):
    """
        Given a stream of text for a PDF, extract start/end date, balance, and transactions
    """
    begBalance, endBalance, feePeriod = getBillingData(text)

    temp_data = {}
    
    temp_data["startDate"] = feePeriod[0]
    temp_data["endDate"] = feePeriod[1]
    temp_data["beginningBalance"] = toFloat(begBalance[2])
    temp_data["endingBalance"] = toFloat(endBalance[2])

    transactions, pdf_total, pdf_added = clean(text, feePeriod)
    temp_data["totalTransactions"] = pdf_added
    temp_data["transactions"] = transactions
    return temp_data, pdf_total, pdf_added


def parseFile(file):
    """
        takes a byte stream/file object to parse, returns data, total # of transactions, added # of transactions to data
    """
    text = stringifyPdf(file)
    temp_data, pdf_total, pdf_added = processText(text)
    return temp_data, pdf_total, pdf_added

def parseDir(pdfDir: str):
    """
        takes a path to a directory of pdfs, grabs the text, cleans it for billing and transaction information, and then adds it all into the same list\n
        returns a list containing every transaction: (date, type, category, amount)
    """
    total = 0
    added = 0

    for filename in os.listdir(pdfDir):
        path = os.path.join(pdfDir, filename)

        text = stringifyPdf(path)
        temp_data, pdf_total, pdf_added = processText(text)
        
        total += pdf_total
        added += pdf_added

        data.append(temp_data)

    print(f"\n{len(data)} PDFs scanned, {total} items parsed, {added} transactions added")

    return transactionData
    

"""
    pypdf behavior: (is it consistent?)
        - first row is beginning balance
        - second row is ending balance
        - [-2] is ending balance
        - [-1] is Standard montly service fee line

    text = ""
    for i in range(len(transactionData['type'])):
        
        temp = f"{transactionData['type'][i]} {transactionData['category'][i]}\n"
        text += temp

    clean the text
    write_clean_data("sample data fixed", transactionData)
    label the text
    pass it into create_csv() for organization 
    create_csv("sample training", "sample_training_labeled")
"""


"""
    1. Put it in a data frame for viewing
    2. Write cleaned data to a file 
    3. Label it all (somehow)
    4. train/test split it 
    5. train it/test it
"""

def main():
    # clean(stringifyPdf(directory_path))
    parseDir(directory_path)
    # df = pd.DataFrame(transactionData)
    # show(df)
    toFloat("12,002,010.45")

if __name__ == "__main__":
    main()