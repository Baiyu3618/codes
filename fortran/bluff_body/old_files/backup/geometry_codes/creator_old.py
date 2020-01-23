# this is the geometry file creator for bluff body simulation
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from copy import copy as cp

# geometry data for creation
L = 0.5
R1 = 0.01
R2 = 0.5

n1 = 11
n2 = 31
n3 = 21

# # creating lower phase body b1

#nx = 21; ny = 41
h = 0.0; k = -1.2*R2
th1 = np.linspace(np.pi/2,0,n3)
Xp = (R2-R1)*np.cos(th1)
r = np.flip(-(k + np.sqrt((R2-R1)**2-(Xp-h)**2)),axis = 0)

X1,Y1 = np.meshgrid(np.linspace(0,L,n1),-r)
X1 = np.flip(X1,axis=1)  # flipped to match with the final matrix

# creating 2nd body b2
theta,R = np.meshgrid(np.linspace(3*np.pi/2,np.pi/2,n2),r)
X2 = R*np.cos(theta)
Y2 = R*np.sin(theta)

# creating 3rd body b3
X3,Y3 = np.meshgrid(np.linspace(0,L,n1),r)

# mergin all the parts
X = np.concatenate([X1[:,:-1],X2[:,:-1],X3],axis=1)
Y = np.concatenate([Y1[:,:-1],Y2[:,:-1],Y3],axis=1)
ny,nx = X.shape

# nx = n1; ny = n2
# R,theta = np.meshgrid(np.linspace(R2,R1,nx),np.linspace(3*np.pi/2,np.pi/2,ny))
# X = R*np.cos(theta)
# Y = R*np.sin(theta)

# nx = 21; ny = 41
# h = 0.0; k = -1.2*R2
# Xp = np.linspace(0,(R2-R1),nx)
# r = k + np.sqrt((R2-R1)**2-(Xp-h)**2)

# R,theta = np.meshgrid(-r,np.linspace(3*np.pi/2,np.pi/2,ny))
# X = R*np.cos(theta)
# Y = R*np.sin(theta)

# nx = 21; ny = 41                                     # this works <----------------------
# h = 0.0; k = -1.2*R2
# th1 = np.linspace(np.pi/2,0,nx)
# Xp = (R2-R1)*np.cos(th1)
# r = k + np.sqrt((R2-R1)**2-(Xp-h)**2)

# R,theta = np.meshgrid(-r,np.linspace(3*np.pi/2,np.pi/2,ny))
# X = R*np.cos(theta)
# Y = R*np.sin(theta)


# # elliptic grid generation section
# Xprev = cp(X); Yprev = cp(Y)
# dE = 1.0; dN = 1.0

# for iterate in range(1000):

#     for i in range(1,nx-1):
#         for j in range(1,ny-1):
#             # computing coefficients
#             dXe = (X[j,i+1]-X[j,i-1])/dE/2.0
#             dYe = (Y[j,i+1]-Y[j,i-1])/dE/2.0
#             dXn = (X[j+1,i]-X[j-1,i])/dN/2.0
#             dYn = (Y[j+1,i]-Y[j-1,i])/dN/2.0

#             alpha = dXn**2 + dYn**2
#             beta = dXe*dXn + dYe*dYn
#             gamma = dXe**2 + dYe**2

#             # computing X position
#             a = (X[j,i+1]+X[j,i-1])/dE**2
#             b = (X[j+1,i+1]+X[j-1,i-1]-X[j+1,i-1]-X[j-1,i+1])/4/dE/dN
#             c = (X[j+1,i]+X[j-1,i])/dN**2
#             d = (2*alpha/dE**2 + 2*gamma/dN**2)

#             X[j,i] = 1.0/d*(alpha*a-2*beta*b+gamma*c)

#             # computing Y position
#             a = (Y[j,i+1]+Y[j,i-1])/dE**2
#             b = (Y[j+1,i+1]+Y[j-1,i-1]-Y[j+1,i-1]-Y[j-1,i+1])/4/dE/dN
#             c = (Y[j+1,i]+Y[j-1,i])/dN**2
#             d = (2*alpha/dE**2 + 2*gamma/dN**2)

#             Y[j,i] = 1.0/d*(alpha*a-2*beta*b+gamma*c)

#     # checking for convergence
#     convergence_x = np.max(abs(Xprev-X)); Xprev = cp(X)
#     convergence_y = np.max(abs(Yprev-Y)); Yprev = cp(Y)

#     # X[ny-1,:] = cp(X[ny-2,:])
#     # X[0,:] = cp(X[1,:])

#     # Y[ny-1,:] = cp(Y[ny-2,:])
#     # Y[0,:] = cp(Y[1,:])

#     print("Iteration : ",iterate)

#     if convergence_x < 1e-7 and convergence_y < 1e-7:
#         break

# plotting the mesh
plt.figure()
for i in range(nx):
    plt.plot(X[:,i],Y[:,i],'-b')
for j in range(ny):
    plt.plot(X[j,:],Y[j,:],'-b')
plt.axis("image")
plt.show()
