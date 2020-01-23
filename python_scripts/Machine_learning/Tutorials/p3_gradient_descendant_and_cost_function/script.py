####################################################################
# Gradient descendant and cost fuction concept in Machine learning #
#                                                                  #
# developed by ramkumar                                            #
####################################################################

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model

""" Gradient Descendant: it is an efficient method in determining the 
linear equation coefficients from set of input and output values.

Input and output values will be given, but we have to do reverse
calculation and find slopes & intercepts of best fit line

cost function is nothing but the comparison function that compares 
the predicted output values with the provided output values.
"""

"""
Its algorithm is as follows:
1) start with m = b = 0 and fix learning_rate and no of iterations
2) start a loop
3) compute y_predicted using initial m and b values with given input values
4) compute cost function to check for error difference b/w predicted and given output values
5) compute derivative of cost_function w.r.t. m abd b
6) compute m and b from that learning_rate equation
7) repeat the process from 3) till cost function is below the convergence 
"""

def Gradient_Descendant(x,y):
    m_curr = b_curr = 0.0

    iterations = 100000
    learning_rate = 0.00018

    for i in range(iterations):
        y_predicted = m_curr * x + b_curr

        n = x.shape[0]
        cost = 1/n*sum(values**2 for values in (y_predicted-y))

        md = 2.0/n*sum(-x*(y - y_predicted))
        bd = 2.0/n*sum(-(y - y_predicted))

        m_curr = m_curr - learning_rate*md
        b_curr = b_curr - learning_rate*bd

        print("m = {} ; b = {} ; cost = {} ; iteration = {} ;".format(m_curr,b_curr,cost,i))
    #
    return m_curr, b_curr


# sample data

fid = pd.read_csv("data.csv")

Mc, Bc = Gradient_Descendant(fid["math"],fid["cs"]) # manual computation

reg = linear_model.LinearRegression()
reg.fit(fid[["math"]],fid.cs)   # computation using module

print("\n\n\nManual Computation Results: m = {}, b = {}; \nNumpy results: m = {}, b = {}".format(Mc,Bc,reg.coef_,reg.intercept_))

# plotting graph
plt.figure()
plt.plot(fid["math"],fid["cs"],'ok', label="given raw data")
plt.plot(fid["math"],reg.coef_*fid["math"]+reg.intercept_, label="Numpy approximation")
plt.plot(fid["math"],Mc*fid["math"]+Bc, label="Manual approximation")
plt.legend()
plt.xlabel("Maths")
plt.ylabel("Computer Science")
plt.title("Subject Marks")
plt.savefig("output.png", dpi =300)
plt.show()
