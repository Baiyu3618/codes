# multi class logic regression concept
import pandas as pd
from sklearn import datasets
from sklearn import linear_model
from sklearn.model_selection import train_test_split

"""
multi class regression is nothing, the output is classified into more than
two options. Example, instead of returning yes or no, it can return the 
names of objects it recognize.

sklearn has built-in datasets for many similar applications, one such dataset is 
taken for current problem. The handwriting recognitiion of numbers 0 to 9.
it is there in the 'load_digits' class under sklearn.datasets
"""

# loading datasets
digits = datasets.load_digits()
# this dataset basically contains all the necessary things, but we are
# going to use only 'data' and 'target'. data is the image data and target
# is the actual number which 'data' corresponds to
# here the images are in 8X8 pixels, i.e. a single array with 64 values
# for each image

# getting the inputs and outputs
X = digits.data
Y = digits.target

# spliting the data into test and training
Xtrain, Xtest, Ytrain, Ytest = train_test_split(X,Y,test_size=0.2)

# creating the model
model = linear_model.LogisticRegression()

# training the model
model.fit(Xtrain,Ytrain)

# testing
y_predicted = model.predict(Xtest)

# score
print("Accuracy of Model is  : ", model.score(Xtest,Ytest)*100.0," %")
