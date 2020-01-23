# Binary Logistic regression model in machine learning
import numpy as np
import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

"""
There are certain cases in which the output needs to be either yes or no.
Those cases are called binary logic, hence they can be solved using LogisticRegression()
function under linear_model

The sample data is taken from a site called kaggle.com

https://www.kaggle.com/azeembootwala/titanic


There is another option under sklearn module
sklearn.model_selection.train_test_split

this function splits the given data into two sets, testing and for training, based on an user
given fraction.

"""

# reading the dataset
fid = pd.read_csv("data.csv")

# bar chart showing impact of salaries on retention
pd.crosstab(fid["salary"],fid["left"]).plot(kind="bar")
plt.savefig("salary_vs_retention.png", dpi = 300)

# bar chart showing impact of department on retention
pd.crosstab(fid["Department"],fid["left"]).plot(kind="bar")
plt.savefig("department_vs_retention.png", dpi = 300)
plt.close("all")

# creatig input and output datasets
X = pd.concat([fid["satisfaction_level"],fid["average_montly_hours"],fid["promotion_last_5years"],fid["salary"]], axis="columns")
# here , these data columns are chosen by checking its impact on retention, i.e. by checking their respective
# graphs on retention. Bar graphs
Y = fid.left

# creating dummy variables for string inputs at salary column
dummy1 = pd.get_dummies(X["salary"])
X = pd.concat([X,dummy1], axis="columns")
X = X.drop(["salary","medium"], axis="columns")

# spliting the data into test and training
Xtrain,Xtest,Ytrain,Ytest = train_test_split(X,Y,train_size = 0.8,test_size=0.2)

# creating a model
model = linear_model.LogisticRegression()

# training model
model.fit(Xtrain,Ytrain)

# testing model
y_predicted = model.predict(Xtest)

# checking model accuracy
print("Model accuracy : ",model.score(Xtest,Ytest)*100.0," %")
