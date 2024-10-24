
import re
def create(filename: str, data: dict):
    '''Takes a dictionary formatted for a Dataframe in parse_pdf and converts it into a list for training, which is stored in a txt file in /data'''
    with open(f'./data/{filename}.txt', 'w') as file:

        for i in range(len(data["type"])):
            type = data["type"][i]
            cat = data["category"][i] 

            file.write(f"{type} {cat}\n")
            # outputList.append(f"{type} {cat}") # unmatched open bracket? 
        
        

