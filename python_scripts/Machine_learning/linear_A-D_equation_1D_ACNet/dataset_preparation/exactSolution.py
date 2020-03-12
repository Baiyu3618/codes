#####################################################
# dataset maker for 1d advection-diffusion equation #
#####################################################

import numpy as np
import matplotlib.pyplot as plt

# function definition to solve exact solution
def exactSolution(x,t,a,nu,U,w):
    l1 = (a + np.sqrt(a**2 + 4*nu*w*1j))/2.0/nu

    l2 = (a - np.sqrt(a**2 + 4*nu*w*1j))/2.0/nu

    u = np.real((np.exp(l1*x) - np.exp(l2*x))*U*np.exp(1j*w*t)/(np.exp(l1) - np.exp(l2)))

    return u

# definitions
n = 21
nt = 1001
Time = 200.0
length = 1.0
a = 0.1
nu = 0.01
U = 0.1
w = 1.0

x = np.linspace(0,length,n)
t = np.linspace(0,Time,1001)

plt.figure()

for i in t:
    u = exactSolution(x,i,a,nu,U,w)

    plt.clf()
    plt.plot(x,u,'-k')
    plt.title(i)
    plt.pause(0.5)
