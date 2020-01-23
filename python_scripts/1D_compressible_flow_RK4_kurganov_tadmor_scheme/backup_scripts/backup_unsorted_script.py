
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from copy import copy as cp
import solver_core as sc

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
Time = 0.005   # simulation time

# computation variables section-------------------------------------------------
Uin = Mach*np.sqrt(g*R*T0)      # inlet velocity

rho = np.linspace(rho0,0.5*rho0,nx)  # initializing computational values
u = np.linspace(Uin, 0.5*Uin, nx)
T = np.linspace(T0, 0.5*T0, nx)

dt = 0.05*dx/Uin                 # computational time step, 0.05 to prevent overflow

U1 = cp(rho)                    # building conservational variables
U2 = rho*u
E = R/(g-1)*T + u**2/2
U3 = rho*E

F1,F2,F3 = sc.encoder(U1,U2,U3,g)  # encoding to flux variables

dU11 = np.zeros(nx); dU12 = cp(dU11); dU13 = cp(dU11)
dU21 = np.zeros(nx); dU22 = cp(dU21); dU23 = cp(dU21)
dU31 = np.zeros(nx); dU32 = cp(dU31); dU33 = cp(dU31)
dU41 = np.zeros(nx); dU42 = cp(dU41); dU43 = cp(dU41)
U1b = cp(U1); U2b = cp(U2); U3b = cp(U3)

# solution section--------------------------------------------------------------
t = 0.0                         # initial simulation time
while t <= Time:

    t += dt

    # rk 1st step
    r_U1 = sc.r_func(U1,nx)        # computing up-down stream ratios
    r_U2 = sc.r_func(U2,nx)
    r_U3 = sc.r_func(U3,nx)

    dU11,dU12,dU13 = sc.KT_solve(U1,U2,U3,r_U1,r_U2,r_U3,nx,g,dx)

    # rk 2nd step
    U1b = U1 + dU11*dt/2.0           # computing value from derivative
    U2b = U2 + dU12*dt/2.0
    U3b = U3 + dU13*dt/2.0

    r_U1 = sc.r_func(U1b,nx)        # computing up-down stream ratios
    r_U2 = sc.r_func(U2b,nx)
    r_U3 = sc.r_func(U3b,nx)

    dU21,dU22,dU23 = sc.KT_solve(U1b,U2b,U3b,r_U1,r_U2,r_U3,nx,g,dx)

    
    # rk 3rd step
    U1b = U1 + dU21*dt/2.0           # computing value from derivative
    U2b = U2 + dU22*dt/2.0
    U3b = U3 + dU23*dt/2.0

    r_U1 = sc.r_func(U1b,nx)        # computing up-down stream ratios
    r_U2 = sc.r_func(U2b,nx)
    r_U3 = sc.r_func(U3b,nx)

    dU31,dU32,dU33 = sc.KT_solve(U1b,U2b,U3b,r_U1,r_U2,r_U3,nx,g,dx)

    # rk 4th step
    U1b = U1 + dU31*dt           # computing value from derivative
    U2b = U2 + dU32*dt
    U3b = U3 + dU33*dt

    r_U1 = sc.r_func(U1b,nx)        # computing up-down stream ratios
    r_U2 = sc.r_func(U2b,nx)
    r_U3 = sc.r_func(U3b,nx)

    dU41,dU42,dU43 = sc.KT_solve(U1b,U2b,U3b,r_U1,r_U2,r_U3,nx,g,dx)

    # assembling the equation
    U1 = U1 + dt/6.0*(dU11 + 2.0*dU21 + 2.0*dU31 + dU41)
    U2 = U2 + dt/6.0*(dU12 + 2.0*dU22 + 2.0*dU32 + dU42)
    U3 = U3 + dt/6.0*(dU13 + 2.0*dU23 + 2.0*dU33 + dU43)
    
    # applying boundary conditions
    U1[nx-1] = 2*U1[nx-2] - U1[nx-3]
    U2[nx-1] = 2*U2[nx-2] - U2[nx-3]
    U3[nx-1] = 2*U3[nx-2] - U3[nx-3]

    # encoding to flux variables
    F1,F2,F3 = sc.encoder(U1,U2,U3,g)

    print("Current Time : ",t)

    # check for solution divergence
    if np.isnan(U1).any():
        raise ValueError("Solution Diverged")

# decoding to primitive variables and saving data-------------------------------

rho = cp(U1)
u = U2/U1
T = (g-1)/R*(U3/U1 - U2**2/2/U1**2)
P = rho*R*T

fid2 = pd.DataFrame({"X":X,"rho":rho,"u":u,"T":T,"P":P})
fid2.to_csv("Data_Final.csv", index=None)

# End of script-----------------------------------------------------------------
