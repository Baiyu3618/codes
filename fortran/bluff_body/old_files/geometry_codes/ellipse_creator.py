 # this is the ellipse bluff body grid generator script
# developed by ramkumar

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from copy import copy as cp

# geometric parameters
a1 = 0.2
b1 = 0.1

a2 = 1.0
b2 = 0.5

nx = 101
ny = 51

theta1 = 3*np.pi/2.0
theta2 = np.pi/2.0

# computing the mesh grid

# computing eccentricity for each ellipse
e1 = np.sqrt(1.0 - b1**2/a1**2)
e2 = np.sqrt(1.0 - b2**2/a2**2)

# computing linear theta variations
theta = np.linspace(theta1,theta2,ny)
r1 = b1/np.sqrt(1.0 - (e1*np.cos(theta))**2)
r2 = b2/np.sqrt(1.0 - (e2*np.cos(theta))**2)

Theta = np.zeros([ny,nx], dtype = float); R = cp(Theta)
for j in range(ny):
    Theta[j,:] = cp(theta)
    R[j,:] = np.linspace(r2[j],r1[j],nx)
# b = np.linspace(b2,b1,nx)
# e = np.linspace(e2,e1,nx)
# Theta = np.zeros([ny,nx], dtype = float); R = cp(Theta)
# for i in range(nx):
#     Theta[:,i] = cp(theta)
#     R[:,i] = b[i]/np.sqrt(1.0 - (e[i]*np.cos(theta))**2)
Theta = np.transpose(Theta)
X = R*np.cos(Theta)
Y = R*np.sin(Theta)

# plotting the mesh
plt.figure()
for i in range(nx):
    plt.plot(X[:,i],Y[:,i],'-b')
for j in range(ny):
    plt.plot(X[j,:],Y[j,:],'-b')
plt.axis("image")
plt.show()


