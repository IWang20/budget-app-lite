# budget-app-lite
local full-stack application that categorizes purchases from bank statements (only Wells Fargo for now) and stores them for basic spending analysis 

# installing and running fasttext (windows)
* unable to build on windows, run on linux vm or wsl2 instead
* use python3 -m pip install fasttext
* you might need to pip install fasttext-wheel

# notes on the model
* fasttext doesn't consider "Wendy's" to be a restaurant/fast food it thinks its a person and I don't know how to fix it lol
* has high variance (repeats in training data, poor validation accuracy)

# how to run
* import modules in requirements
* make sure mysql is running
* put the billing statements (.pdf) in /pdfs
* run start.py with your mysql credentials