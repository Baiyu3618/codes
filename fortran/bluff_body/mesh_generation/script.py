##################################################################
# Geometry and Mesh generator for bluff-body aerodynamics script #
# developed by Ramkumar                                          #
##################################################################

import numpy as np
import matplotlib.pyplot as plt
from copy import copy as cp

# functions for computation-----------------------------------------------------
def compute_alpha(i,j):
    a = (X[j+1,i] - X[j-1,i])/dN/2.0
    b = (Y[j+1,i] - Y[j-1,i])/dN/2.0

    return a**2 + b**2

def compute_beta(i,j):
    a = (X[j+1,i] - X[j-1,i])/dN/2.0
    b = (X[j,i+1] - X[j,i-1])/dE/2.0
    c = (Y[j+1,i] - Y[j-1,i])/dN/2.0
    d = (Y[j,i+1] - Y[j,i-1])/dE/2.0

    return a*b + c*d

def compute_gamma(i,j):
    a = (X[j,i+1] - X[j,i-1])/dE/2.0
    b = (Y[j,i+1] - Y[j,i-1])/dE/2.0

    return a**2 + b**2

def compute_X(alpha,beta,gamma,i,j):
    q = 2.0*(alpha/dE**2 + gamma/dN**2)
    a = alpha*(X[j,i+1] + X[j,i-1])/dE**2
    b = 2.0*beta*(X[j+1,i+1] + X[j-1,i-1] - X[j-1,i+1] - X[j+1,i-1])/4.0/dE/dN
    c = gamma*(X[j+1,i] + X[j-1,i])/dN**2

    return 1/q * (a - b + c)

def compute_Y(alpha,beta,gamma,i,j):
    q = 2.0*(alpha/dE**2 + gamma/dN**2)
    a = alpha*(Y[j,i+1] + Y[j,i-1])/dE**2
    b = 2.0*beta*(Y[j+1,i+1] + Y[j-1,i-1] - Y[j-1,i+1] - Y[j+1,i-1])/4.0/dE/dN
    c = gamma*(Y[j+1,i] + Y[j-1,i])/dN**2

    return 1/q * (a - b + c)

# bluff body description--------------------------------------------------------
# bluff body chosen as ellipse
a1 = 0.1                        # semi major and semi minor axis definitions
b1 = 0.05
a2 = 0.5
b2 = 0.25

nx = 101                        # actually nr - radial no of elements
ny = 101                        # actually nt - angular no of elements

# initial mesh generation-------------------------------------------------------
a,b = np.linspace(a2,a1,nx), np.linspace(b2,b1,nx)
t = np.linspace(-np.pi/2.0,np.pi/2.0,ny)

X = np.zeros([ny,nx]); Y = cp(X)

for i in range(nx):
    for j in range(ny):
        X[j,i] = -a[i]*np.cos(t[j])
        Y[j,i] =  b[i]*np.sin(t[j])
#

# elliptic grid generation------------------------------------------------------
dE = 1.0
dN = 1.0

for itr in range(1000):
    Xprev = cp(X); Yprev = cp(Y)
    
    for i in range(1,nx-1):
        for j in range(1,ny-1):
            a = compute_alpha(i,j)
            b = compute_beta(i,j)
            c = compute_gamma(i,j)

            X[j,i] = compute_X(a,b,c,i,j)
            Y[j,i] = compute_Y(a,b,c,i,j)
    #

    convergence = np.max(abs(Xprev - X))

    print("Iteration : ",itr+1," Convergence : ",convergence)

    if convergence < 1e-7:
        print("converged!")
        break
#

# plotting mesh-----------------------------------------------------------------
plt.close("all")
plt.figure()
for i in range(nx):
    plt.plot(X[:,i],Y[:,i],'-k')
for j in range(ny):
    plt.plot(X[j,:],Y[j,:],'-k')
plt.axis("image")
plt.show()
