##############################################################
# 1D compressible flow solution using kurganov tadmor scheme #
# developed by Ramkumar                                      #
##############################################################

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from copy import copy as cp

# functions definition section -------------------------------------------------
def encoder(u1,u2,u3,g):        # encoder funtion to compute F's from U's
    f1 = cp(u2)
    f2 = (3.0-g)/2.0*u2**2/u1 + (g-1.0)*u3
    f3 = g*u2*u3/u1 - u2**3/u1**2/2.0*(g-1.0)

    return f1,f2,f3

def r_func(U,nx):               # computes upstream-downstream ratio
    r = np.ones(nx, dtype = float)
    for i in range(1,nx-1):
        if (U[i+1]-U[i]) != 0.0:
            r[i] = (U[i]-U[i-1])/(U[i+1]-U[i])
        else:
            r[i] = 0.0
    return r

def phi(r):                     # computes limiter function
    res = np.max([0,np.max([min(2*r,1),min(2,r)])]) # super-bee function
    return res

def spectral_radius(u1,u2,u3,g): # computes spectral radius of jacobian
    # assumption: computing 3 roots of "complex" char* eqn is very tedious,
    # hence, computing single root and using it as the maximum absolute root
    # of the equation. even computing single root is tedious
    # reference for this: wikipedia:
    # https://en.wikipedia.org/wiki/Cubic_function

    a = 1.0                     # coeffs of char equation
    b = -(3*u2/u1)
    c = (g-1)*g*u2**2/2/u1**2-(g-1)*g*u3/u1
    d = u2**3/u1**3*(g**2/2-g/2+1) - g*(g-1)*u2*u3/u1
    # solution to cubic function
    del0 = b**2 - 3*a*c
    del1 = 2*b**3 - 9*a*b*c + 27*a**2*d
    # "abs" are included to prevent invalid input
    root1 = np.cbrt(abs(del1 + np.sqrt(abs(del1**2-4*del0**3)))/2.0)
    root2 = np.cbrt(abs(del1 - np.sqrt(abs(del1**2-4*del0**3)))/2.0)

    root = np.max([abs(root1),abs(root2)])

    return root

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
Time = 0.01   # simulation time

# computation variables section-------------------------------------------------
Uin = Mach*np.sqrt(g*R*T0)      # inlet velocity

rho = np.linspace(rho0,1.0,nx)  # initializing computational values
u = np.linspace(Uin, 0.0, nx)
T = np.linspace(T0, 288.18, nx)

