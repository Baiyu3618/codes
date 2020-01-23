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
        self.IT = 200000        # max iteration count
        self.Re = 1e-6          # min residual value
    #

    def step_gd(self,m1,m2,m3,b):
        # predicting the values using given m and b
        y_predict = m1*self.X**3 + m2*self.X**2 + m3*self.X + b

        # computing cost function
        tmp = (y_predict - self.Y)
        CF = sum(tmp**2)/len(tmp)  # computing mean value

        dm1 = 2.0/len(tmp) * sum(tmp*self.X**3)
        dm2 = 2.0/len(tmp) * sum(tmp*self.X**2)
        dm3 = 2.0/len(tmp) * sum(tmp*self.X)
        db  = 2.0/len(tmp) * sum(tmp)

        m1,m2,m3,b = m1 - self.LR*dm1, m2 - self.LR*dm2, m3 - self.LR*dm3, b - self.LR*db

        return m1,m2,m3,b
    #

    def gd_runner(self):
        m1 = m2 = m3 = b = 0               # initial slope and intercept values

        for i in range(self.IT):
            m1p,m2p,m3p,bp = self.step_gd(m1,m2,m3,b)

            convergence = max([abs(m1p - m1), abs(m2p - m2), abs(m3p - m3), abs(bp - b)])
            m1 = cp(m1p); m2 = cp(m2p); m3 = cp(m3p); b = cp(bp)

            print ("Iteration : ",i," convergence : ",convergence)

            if convergence < self.Re:
                print("converged with m1 = ",m1," m2 = ",m2," m3 = ",m3, " and b = ",b)
                break
            #
        self.m1 = m1
        self.m2 = m2
        self.m3 = m3
        self.b = b
    #
