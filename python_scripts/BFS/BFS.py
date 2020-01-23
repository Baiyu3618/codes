# this program solves the incompressible laminar flow over backward facing step
# method of solution : vorticity-streamfunction formulation FDM
# author of the code : Ramkumar
# developed on       : saturday, 19/05/2018 @ 12:44 PM
# ref. for validation : verification and validation guide-Abaqus/CFD 6th unit

import numpy as np
from copy import copy as cp

# GEOMETRY AND MESHING SECTION--------------------------------------------------
length = 30.0           # length of fluid domain
width  = 1.0            # width of domain
nx = 51                # number of grids on x direction
ny = 21                 # number of grids on y direction

X,Y = np.meshgrid(np.linspace(0,length,nx),np.linspace(-width/2,width/2,ny))
dx = length/float(nx-1); dy = width/float(ny-1)
Nss = 0                 # step wall start node
Nse = int(ny/2)         # step wall end node

# FLUID FLOW VARIABLES SECTION--------------------------------------------------
rho = 1                 # fluid density
Re = 800.0              # Reynolds Number based on channel height
dt = 1e-03              # computational time step
Nstp = 1000             # number of time steps
Vavg = 1.0              # average velocity @ inlet (parabolic inlet specified)

# COMPUTATION VARIABLES SECTION-------------------------------------------------
nu = Vavg*width/Re
u = np.zeros([ny,nx], dtype = float);   # x velocity matrix
v = cp(u); p = cp(u); w = cp(u); ws = cp(u); shi = np.random.rand(ny,nx)#cp(u)

# VARIABLES INITIALIZATION SECTION----------------------------------------------
u[Nse:ny,0] = 2.4*Y[Nse:ny,0]*(0.5-Y[Nse:ny,0])  # intet velocity field
for j in range(Nse,ny):                         # streamfunction
    shi[j,0] = shi[j-1,0] + u[j,0]*dy
shi[ny-1,:] = cp(shi[ny-1,0])
shi[0,:] = 0; shi[Nss:Nse,0] = 0
# COMPUTATION SECTION-----------------------------------------------------------
Uprev = cp(u)
for itr in range(Nstp):
    # vorticiy boundary values computation
    for i in range(1,nx-1):
        j = 0               # at bottom boundary
        dUy = (u[j+1,i]-u[j,i])/dy
        w[j,i] = cp(dUy)

        j = ny-1            # at top boundary
        dUy = (u[j,i]-u[j-1,i])/dy
        w[j,i] = cp(dUy)

    for j in range(1,ny-1):
        i = 0               # at left boundary
        dVx = (v[j,i+1]-v[j,i])/dx
        w[j,i] = -dVx

        i = nx-1            # at right boundary
        dVx = (v[j,i]-v[j,i-1])
        w[j,i] = -dVx

    i = 0; j = 0            # at south west corner
    dUy = (u[j+1,i]-u[j,i])/dy
    dVx = (v[j,i+1]-v[j,i])/dx
    w[j,i] = dUy-dVx

    i = nx-1; j = 0         # at south east corner
    dUy = (u[j+1,i]-u[j,i])/dy
    dVx = (v[j,i]-v[j,i-1])/dx
    w[j,i] = dUy-dVx

    i = 0; j = ny-1         # at north west corner
    dUy = (u[j,i]-u[j-1,i])/dy
    dVx = (v[j,i+1]-v[j,i])/dx
    w[j,i] = dUy-dVx

    i = nx-1; j = ny-1      # at north east corner
    dUy = (u[j,i]-u[j-1,i])/dy
    dVx = (v[j,i]-v[j,i-1])/dx
    w[j,i] = dUy-dVx

    # vorticity equation explicit solution
    for i in range(1,nx-1):
        for j in range(1,ny-1):
            F1 = u[j,i]*(w[j,i+1]-w[j,i-1])/dx/2
            F2 = v[j,i]*(w[j+1,i]-w[j-1,i])/dy/2
            D1 = nu*(w[j,i+1]-2*w[j,i]+w[j,i-1])/dx**2
            D2 = nu*(w[j+1,i]-2*w[j,i]+w[j-1,i])/dx**2

            ws[j,i] = w[j,i] + (-F1-F2+D1+D2)*dt

    # streamfunction equation solution
    shiprev = cp(shi)
    for iterate_shi in range(100):
        for i in range(1,nx-1):
            for j in range(1,ny-1):
                shi[j,i] = dx**2*dy**2/2/(dx**2+dy**2)* \
                    ((shi[j,i+1]+shi[j,i-1])/dx**2+\
                    (shi[j+1,i]+shi[j-1,i])/dy**2 + ws[j,i])
        shi[:,nx-1] = cp(shi[:,nx-2])
        convergence_shi = np.max(abs(shiprev-shi)); shiprev = cp(shi)
        if convergence_shi<1e-6:
            break

    # velocity computation from streamfunction
    for i in range(1,nx-1):
        for j in range(1,ny-1):
            u[j,i] = (shi[j+1,i]-shi[j-1,i])/dy/2
            v[j,i] = (shi[j,i-1]-shi[j,i+1])/dx/2
    u[:,nx-1] = cp(u[:,nx-2])
    v[:,nx-1] = cp(v[:,nx-2])

    print("\n Time Step : ",itr+1)

    if np.isnan(ws).any():
        print("\nError Solution Diverged!!!")
        break

    convergence = np.max(ws - w); Uprev = cp(u)
    w = cp(ws)
