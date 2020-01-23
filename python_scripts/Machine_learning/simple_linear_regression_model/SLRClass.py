################################################################################
# Simple Linear Regression Model of Machine Learning                           #
# with single variable as input and output                                     #
#                                                                              #
# developed by : Ramkumar                                                      #
#                                                                              #
# Note         : Model does not take lists as inputs,                          #
#                only array and dataframe are supported.                       #
#                                                                              #
# details on execution:                                                        #
# 1) import the class module into the workspace from this file                 #
# 2) initialize a class object with training input and output datasets         #
#    example: a = Linear_Regression(Input, Output)                             #
# 3) the model will get trained and outputs the final cost function            #
#    of that dataset, along with the iteration count at which the              #
#    gradient descendant is converged (if it is converged), residual           #
#    of cost function iteration.                                               #
# 4) In case there is no output regarding convergence means, the model         #
#    requires few more iterations to get fit well. it can be arranged with     #
#    Gradient_Descendant function of the model. for example,                   #
#       a.Gradient_Descendant(Iteration Count, learning rate, residual)        #
# 5) In case of divergence error during initialization, the learning rate      #
#    is too high for current dataset, hence it has to be lowered. The          #
#    optimal learning rate can be determined by trial and error. Learning      #
#    rate can be fed to the model by Gradient_Descendant function.             #
# 6) After fitting every thing, the model is ready to predict the output.      #
#    The output can be predicted using predict() function of the class object. #
#    It takes one data as input, that data can be an array or dataframe,       #
#    BUT NOT LIST!!!.                                                          #
################################################################################

import numpy as np
import pandas as pd
from copy import copy as cp

class Linear_Regression(object):
    def __init__(self,X,Y):
        self.X = X              # input
        self.Y = Y              # output
        self.Gradient_Descendant(10000,2.9e-4,1e-6)
    #

    # a function that determines the best slope and intercept
    def Gradient_Descendant(self, itr_count, learning_rate, residual):
        m_curr = b_curr = 0.0                                            # initial values for slope

        cf_prev = 1.2345                                                 # initial cost function value

        for i in range(itr_count):                                       # starting a loop
            y_predicted = m_curr * self.X + b_curr                       # computing predicted values

            n = self.X.shape[0]                                          # no of elements

            cf = 1.0/n*sum(values**2 for values in (y_predicted-self.Y)) # cost function
            
            dm = -2.0/n*sum((self.Y - y_predicted)*self.X)               # slope derivative of cost function

            db = -2.0/n*sum(self.Y - y_predicted)                        # intercept derivative of cost function

            m_curr -= learning_rate*dm                                   # new slope value

            b_curr -= learning_rate*db                                   # new intercept value

            err = abs(cf_prev - cf)                                      # error diff b/w previous and present cost function
            cf_prev = cp(cf)

            if err <residual:
                print("Gradient Descendant \nConverged at : ",i," iteration with residual of : ",residual)
                break
        
        print("Cost Function Value at end of fitting : ",cf)
        print("Error Difference b/w Cost functions of successive iterations : ",err)

        self.slope = m_curr
        self.intercept = b_curr
    #

    # prediction function
    def predict(self,x):
        y_out = self.slope * x + self.intercept
        return y_out

    # accuracy computing function
    def accuracy(self, x, y):
        y_out = self.slope * x + self.intercept

        acc = (1.0-np.mean(abs(y-y_out))/np.mean(y))*100.0

        # print("Accuracy of Model : ",acc," %")
        return acc
    #
#
# End of Model====================================================================================================
