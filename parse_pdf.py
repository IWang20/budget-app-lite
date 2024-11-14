from pypdf import PdfReader
from pathlib import Path
import re
from pandasgui import show 
from create_data import write_clean_data

import os

directory_path = './pdfs'

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

for filename in os.listdir(directory_path):
    file_path = os.path.join(directory_path, filename)


    reader = PdfReader(file_path)
    print("reading", file_path)
    pages = reader.pages[1:-2]
    temp = ""
    # print(len(pages))
    for page in range(len(pages)):
        # print("Page", page)
        temp += pages[page].extract_text()
        # print()

    temp = temp.replace('\n', ' ')

    pattern = r"(Beginning balance on )?(\d{1,2}\/\d{1,2})(.*?)(\d{1,2}\/\d{1,2})?(.*?)(\d{1,}\.\d{2})"
    transactions = re.finditer(pattern, temp)



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
            pass
            ### CLEAN THIS!
            # err = re.findall(tPattern2, tString)
            # print(tString, err)
            # splitTrans = list(err[0])
            # splitTrans[1] = splitTrans[1].lstrip()
            # splitTrans[1] = splitTrans[1].rstrip()
            

            # # transactionData.get("type").
            # if "Recurring Transfer" in splitTrans[1]:
            #     reccurPattern = r"(Recurring Transfer From .*?)(Ref.*?#\w+\s+)(.*)"
            #     clean = re.findall(reccurPattern, splitTrans[1])[0]
                
            #     print(clean)
            #     transactionData.get("date").append(splitTrans[0])
            #     transactionData.get("type").append(clean[0])
            #     transactionData.get("category").append(clean[2])
            #     transactionData.get("amount").append(splitTrans[2])
            # print(splitTrans)

    # pypdf behavior: (is it consistent?)
    #  - first row is beginning balance
    #  - second row is ending balance
    #  - [-2] is ending balance
    #  - [-1] is Standard montly service fee line


    """
        1. Put it in a data frame for viewing
        2. Write cleaned data to a file 
        3. Label it all (somehow)
        4. train/test split it 
        5. train it/test it
    """

    # df = pd.DataFrame(transactionData)
    # show(df)

    text = ""
    for i in range(len(transactionData['type'])):
        
        temp = f"{transactionData['type'][i]} {transactionData['category'][i]}\n"
        text += temp

    # clean the text
    write_clean_data("sample data", transactionData)
    # label the text
    # pass it into create_csv() for organization 
    # create_csv("sample training", "sample_training_labeled")