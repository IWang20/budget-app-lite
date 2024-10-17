from pypdf import PdfReader
from pathlib import Path
import re


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

pattern = r"(Beginning balance on )?(\d{1,2}\/\d{1,2})(.*?)(\d{1,2}\/\d{1,2})?(.*?)(\d{1,}\.\d{2})"
transactions = re.finditer(pattern, temp)

for transaction in transactions:
    print(transaction.group())
    