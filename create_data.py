
import re
# add append/write mode
def write_clean_data(filename: str, data: dict):
    '''Takes a dictionary formatted for a Dataframe in parse_pdf and converts it into a list for parsing into a txt for labeling, which is stored in a txt file in /data'''
    with open(f'./data/{filename}.txt', 'a') as file:

        for i in range(len(data["type"])):
            type = data["type"][i]
            cat = data["category"][i] 

            file.write(f"{type} {cat}\n")

# def create_csv(infile: str, outfile: str):
#     '''Takes a set of labeled text and turns it into a csv'''
#     with open(f'./data/{outfile}.csv', 'a') as outfile, open(f'./data/{infile}.txt', 'r') as infile:

#         for i in range(len(data["type"])):
#             labeled_lines = infile.readlines()
#             for line in labeled_lines:
#                 label, text = re.findall("__(.?*)__(.?*)")
#             outfile.write(f"{type} {cat}\n")
            # outputList.append(f"{type} {cat}") # unmatched open bracket? 