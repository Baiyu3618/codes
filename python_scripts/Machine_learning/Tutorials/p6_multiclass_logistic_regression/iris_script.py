# this is another script using different dataset and problem
# for multi-catogorial logistci regression
import pandas as pd
import sklearn.linear_model as linear_model
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

"""
This is similar to that of the other script in the same directory
except the fact that, the problem defined in this script
is to classify the iris flowers in 3 different categories 
using its petal and sepal dimensions
"""

data = load_iris()

# getting input and output data
X = data.data                   # it is a 1d array collections, of order [sepal length, sepal width, petal length, petal width]
Y = data.target                 # it is a repetition of numbers 0,1,2 which corresponds to 'setosa', 'versicolor', 'virginica' respectively

# spliting the data for training and testing
Xtrain, Xtest, Ytrain, Ytest = train_test_split(X,Y, test_size=0.2)

# creating the model
model = linear_model.LogisticRegression()

# training the model
model.fit(Xtrain,Ytrain)

# testing the model
y_predicted = model.predict(Xtest)

# creating confusion matrix
cm = confusion_matrix(Ytest,y_predicted)
# confusion matrix is a diagonal matrix that shows number of tests have passed successfully and those which predicted wrongly

# score
print("Accuracy : ",model.score(Xtest,Ytest)*100.0," %")
