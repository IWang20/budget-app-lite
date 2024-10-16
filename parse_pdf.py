from pypdf import PdfReader
from pathlib import Path
import re


pdf_path = Path("pdfs")

reader = PdfReader("./pdfs/291af904-a0ca-4db0-8cfe-62d97ba2b050.pdf")
pages = reader.pages[1:-2]
temp = ""
for page in range(2):
    # print("Page", page)
    temp = pages[page].extract_text()
    # print()

temp = temp.replace('\n', ' ')
# print(temp)
# \d{1,2}\/\d{1,2}[a-zA-z ]+(\d{2}\/\d{2})?.*?Card 1848[ ]+\d{1,}.\d{2}
# https://regex101.com/r/4Mwt3g/1
pattern = r"\d{1,2}\/\d{1,2}([a-zA-z ]+)(?:\d{2}\/\d{2})?.*?((?:Card 1848)?\d{1,}.\d{2})"
transactions = re.finditer(pattern, temp)

for transaction in transactions:
    print(transaction.group())