#########################################################
# This is the class file for cubic fit regression model #
# It can be imported and used to generate cubic fit     #
# for the series of input and output data generated     #
#########################################################
import numpy as np
from copy import copy as cp

class CubicRegression(object):
    def __init__(self,X,Y):
        self.X = X              # x values
        self.Y = Y              # y values
        self.LR = 1e-1          # learning rate
        self.IT = 1000          # max iteration count
        self.Re = 1e-6          # min residual value
    #

    def step_gd(self,m,b):
        # predicting the values using given m and b
        y_predict = m*self.X + b

        # computing cost function
        tmp = (y_predict - self.Y)
        CF = sum(tmp**2)/len(tmp)  # computing mean value

        dm = 2.0/len(tmp) * sum(tmp*self.X)
        db = 2.0/len(tmp) * sum(tmp)

        m,b = m - self.LR*dm, b - self.LR*db

        return m,b
    #

    def gd_runner(self):
        m = b = 0               # initial slope and intercept values

        for i in range(self.IT):
            mp,bp = self.step_gd(m,b)

            convergence = max([abs(mp - m) ,abs(bp - b)])
            m = cp(mp); b = cp(bp)

            print ("Iteration : ",i," convergence : ",convergence)

            if convergence < self.Re:
                print("converged with m = ",m, " and b = ",b)
                break
            #
        self.m = m
        self.b = b
    #
