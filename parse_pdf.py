from pypdf import PdfReader
from pathlib import Path
import re
import pandas as pd
from pandasgui import show 
from create_training_data import create
import spacy
from spacy import displacy

pdf_path = Path("pdfs")

reader = PdfReader("./pdfs/291af904-a0ca-4db0-8cfe-62d97ba2b050.pdf")
pages = reader.pages[1:-2]
temp = ""
# print(len(pages))
for page in range(len(pages)):
    # print("Page", page)
    temp += pages[page].extract_text()
    # print()

temp = temp.replace('\n', ' ')

# print(temp)
# (Beginning balance on )?(\d{1,2}\/\d{1,2})(.*?)(\d{1,2}\/\d{1,2})(.*?)(\d{1,}\.\d{2})# # (\d{1,2}\/\d{1,2})(.*?) (\d{1,}\.\d{2})
# https://regex101.com/r/jsCfJi/1

pattern = r"(Beginning balance on )?(\d{1,2}\/\d{1,2})(.*?)(\d{1,2}\/\d{1,2})?(.*?)(\d{1,}\.\d{2})"
transactions = re.finditer(pattern, temp)

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

tPattern = r"(\d{1,2}\/\d{1,2})(.*?) on (\d{2}\/\d{2}) (.*?)(\d{1,}\.\d{2})"
tPattern2 = r"(\d{1,2}\/\d{1,2})(.*?)(\d{1,},?\d{1,}\.\d{2})"

# what about the amount withdrawn
# (\d{1,2}\/\d{1,2})(.*?)(\d{1,},?\d{1,}\.\d{2})

for transaction in transactions:
    tString = transaction.group()
    segements = re.findall(tPattern, tString)
    if segements:
        splitTrans = list(segements[0])
        splitTrans[1] = splitTrans[1].lstrip()
        splitTrans[-2] = splitTrans[-2].rstrip()
        transactionData.get("date").append(splitTrans[2])
        
        type = splitTrans[1].split()
        if type[-1] == "authorized":
            transactionData.get("type").append(" ".join(type[0:-1]))
        else:
            transactionData.get("type").append(" ".join(type))
        
        catPattern = r"(.*?\b)(?:[S|P]\d+ Card 1848)"
        category = splitTrans[3]
        clean_category = re.match(catPattern, category)
        

        if clean_category:
            nonalpha = r"[0-9#*-]+"
            temp = re.sub(nonalpha, "", clean_category.group(1))
            singles = r"( [A-Za-z] )|  "
            new_category = re.sub(singles, " ", temp)
            transactionData.get("category").append(new_category)
        else:
            nonalpha = r"[0-9#*-]+"
            temp = re.sub(nonalpha, "", splitTrans[3])
            singles = r"( [A-Za-z] )|  "
            new_category = re.sub(singles, " ", temp)
            transactionData.get("category").append(new_category)

        transactionData.get("amount").append(splitTrans[4])
    else:
        # print("ERROR:", tString) # transactions without date(recurring Transfer) and starting/ending values
        err = re.findall(tPattern2, tString)
        splitTrans = list(err[0])
        splitTrans[1] = splitTrans[1].lstrip()
        splitTrans[1] = splitTrans[1].rstrip()
        # print(splitTrans)

# pypdf behavior: (is it consistent?)
#  - first row is beginning balance
#  - second row is ending balance
#  - [-2] is ending balance
#  - [-1] is Standard montly service fee line

df = pd.DataFrame(transactionData)
# show(df)

text = ""
for i in range(len(transactionData['type'])):
    
    temp = f"{transactionData['type'][i]} {transactionData['category'][i]}\n"
    text += temp

create("sample training", transactionData)

# nlp = spacy.load("en_core_web_trf")
# doc = nlp(text)
# displacy.serve(doc, style="ent")

