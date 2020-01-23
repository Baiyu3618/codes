#####################################################################
# 1-D Compressible Flow solution using RK4, Kurganov-Tadmor Scheme  #
#                                                                   #
# developed by                   : Ramkumar                         #
# discretization method          : FDM                              #
# discretization type            : Semi-discrete                    #
# spatial discretization method  : Kurganov-Tadmor Central Scheme   #
# Temporal discretization scheme : Runge-Kutta 4th order            #
# description                    :                                  #
# this is the solver script that contains KT scheme                 #
# along with other supporting functions for solution                #
#                                                                   #
# Future Works                   : same with FVM and documentation  #
#####################################################################

import numpy as np
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


def KT_solve(Us1,Us2,Us3,r_u1,r_u2,r_u3,nx,g,dx):

    du1 = np.zeros(nx, dtype = float)
    du2 = np.zeros(nx, dtype = float)
    du3 = np.zeros(nx, dtype = float)
    
    for i in range(2,nx-2):
        u1_Lm = Us1[i-1] + 0.5*phi(r_u1[i-1])*(Us1[i-1]-Us1[i-2]) # flux at edges
        u1_Rm = Us1[i] - 0.5*phi(r_u1[i])*(Us1[i+1]-Us1[i])
        u1_Lp = Us1[i] + 0.5*phi(r_u1[i])*(Us1[i]-Us1[i-1])
        u1_Rp = Us1[i+1] - 0.5*phi(r_u1[i+1])*(Us1[i+2]-Us1[i+1])

        u2_Lm = Us2[i-1] + 0.5*phi(r_u2[i-1])*(Us2[i-1]-Us2[i-2])
        u2_Rm = Us2[i] - 0.5*phi(r_u2[i])*(Us2[i+1]-Us2[i])
        u2_Lp = Us2[i] + 0.5*phi(r_u2[i])*(Us2[i]-Us2[i-1])
        u2_Rp = Us2[i+1] - 0.5*phi(r_u2[i+1])*(Us2[i+2]-Us2[i+1])

        u3_Lm = Us3[i-1] + 0.5*phi(r_u3[i-1])*(Us3[i-1]-Us3[i-2])
        u3_Rm = Us3[i] - 0.5*phi(r_u3[i])*(Us3[i+1]-Us3[i])
        u3_Lp = Us3[i] + 0.5*phi(r_u3[i])*(Us3[i]-Us3[i-1])
        u3_Rp = Us3[i+1] - 0.5*phi(r_u3[i+1])*(Us3[i+2]-Us3[i+1])

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

        du1[i] = -(F1R-F1L)/dx
        du2[i] = -(F2R-F2L)/dx
        du3[i] = -(F3R-F3L)/dx


    # computing at left boundary side interior node
    i = 1
    u1_Lm = 0.5*(Us1[i-1]+Us1[i])
    u1_Rm = Us1[i] - 0.5*phi(r_u1[i])*(Us1[i+1]-Us1[i])
    u1_Lp = Us1[i] + 0.5*phi(r_u1[i])*(Us1[i]-Us1[i-1])
    u1_Rp = Us1[i+1] - 0.5*phi(r_u1[i+1])*(Us1[i+2]-Us1[i+1])

    u2_Lm = 0.5*(Us2[i-1]+Us2[i])
    u2_Rm = Us2[i] - 0.5*phi(r_u2[i])*(Us2[i+1]-Us2[i])
    u2_Lp = Us2[i] + 0.5*phi(r_u2[i])*(Us2[i]-Us2[i-1])
    u2_Rp = Us2[i+1] - 0.5*phi(r_u2[i+1])*(Us2[i+2]-Us2[i+1])

    u3_Lm = 0.5*(Us3[i-1]+Us3[i])
    u3_Rm = Us3[i] - 0.5*phi(r_u3[i])*(Us3[i+1]-Us3[i])
    u3_Lp = Us3[i] + 0.5*phi(r_u3[i])*(Us3[i]-Us3[i-1])
    u3_Rp = Us3[i+1] - 0.5*phi(r_u3[i+1])*(Us3[i+2]-Us3[i+1])

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
    
    du1[i] = -(F1R-F1L)/dx
    du2[i] = -(F2R-F2L)/dx
    du3[i] = -(F3R-F3L)/dx

    # computing at right boundary side interior node
    i = nx-2
    u1_Lm = Us1[i-1] + 0.5*phi(r_u1[i-1])*(Us1[i-1]-Us1[i-2]) # flux at edges
    u1_Rm = Us1[i] - 0.5*phi(r_u1[i])*(Us1[i+1]-Us1[i])
    u1_Lp = Us1[i] + 0.5*phi(r_u1[i])*(Us1[i]-Us1[i-1])
    u1_Rp = 0.5*(Us1[i+1]+Us1[i])

    u2_Lm = Us2[i-1] + 0.5*phi(r_u2[i-1])*(Us2[i-1]-Us2[i-2])
    u2_Rm = Us2[i] - 0.5*phi(r_u2[i])*(Us2[i+1]-Us2[i])
    u2_Lp = Us2[i] + 0.5*phi(r_u2[i])*(Us2[i]-Us2[i-1])
    u2_Rp = 0.5*(Us2[i+1]+Us2[i])

    u3_Lm = Us3[i-1] + 0.5*phi(r_u3[i-1])*(Us3[i-1]-Us3[i-2])
    u3_Rm = Us3[i] - 0.5*phi(r_u3[i])*(Us3[i+1]-Us3[i])
    u3_Lp = Us3[i] + 0.5*phi(r_u3[i])*(Us3[i]-Us3[i-1])
    u3_Rp = 0.5*(Us3[i+1]+Us3[i])

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

    du1[i] = -(F1R-F1L)/dx
    du2[i] = -(F2R-F2L)/dx
    du3[i] = -(F3R-F3L)/dx

    return du1,du2,du3

# end of script-----------------------------------------------------------------
