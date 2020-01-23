# this is the python script for plotting the data
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from copy import copy as cp

# reading the data from file
cols=["X","Y","U","V","P"]
fid = pd.read_csv("Data.csv",header=None,skiprows=1,names=cols)

nx = 129; ny = 129

# reconstructing the matrix
X = np.zeros([ny,nx],dtype = float)
Y = cp(X); U = cp(X); V = cp(X); P = cp(X)
count = 0;
for i in range(nx):
    for j in range(ny):
        X[j,i] = fid["X"][count]
        Y[j,i] = fid["Y"][count]
        U[j,i] = fid["U"][count]
        V[j,i] = fid["V"][count]
        P[j,i] = fid["P"][count]
        count += 1

# plotting contours
fig1 = plt.figure()
plt.contourf(X,Y,np.sqrt(U**2+V**2),600,cmap = 'jet')
plt.axis('image'); plt.colorbar()

fig2 = plt.figure()
plt.contourf(X,Y,P,600,cmap = 'jet')
plt.axis('image'); plt.colorbar()

# reading filename
fid = open("fileid.txt","r")
txt = fid.readlines()
pname = "pressure_contour/"+txt[0].strip()+".png"
vname = "velocity_contour/"+txt[0].strip()+".png"

fig1.savefig(vname,dpi=500)
fig2.savefig(pname,dpi=500)

plt.close("all")
