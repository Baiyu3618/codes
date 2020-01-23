#################################################################
# single linear regression problem example fro youtube tutorial #
# on channel youtube.com/codebasics/MachineLearning             #
#                                                               #
# developed by ramkumar                                         #
#################################################################

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model

# in this script, the 'per-capita income' of US for past several
# years are taken as data input and it is required to predict
# the income for the year 2020

# reading the data from csv file
fid = pd.read_csv("test_data.csv")

# creating a regression object
reg = linear_model.LinearRegression()

# fitting the data to the object, i.e training the object with existing data
reg.fit(fid[["year"]],fid.PCI)

# predicting the value of PCI for the year 2020
value = reg.predict(2020)

print("The Per-capita income for the year 2020  is : ",value)

# plotting the data values and linear regression graph
plt.figure()
plt.scatter(fid["year"], fid["PCI"], marker = '*', color = 'red', label = "data values")
plt.plot(fid["year"], reg.coef_ * fid["year"] + reg.intercept_,'-b', label = "linear regression")
plt.plot(2020, value, 'ok', markerfacecolor="k", label = "predicted value")
plt.xlabel("year")
plt.ylabel("PCI")
plt.legend()
plt.savefig("output.png", dpi = 300)
plt.show()
