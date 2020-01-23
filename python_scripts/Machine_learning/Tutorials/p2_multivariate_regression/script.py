#########################################################################
# Multivariate regression                                               #
# This concept is similar to that of previous single linear regression, #
# except that now there are multiple independent variables.             #
#                                                                       #
# developed by Ramkumar                                                 #
#                                                                       #
# https:/youtube.com/codebasics - machine learning tuturoials           #
#########################################################################

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model
import math

""" In this tutorial, the example of multiple variables linear regression is given,
here, the similar example of previous tutorial, price of home, is chosen but with
additional variables as age of home and number of bedrooms. """

""" MAIN_RULE:  one of the main rules, is that the data which is fed for machine
to learn should be full!!! without any missing data. 
the present data is taken in such a way that it has a missing data and how to deal
with it is given in the tutorial"""

"""
independent variables a.k.a features
if the problem appears to be linear, then only the linear regression model is 
applicable """

# reading the original given data
fid = pd.read_csv("data_original.csv")

""" here a data will be missing in the no of bedrooms column, 
in order to tackle that, computing a median with rest of values and placing it in 
the missing position will solve the issue"""

# computing median of bedrooms
median_bedrooms = math.floor(fid.rooms.median())

# filling the gaps with median value
fid.rooms = fid.rooms.fillna(median_bedrooms)

""" Now once the data is processed, next is to create class objects for linear regression and proceeed"""

reg = linear_model.LinearRegression() # creating a class object

# fitting the training data to the model
reg.fit(fid[['area','rooms','age']],fid.price) # note the syntax between features and dependant variable [[]]

""" in this problem, there are 3 coefficients, since, there are 3 features that define the problem. 
so the governing equation would look like this, y = m1*x1 + m2*x2 + m3*x3 + b"""

# now predicting the price of home with 3000 sqft, 3 rooms, and 40 age
price1 = reg.predict([[3000, 3, 40]])

# now predicting the price of home with 2500 sqft, 4 rooms, and 5 age
price2 = reg.predict([[2500, 4, 5]])

print("Price of Home 1 : ", price1, "\nPrice of Home 2 : ",price2)
