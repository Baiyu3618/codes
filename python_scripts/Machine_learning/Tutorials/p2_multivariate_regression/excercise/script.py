########################################################################
# this is an excercise script for multivariate linear regression model #
# developed by ramkumar                                                #
########################################################################

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model
import math

# reading the data from file
fid = pd.read_csv("test_data.csv")

# filling nan values with medians for test_score
fid.test_score = fid.test_score.fillna(math.floor(fid.test_score.mean()))

# filling nan values with 0 for experience column
fid.experience = fid.experience.fillna(0)

# in the present problem, it is required to compute the salary
# based on experience, test and interview score

reg = linear_model.LinearRegression() # creating class model
reg.fit(fid[["experience","test_score","interview_score"]],fid.salary)

# computing the salary for 2 candidates
c1 = reg.predict([[2,9,6]])
c2 = reg.predict([[12,10,10]])

# output
print("salaries of two candidates are ",c1," & ",c2," respectively")
print(fid)
