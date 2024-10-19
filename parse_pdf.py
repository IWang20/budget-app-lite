from pypdf import PdfReader
from pathlib import Path
import re
import pandas as pd
from pandasgui import show 


pdf_path = Path("pdfs")

reader = PdfReader("./pdfs/291af904-a0ca-4db0-8cfe-62d97ba2b050.pdf")
pages = reader.pages[1:-2]
temp = ""
print(len(pages))
for page in range(len(pages)):
    # print("Page", page)
    temp += pages[page].extract_text()
    # print()

temp = temp.replace('\n', ' ')

#10/1   Zelle to Kai on 10/01 Ref #Rp0Y42Rgyp     70.00    2,048.54     10/2   Purchase authorized on 09/30 Ara Uci Side Door Irvine CA  S584274682713977 Card 1848     2.99        10/2   Purchase authorized on 09/30 Albertsons #0597 Irvine CA  S304274713914914 Card 1848     36.33    2,009.22     10/7   Purchase authorized on 10/03 Chick-Fil-A #03260  949-725-0230 CA S584277698423686 Card 1848     7.96        10/7   Purchase authorized on 10/04 Target 0003 Irvine CA  S464278690638879 Card 1848     2.78        10/7   Purchase authorized on 10/04 Chipotle 2116 Irvine CA  S304278703835207 Card 1848     10.51        10/7   Purchase authorized on 10/04 Target T-0336 3750 Barran  Irvine CA P464279043496030 Card 1848     51.12        10/7   Purchase authorized on 10/06 Trader Joe S #11 Trader J Irvine  CA P384280777586092 Card 1848     6.85        10/7   Money Transfer authorized on 10/06 Venmo *Noah Wang VISA  Direct NY S384281191311998 Card 1848     21.00    1,909.00    
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
        
        transactionData.get("category").append(splitTrans[3])
        transactionData.get("amount").append(splitTrans[4])
        print(splitTrans)
    else:
        # print("ERROR:", tString) # transactions without date(recurring Transfer) and starting/ending values
        err = re.findall(tPattern2, tString)
        splitTrans = list(err[0])
        splitTrans[1] = splitTrans[1].lstrip()
        splitTrans[1] = splitTrans[1].rstrip()
        print(splitTrans)

# pypdf behavior: (is it consistent?)
#  - first row is beginning balance
#  - second row is ending balance
#  - [-2] is ending balance
#  - [-1] is Standard montly service fee line

df = pd.DataFrame(transactionData)
show(df)

    