##############################################################
# 1D compressible flow solution using kurganov tadmor scheme #
# developed by Ramkumar                                      #
##############################################################

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from copy import copy as cp

# functions definition section -------------------------------------------------
def encoder(u1,u2,u3,g):
    f1 = cp(u2)
    f2 = (3.0-g)/2.0*u2**2/u1 + (g-1.0)*u3
    f3 = g*U2*U3/U1 - U2**3/U1**2/2.0*(g-1.0)

    return f1,f2,f3

# geometry and meshing section--------------------------------------------------
L  = 1.0; nx = 41       # length and number of nodes

X = np.linspace(0,L,nx) # computing nodal positions
dx = X[1]-X[0]          # space step size
    
# computation parameters section------------------------------------------------
rho0 = 1.5   # inlet density
Mach = 2.0   # inlet mach number
T0   = 500.0 # inlet temperature
g    = 1.4   # ratio of specific heats
R    = 287.0 # gas constant
Time = 0.1   # simulation time

# computation variables section-------------------------------------------------
Uin = Mach*np.sqrt(g*R*T0)      # inlet velocity

rho = np.linspace(rho0,1.0,nx)  # initializing computational values
u = np.linspace(Uin, 0.0, nx)
T = np.linspace(T0, 288.18, nx)

dt = 0.5*dx/Uin                 # computational time step

U1 = cp(rho)                    # building conservational variables
U2 = rho*u
E = R/(g-1)*T + u**2/2
U3 = rho*E

F1,F2,F3 = encoder(U1,U2,U3,g)  # encoding to flux variables

dU11 = np.zeros(nx); dU12 = cp(dU11); dU13 = cp(dU11)
dU21 = np.zeros(nx); dU22 = cp(dU21); dU23 = cp(dU21)
dU31 = np.zeros(nx); dU32 = cp(dU31); dU33 = cp(dU31)
dU41 = np.zeros(nx); dU42 = cp(dU41); dU43 = cp(dU41)
U1b = cp(U1); U2b = cp(U2); U3b = cp(U3)

# solution section--------------------------------------------------------------
t = 0.0                         # initial simulation time
while t <= Time:

    t += dt

    # rk 1 step
    for i in range(1,nx):
        dU11[i] = -(F1[i]-F1[i-1])/dx
        dU12[i] = -(F2[i]-F2[i-1])/dx
        dU13[i] = -(F3[i]-F3[i-1])/dx

    # encoding for second step
    F1,F2,F3 = encoder(U1+dU11/2.0*dt,U2+dU12/2.0*dt,U3+dU13/2.0*dt,g)
    
    # rk 2 step
    for i in range(1,nx):
        dU21[i] = -(F1[i]-F1[i-1])/dx
        dU22[i] = -(F2[i]-F2[i-1])/dx
        dU23[i] = -(F3[i]-F3[i-1])/dx

    # encoding for third step
    F1,F2,F3 = encoder(U1+dU21/2.0*dt,U2+dU22/2.0*dt,U3+dU23/2.0*dt,g)

    # rk 3 step
    for i in range(1,nx):
        dU31[i] = -(F1[i]-F1[i-1])/dx
        dU32[i] = -(F2[i]-F2[i-1])/dx
        dU33[i] = -(F3[i]-F3[i-1])/dx

    # encoding for fourth step
    F1,F2,F3 = encoder(U1+dU31*dt,U2+dU32*dt,U3+dU33*dt,g)

    # rk 4 step
    for i in range(1,nx):
        dU41[i] = -(F1[i]-F1[i-1])/dx
        dU42[i] = -(F2[i]-F2[i-1])/dx
        dU43[i] = -(F3[i]-F3[i-1])/dx
        
    # assembling equation
    U1 = U1 + dt/6.0*(dU11 + 2.0*dU21 + 2.0*dU31 + dU41)
    U2 = U2 + dt/6.0*(dU12 + 2.0*dU22 + 2.0*dU32 + dU42)
    U3 = U3 + dt/6.0*(dU13 + 2.0*dU23 + 2.0*dU33 + dU43)

    # applying boundary conditions
    U1[nx-1] = 2*U1[nx-2] - U1[nx-3]
    U2[nx-1] = 2*U2[nx-2] - U2[nx-3]
    U3[nx-1] = 2*U3[nx-2] - U3[nx-3]

    # encoding to flux variables
    F1,F2,F3 = encoder(U1,U2,U3,g)

    print("Current Time : ",t)

    # check for solution divergence
    if np.isnan(U1).any():
        raise ValueError("Solution Diverged")

# decoding to primitive variables

rho = cp(U1)
u = U2/U1
T = (g-1)/R*(U3/U1 - U2**2/2/U1**2)
