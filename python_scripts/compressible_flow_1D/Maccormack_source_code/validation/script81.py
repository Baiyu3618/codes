###############################################################
# one dimensional constant area supersonic flow solver script #
# method: FDM Maccormack                                      #
# developed by: Ramkumar                                      #
###############################################################
import numpy as np
import matplotlib.pyplot as plt
from copy import copy as cp
import pandas as pd

# geometry and meshing section--------------------------------------------------
L  = 1.0                        # length of the domain 
nx = 81                         # number of nodes
X  = np.linspace(0.0, L, nx)    # creating x nodes
dx = L/float(nx-1)              # space step size

# fluid flow variables section -------------------------------------------------
rho0      = 1.5                 # inlet density of fluid
T0        = 500.0               # inlet temperature
Mach      = 3.0                 # inlet mach number
gamma     = 1.4                 # ratio of specific heats
R         = 287.0               # gas constant
SimTime   = 1.0                 # simulation time in seconds

# computation variables section-------------------------------------------------
Uin = Mach*np.sqrt(gamma*R*T0)     # inlet velocity
dt  = 0.5*dx/Uin                   # time step size

rho = np.linspace(rho0, 0.5*rho0, nx) 
u   = np.linspace(Uin, 0.0, nx)    # creating initial field
T   = np.linspace(T0, 0.8*T0, nx)

E   = R*T/(gamma-1.0) + u**2/2.0   # combining thermal variables
H   = E + R*T

U1  = cp(rho)                      # initializing flux variables
U2  = rho*u
U3  = rho*E

F1  = cp(U2)                       # initializing x-flux variables
F2  = (3.0-gamma)/2.0*U2**2/U1 + (gamma-1.0)*U3
F3  = gamma*U2*U3/U1 - U2**3/2.0/U1**2*(gamma-1.0)

U1b = cp(U1); F1b = cp(F1)         # initializing correctors
U2b = cp(U2); F2b = cp(F2)
U3b = cp(U3); F3b = cp(F3)

dU1 = np.zeros(nx, dtype = float); dU2 = cp(dU1); dU3 = cp(dU1)

t   = 0.0                          # setting initial time

# computation section-----------------------------------------------------------
while t <= SimTime:
    # predictor step
    for i in range(0,nx-1):
        df1 = (F1[i+1] - F1[i])/dx # computing first derivative
        df2 = (F2[i+1] - F2[i])/dx
        df3 = (F3[i+1] - F3[i])/dx

        dU1[i] = -cp(df1)           # computing time derivative
        dU2[i] = -cp(df2)
        dU3[i] = -cp(df3)

        U1b[i] = U1[i] + dU1[i]*dt # predictor step
        U2b[i] = U2[i] + dU2[i]*dt
        U3b[i] = U3[i] + dU3[i]*dt

    # intermediate encoding
    F1b  = cp(U2b)
    F2b  = (3.0-gamma)/2.0*U2b**2/U1b + (gamma-1.0)*U3b
    F3b  = gamma*U2b*U3b/U1b - U2b**3/2.0/U1b**2*(gamma-1.0)

    # corrector step
    for i in range(1,nx):
        df1 = (F1b[i] - F1b[i-1])/dx
        df2 = (F2b[i] - F2b[i-1])/dx
        df3 = (F3b[i] - F3b[i-1])/dx

        dU1b = -cp(df1)
        dU2b = -cp(df2)
        dU3b = -cp(df3)

        dU1avg = 0.5*(dU1[i] + dU1b)
        dU2avg = 0.5*(dU2[i] + dU2b)
        dU3avg = 0.5*(dU3[i] + dU3b)

        U1[i] = U1[i] + dU1avg*dt
        U2[i] = U2[i] + dU2avg*dt
        U3[i] = U3[i] + dU3avg*dt

    # linear extrapolation at outlet
    U1[nx-1] = 2*U1[nx-2] - U1[nx-3]
    U2[nx-1] = 2*U2[nx-2] - U2[nx-3]
    U3[nx-1] = 2*U3[nx-2] - U3[nx-3]

    # intermediate encoding
    F1  = cp(U2)
    F2  = (3.0-gamma)/2.0*U2**2/U1 + (gamma-1.0)*U3
    F3  = gamma*U2*U3/U1 - U2**3/2.0/U1**2*(gamma-1.0)

    print("\n Current Time : ",t)
    t += dt

    if np.isnan(F3).any():
        raise ValueError("Solution Diverged")

# decoder section---------------------------------------------------------------
rho = cp(U1)                                # density
u   = U2/U1                                 # velocity
T   = (gamma-1.0)/R*(U3/U1-U2**2/2.0/U1**2) # temperature
P   = rho*R*T                               # presure

# output export section---------------------------------------------------------
fid = pd.DataFrame({"X":X,'rho':rho,'U':u,'T':T,'P':P})
fid_ordered = fid[['X','rho','U','T','P']]  # to prevent auto arrange of columns
fid_ordered.to_csv("Data.csv", index=None)

# End of Script-----------------------------------------------------------------
