import fasttext
from fasttext.FastText import _FastText
import numpy as np
import os
import matplotlib as plt
from sklearn.model_selection import train_test_split
import re
import math


# def split(labeled_data: str)
def split(inFile: str, trainFile: str, testFile: str):
    """
        split inFile into two files for testing and training 
    """
    with open (f'./data/{inFile}', 'r') as data_text, open(f'./data/{trainFile}', 'w') as train_file, open(f'./data/{testFile}', 'w') as test_file:
        data = data_text.readlines()
        train_data, test_data = train_test_split(data, test_size=0.2, random_state=100)
        train_file.writelines(train_data)
        test_file.writelines(test_data)


def test_pred(testFile: str, model):
    """
        take a labeled file and a model, checks predictions to see if they are correct 
    """
    with open(f'./data/{testFile}') as file:
        data = file.readlines()
        correct = 0
        total = len(data)
        accuracy = 0
        for transaction_text in data:
            groups = re.findall(r"__label__(.*?) (.*?)\n", transaction_text)[0]
            # print(groups)
            actual_label = groups[0]
            labels, probability = model.predict(groups[1], k=3)

            predicted_label = labels[0]
            
            predicted_label = re.sub("__label__", "", predicted_label)
            if predicted_label == actual_label:
                correct += 1
            else:
                prob_format = [f"{i:.9f}" for i in probability]
                print(f"Incorrect prediction {predicted_label} != {actual_label} in | {groups} | prediction: {prob_format}")
        accuracy = correct / total
        print(f"{testFile} accuracy is {accuracy}!! Congrats :3")


def train(inStr: str, outStr: str):
    model = fasttext.train_supervised(input=f'./data/{inStr}',
                                    epoch=100, 
                                    lr=0.1, 
                                    wordNgrams=3, 
                                    verbose=2, 
                                    minCount=1,
                                    dim=300,
                                    neg=10,
                                    ws=5,
                                    loss='softmax',
                                    pretrainedVectors='./data/wiki-news-300d-1M.vec')
    model.save_model(f'./models/{outStr}')
    
    return model

def load_model(model_name: str):
    """
        takes file name of model stored at ./models
    """
    return fasttext.load_model(f"./models/{model_name}")

def categorize(data: str, model: _FastText):
    """
        categorizes a string and returns the label it is most likely to be assigned
    """
    probabilities = model.predict(data)
    return probabilities

def write_data(inFile: str, transactions):
    """
        takes transactions and writes to ./data
    """
    print(f"Writing '{inFile}', Adding {len(transactions)} items")
    with open(f"./data/{inFile}", "w") as dataFile:
        for transaction in transactions:
            dataFile.write(transaction + "\n")


def main():
    pass

    # test("./data/sample_training.txt", model)
    # label, probability = model.predict("Purchase NyxCanteen Portla Tigard OR ", k=3)
    # print(label, probability)
    # model.

# categories 
# rent, resturants, groceries, shopping, travel, deposit, personal 
if __name__ == "__main__":
    main()

