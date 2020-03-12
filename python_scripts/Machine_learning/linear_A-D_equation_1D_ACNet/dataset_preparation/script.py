#####################################################
# dataset maker for 1d advection-diffusion equation #
#####################################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from copy import copy as cp

# simulation parameters definition
n = 51
a = 0.5
nu = 0.1
length = 1.0
Time = 10.0
dt = 1e-3

# initial conditions
U = np.zeros(n); U[0] = 1.0
Unew = cp(U)
dx = length/float(n-1)
X = np.linspace(0,length,n)

# creating lists
Uin = []; Uout = []

# matrix formation
mat = np.zeros([n-2,n])

A = -a/2.0/dx - nu/dx**2
B = -1/dt + 2.0*nu/dx**2
C = a/2.0/dx - nu/dx**2

for i in range(n-2):
    mat[i,i] = cp(A)
    mat[i,i+1] = cp(B)
    mat[i,i+2] = cp(C)

# solving the governing equation
nTimes = int(Time/dt)

# plt.figure()

for itr in range(nTimes):
    Utemp = -1*np.matmul(mat,U)*dt
    Unew[1:-1] = cp(Utemp)
    Unew[-1] = 2.0*Unew[-2] - Unew[-3]

    error = np.sqrt(np.mean((Unew - U)**2))

    Uin.append(U)
    # Uout.append(Unew)

    U = cp(Unew)
    Uout.append(U)

    print("Iteration : ",itr," Error : ", error)
    # plt.clf()
    # plt.plot(X,U,'-k')
    # plt.axis([0,1,0,1.5])
    # plt.pause(0.01)

# preparing and writing dataFrames
fid_Uin = pd.DataFrame(Uin)
fid_Uout = pd.DataFrame(Uout)

fid_Uin.to_csv("X.csv", index = None, header = None)
fid_Uout.to_csv("Y.csv", index = None, header = None)

print("dataset writen .. ")
