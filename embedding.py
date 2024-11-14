import fasttext
import numpy as np
from typing import List, Union
import os
import matplotlib as plt
from sklearn.model_selection import train_test_split
import re

"""
    Pull from the training data and split it into train/test splits
"""
# def split(labeled_data: str)
def split():
    with open (f'./data/sample_data_labeled.txt', 'r') as data_text, open('./data/sample_training.txt', 'w') as train_file, open('./data/sample_test.txt', 'w') as test_file:
        data = data_text.readlines()
        train_data, test_data = train_test_split(data, test_size=0.2, random_state=100)
        train_file.writelines(train_data)
        test_file.writelines(test_data)

"""
    take a labeled set and a model and makes predictions to see if they are correct 
"""
def test(testFile: str, model):
    
    with open(f'{testFile}') as file:
        data = file.readlines()
        correct = 0
        total = len(data)
        accuracy = 0
        for transaction_text in data:
            groups = re.findall(r"__label__(.*?) ([a-zA-z ]+)", transaction_text)[0]
            # print(groups)
            actual_label = groups[0]
            predicted_label, probability = model.predict(groups[1], k=3)
            
            predicted_label = re.sub("__label__", "", predicted_label[0])
            if predicted_label == actual_label:
                correct += 1
            else:
                print(f"Incorrect prediction {predicted_label} != {actual_label} in {groups[1]}")
        accuracy = correct / total
        print(f"{testFile} accuracy is {accuracy}!! Cogrants :3")


            


def main():
    # split()
    # model = fasttext.train_supervised(input='./data/sample_training.txt',
    #                                 epoch=100, 
    #                                 lr=0.1, 
    #                                 wordNgrams=3, 
    #                                 verbose=2, 
    #                                 minCount=1,
    #                                 dim = 300,
    #                                 neg = 10,
    #                                 ws = 5,
    #                                 loss='softmax',
    #                                 pretrainedVectors='./data/wiki-news-300d-1M.vec/wiki-news-300d-1M.vec')
    # model.save_model('./models/budget-0.bin')
    model = fasttext.load_model("./models/budget-0.bin")

    test("./data/sample_test.txt", model)
    # label, probability = model.predict("Purchase NyxCanteen Portla Tigard OR ", k=3)
    # print(label, probability)
    # model.

# categories 
# rent, resturants, groceries, shopping, travel, deposit, personal 
if __name__ == "__main__":
    main()

