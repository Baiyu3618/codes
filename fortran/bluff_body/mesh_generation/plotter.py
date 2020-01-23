##################################################################
# plotter function written in python for bluff body aerodynamics #
# developed by Ramkumar                                          #
##################################################################
import matplotlib.pyplot as plt
import numpy as np

fid = open("grid.grd","r")

# reading number of elements
tmp = fid.readline().split(",")
nx = int(float(tmp[0].split()[0]))
ny = int(float(tmp[1].split()[0]))

# declaration of array and reading data from file
X, Y = np.zeros([ny,nx]), np.zeros([ny,nx])

for i in range(nx):
    for j in range(ny):
        tmp = fid.readline().split(",")
        X[j,i] = float(tmp[0].split()[0])
        Y[j,i] = float(tmp[1].split()[0])
#

# plotting the mesh
plt.close("all")
plt.figure()
for i in range(nx):
    plt.plot(X[:,i],Y[:,i],'-k')
#
for j in range(ny):
    plt.plot(X[j,:],Y[j,:],'-k')
#
plt.axis("image")
plt.show()