dt = 0.1*dx/Uin                 # computational time step, 0.1 to prevent overflow

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

    # rk 1st step
    r_u1 = r_func(U1,nx)        # computing up-down stream ratios
    r_u2 = r_func(U2,nx)
    r_u3 = r_func(U3,nx)

    for i in range(2,nx-2):
        u1_Lm = U1[i-1] + 0.5*phi(r_u1[i-1])*(U1[i-1]-U1[i-2]) # flux at edges
        u1_Rm = U1[i] - 0.5*phi(r_u1[i])*(U1[i+1]-U1[i])
        u1_Lp = U1[i] + 0.5*phi(r_u1[i])*(U1[i]-U1[i-1])
        u1_Rp = U1[i+1] - 0.5*phi(r_u1[i+1])*(U1[i+2]-U1[i+1])

        u2_Lm = U2[i-1] + 0.5*phi(r_u2[i-1])*(U2[i-1]-U2[i-2])
        u2_Rm = U2[i] - 0.5*phi(r_u2[i])*(U2[i+1]-U2[i])
        u2_Lp = U2[i] + 0.5*phi(r_u2[i])*(U2[i]-U2[i-1])
        u2_Rp = U2[i+1] - 0.5*phi(r_u2[i+1])*(U2[i+2]-U2[i+1])

        u3_Lm = U3[i-1] + 0.5*phi(r_u3[i-1])*(U3[i-1]-U3[i-2])
        u3_Rm = U3[i] - 0.5*phi(r_u3[i])*(U3[i+1]-U3[i])
        u3_Lp = U3[i] + 0.5*phi(r_u3[i])*(U3[i]-U3[i-1])
        u3_Rp = U3[i+1] - 0.5*phi(r_u3[i+1])*(U3[i+2]-U3[i+1])

        sr_lm = spectral_radius(u1_Lm,u2_Lm,u3_Lm,g) # computing spectral radii
        sr_rm = spectral_radius(u1_Rm,u2_Rm,u3_Rm,g)
        sr_lp = spectral_radius(u1_Lp,u2_Lp,u3_Lp,g)
        sr_rp = spectral_radius(u1_Rp,u2_Rp,u3_Rp,g)
        alpha_m = np.max([sr_lm,sr_rm]) # local propogation speed
        alpha_p = np.max([sr_lp,sr_rp])

        F1_lm,F2_lm,F3_lm = encoder(u1_Lm,u2_Lm,u3_Lm,g)
        F1_rm,F2_rm,F3_rm = encoder(u1_Rm,u2_Rm,u3_Rm,g)
        F1_lp,F2_lp,F3_lp = encoder(u1_Lp,u2_Lp,u3_Lp,g)
        F1_rp,F2_rp,F3_rp = encoder(u1_Rp,u2_Rp,u3_Rp,g)

        F1L = 0.5*(F1_lm+F1_rm - alpha_m*(u1_Rm-u1_Lm))
        F1R = 0.5*(F1_lp+F1_rp - alpha_p*(u1_Rp-u1_Lp))

        F2L = 0.5*(F2_lm+F2_rm - alpha_m*(u2_Rm-u2_Lm))
        F2R = 0.5*(F2_lp+F2_rp - alpha_p*(u2_Rp-u2_Lp))

        F3L = 0.5*(F3_lm+F3_rm - alpha_m*(u3_Rm-u3_Lm))
        F3R = 0.5*(F3_lp+F3_rp - alpha_p*(u3_Rp-u3_Lp))

        dU1 = -(F1R-F1L)/dx
        dU2 = -(F2R-F2L)/dx
        dU3 = -(F3R-F3L)/dx

        U1[i] = U1[i] + dU1*dt
        U2[i] = U2[i] + dU2*dt
        U3[i] = U3[i] + dU3*dt

    # computing at left boundary side interior node
    i = 1
    u1_Lm = 0.5*(U1[i-1]+U1[i])
    u1_Rm = U1[i] - 0.5*phi(r_u1[i])*(U1[i+1]-U1[i])
    u1_Lp = U1[i] + 0.5*phi(r_u1[i])*(U1[i]-U1[i-1])
    u1_Rp = U1[i+1] - 0.5*phi(r_u1[i+1])*(U1[i+2]-U1[i+1])

    u2_Lm = 0.5*(U2[i-1]+U2[i])
    u2_Rm = U2[i] - 0.5*phi(r_u2[i])*(U2[i+1]-U2[i])
    u2_Lp = U2[i] + 0.5*phi(r_u2[i])*(U2[i]-U2[i-1])
    u2_Rp = U2[i+1] - 0.5*phi(r_u2[i+1])*(U2[i+2]-U2[i+1])

    u3_Lm = 0.5*(U3[i-1]+U3[i])
    u3_Rm = U3[i] - 0.5*phi(r_u3[i])*(U3[i+1]-U3[i])
    u3_Lp = U3[i] + 0.5*phi(r_u3[i])*(U3[i]-U3[i-1])
    u3_Rp = U3[i+1] - 0.5*phi(r_u3[i+1])*(U3[i+2]-U3[i+1])

    sr_lm = spectral_radius(u1_Lm,u2_Lm,u3_Lm,g) # computing spectral radii
    sr_rm = spectral_radius(u1_Rm,u2_Rm,u3_Rm,g)
    sr_lp = spectral_radius(u1_Lp,u2_Lp,u3_Lp,g)
    sr_rp = spectral_radius(u1_Rp,u2_Rp,u3_Rp,g)
    alpha_m = np.max([sr_lm,sr_rm]) # local propogation speed
    alpha_p = np.max([sr_lp,sr_rp])

    F1_lm,F2_lm,F3_lm = encoder(u1_Lm,u2_Lm,u3_Lm,g)
    F1_rm,F2_rm,F3_rm = encoder(u1_Rm,u2_Rm,u3_Rm,g)
    F1_lp,F2_lp,F3_lp = encoder(u1_Lp,u2_Lp,u3_Lp,g)
    F1_rp,F2_rp,F3_rp = encoder(u1_Rp,u2_Rp,u3_Rp,g)

    F1L = 0.5*(F1_lm+F1_rm - alpha_m*(u1_Rm-u1_Lm))
    F1R = 0.5*(F1_lp+F1_rp - alpha_p*(u1_Rp-u1_Lp))

    F2L = 0.5*(F2_lm+F2_rm - alpha_m*(u2_Rm-u2_Lm))
    F2R = 0.5*(F2_lp+F2_rp - alpha_p*(u2_Rp-u2_Lp))

    F3L = 0.5*(F3_lm+F3_rm - alpha_m*(u3_Rm-u3_Lm))
    F3R = 0.5*(F3_lp+F3_rp - alpha_p*(u3_Rp-u3_Lp))

    dU1 = -(F1R-F1L)/dx
    dU2 = -(F2R-F2L)/dx
    dU3 = -(F3R-F3L)/dx

    U1[i] = U1[i] + dU1*dt
    U2[i] = U2[i] + dU2*dt
    U3[i] = U3[i] + dU3*dt

    # computing at right boundary side interior node
    i = nx-2
    u1_Lm = U1[i-1] + 0.5*phi(r_u1[i-1])*(U1[i-1]-U1[i-2]) # flux at edges
    u1_Rm = U1[i] - 0.5*phi(r_u1[i])*(U1[i+1]-U1[i])
    u1_Lp = U1[i] + 0.5*phi(r_u1[i])*(U1[i]-U1[i-1])
    u1_Rp = 0.5*(U1[i+1]+U1[i])

    u2_Lm = U2[i-1] + 0.5*phi(r_u2[i-1])*(U2[i-1]-U2[i-2])
    u2_Rm = U2[i] - 0.5*phi(r_u2[i])*(U2[i+1]-U2[i])
    u2_Lp = U2[i] + 0.5*phi(r_u2[i])*(U2[i]-U2[i-1])
    u2_Rp = 0.5*(U2[i+1]+U2[i])

    u3_Lm = U3[i-1] + 0.5*phi(r_u3[i-1])*(U3[i-1]-U3[i-2])
    u3_Rm = U3[i] - 0.5*phi(r_u3[i])*(U3[i+1]-U3[i])
    u3_Lp = U3[i] + 0.5*phi(r_u3[i])*(U3[i]-U3[i-1])
    u3_Rp = 0.5*(U3[i+1]+U3[i])

    sr_lm = spectral_radius(u1_Lm,u2_Lm,u3_Lm,g) # computing spectral radii
    sr_rm = spectral_radius(u1_Rm,u2_Rm,u3_Rm,g)
    sr_lp = spectral_radius(u1_Lp,u2_Lp,u3_Lp,g)
    sr_rp = spectral_radius(u1_Rp,u2_Rp,u3_Rp,g)
    alpha_m = np.max([sr_lm,sr_rm]) # local propogation speed
    alpha_p = np.max([sr_lp,sr_rp])

    F1_lm,F2_lm,F3_lm = encoder(u1_Lm,u2_Lm,u3_Lm,g)
    F1_rm,F2_rm,F3_rm = encoder(u1_Rm,u2_Rm,u3_Rm,g)
    F1_lp,F2_lp,F3_lp = encoder(u1_Lp,u2_Lp,u3_Lp,g)
    F1_rp,F2_rp,F3_rp = encoder(u1_Rp,u2_Rp,u3_Rp,g)

    F1L = 0.5*(F1_lm+F1_rm - alpha_m*(u1_Rm-u1_Lm))
    F1R = 0.5*(F1_lp+F1_rp - alpha_p*(u1_Rp-u1_Lp))

    F2L = 0.5*(F2_lm+F2_rm - alpha_m*(u2_Rm-u2_Lm))
    F2R = 0.5*(F2_lp+F2_rp - alpha_p*(u2_Rp-u2_Lp))

    F3L = 0.5*(F3_lm+F3_rm - alpha_m*(u3_Rm-u3_Lm))
    F3R = 0.5*(F3_lp+F3_rp - alpha_p*(u3_Rp-u3_Lp))

    dU1 = -(F1R-F1L)/dx
    dU2 = -(F2R-F2L)/dx
    dU3 = -(F3R-F3L)/dx

    U1[i] = U1[i] + dU1*dt
    U2[i] = U2[i] + dU2*dt
    U3[i] = U3[i] + dU3*dt

    
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
