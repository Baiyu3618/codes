################################################################
# This is an exercise program that is for decision tree method #
# developed by ramkumar for problem 7                          #
################################################################
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn import tree
from sklearn.model_selection import train_test_split

""" 
for this exercise, the data from titanic have been given.
out of all the columns, the effective columns are
output  - Survived
input - Pclass, Sex, Age, Fare
"""

# reading the data from file
fid = pd.read_csv("exercise_data.csv")

# spliting data into inputs and outputs
inputs = fid[["Pclass","Sex","Age","Fare"]]
outputs = fid.Survived

# filling the missing data with median on the columns of Age
inputs["Age"] = inputs.Age.fillna(int(inputs["Age"].median()))

# encoding labels for sex column
Sex_le = LabelEncoder()
inputs["Sex_n"] = Sex_le.fit_transform(inputs["Sex"])
"""
 Here the encoding is again done based on Alphabetcial order
hence Male = 1; Female = 0
"""

# appending to final inputs_n
inputs_n = inputs.drop(["Sex"], axis ="columns")

# spliting the data into testing and training
itrain,itest,otrain,otest = train_test_split(inputs_n,outputs, test_size = 0.2)

# creating and training the model
model = tree.DecisionTreeClassifier()
model.fit(itrain, otrain)

# checking the test score
print("\n\n\nModel Accuracy : ",model.score(itest,otest)*100.0," %")
