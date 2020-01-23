###################################################
# Machine Learning tutorial - Decision tree model #
# source : https://youtube.com/codebasics         #
###################################################

import numpy as np
from sklearn import tree
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

"""
Decision tree is a model that can be used in problems 
where there will be several set of classifications
along with sub-classifications. In this example,
the salary of exmployee is predicted whether greater
than $100k or not, based on the gathered data
For this, the "tree" model under sklearn is 
used.
"""

# reading the dataset
fid = pd.read_csv("data.csv")

# spliting data into inputs and outputs
inputs = fid.drop(["salary"],axis = "columns")
outputs = fid.salary

# encoding labels for inputs since they contain only the text as input
le_company  = LabelEncoder()
le_job = LabelEncoder()
le_degree = LabelEncoder()

inputs["company_n"] = le_company.fit_transform(inputs["company"])
inputs["job_n"] = le_job.fit_transform(inputs["job"])
inputs["degree_n"] = le_degree.fit_transform(inputs["degree"])

"""
Here the label encoding works in such way that it assigns a number  from 0 to
each name in the input data, sorting them in ascending order. 
hence here in company column

ABC Pharma - 0
facebook - 1
google - 2

business manager - 0
computer programmer - 1
sales executive - 2

bachelors - 0
masters - 1

these values are get by sorting them in alphabetical order
"""

# droping the data with alphanumeric characters
inputs_n = inputs.drop(["company","job", "degree"], axis = "columns")

# spliting inputs for testing and training
itrain, itest, otrain, otest = train_test_split(inputs_n, outputs, test_size = 0.2)

# creating and training the model
model = tree.DecisionTreeClassifier()

model.fit(itrain,otrain)        # training

# testing the model with test data and score
print("score of the model : ", model.score(itest,otest))
print("The reason for low score is that it requires simply more data")
