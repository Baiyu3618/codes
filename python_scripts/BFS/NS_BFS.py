# this program solves the incompressible laminar flow over backward facing step
# method of solution : Pressure Correction Technique SIMPLE
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
dt = 1e-02              # computational time step
Nstp = 1000             # number of time steps
Vavg = 1.0              # average velocity @ inlet (parabolic inlet specified)

# COMPUTAION VARIABLES SECTION--------------------------------------------------
npx = nx+1; npy = ny+1
nux = npx-1; nuy = npy
nvx = npx; nvy = npy-1

mu = rho*Vavg*width/Re

u = np.zeros([nuy,nux],dtype = float)
apu = cp(u); aeu = cp(u); awu = cp(u); anu = cp(u); asu = cp(u); bu = cp(u);
du  = cp(u);

v = np.zeros([nvy,nvx], dtype = float)
apv = cp(v); aev = cp(v); awv = cp(v); anv = cp(v); asv = cp(v); bv = cp(v);
dv  = cp(v);

p = np.zeros([npy,npx],dtype = float)
app = cp(p); aep = cp(p); awp = cp(p); anp = cp(p); asp = cp(p); Bp = cp(p);

ap0 = rho*dx*dy/dt
De = mu/dx*dy; Dw = cp(De); Dn = mu/dy*dx; Ds = cp(Dn)
u[int(nuy/2):nuy,0] = cp(Vavg); us = cp(u); vs = cp(v); pp = cp(p)

# COMPUTATION SECTION-----------------------------------------------------------
for itr in range(Nstp):
    # x-momentum equation coefficients computation
    for i in range(1,nux-1):
        for j in range(1,nuy-1):
            Fe = rho*dy*0.5*(u[j,i]+u[j,i+1])
            Fw = rho*dy*0.5*(u[j,i]+u[j,i-1])
            Fn = rho*dx*0.5*(v[j,i]+v[j,i+1])
            Fs = rho*dx*0.5*(v[j-1,i]+v[j-1,i+1])

            Pe = Fe/De; Pw = Fw/Dw; Pn = Fn/Dn; Ps = Fs/Ds

            aeu[j,i] = De*np.max([0,(1-0.1*abs(Pe))**5]) + np.max([0,-Fe])
            awu[j,i] = Dw*np.max([0,(1-0.1*abs(Pw))**5]) + np.max([0, Fw])
            anu[j,i] = Dn*np.max([0,(1-0.1*abs(Pn))**5]) + np.max([0,-Fn])
            asu[j,i] = Ds*np.max([0,(1-0.1*abs(Ps))**5]) + np.max([0, Fs])
            apu[j,i] = aeu[j,i]+awu[j,i]+anu[j,i]+asu[j,i]+ap0
            bu[j,i] = ap0*u[j,i]; du[j,i] = dy/apu[j,i]

    # y-momentum equation coefficients computation
    for i in range(1,nvx-1):
        for j in range(1,nvy-1):
            Fe = rho*dy*0.5*(u[j,i]+u[j+1,i])
            Fw = rho*dy*0.5*(u[j,i-1]+u[j+1,i-1])
            Fn = rho*dx*0.5*(v[j,i]+v[j+1,i])
            Fs = rho*dx*0.5*(v[j,i]+v[j-1,i])

            Pe = Fe/De; Pw = Fw/Dw; Pn = Fn/Dn; Ps = Fs/Ds

            aev[j,i] = De*np.max([0,(1-0.1*abs(Pe))**5]) + np.max([0,-Fe])
            awv[j,i] = Dw*np.max([0,(1-0.1*abs(Pw))**5]) + np.max([0, Fw])
            anv[j,i] = Dn*np.max([0,(1-0.1*abs(Pn))**5]) + np.max([0,-Fn])
            asv[j,i] = Ds*np.max([0,(1-0.1*abs(Ps))**5]) + np.max([0, Fs])
            apv[j,i] = aev[j,i]+awv[j,i]+anv[j,i]+asv[j,i]+ap0
            bv[j,i] = ap0*v[j,i]; dv[j,i] = dx/apv[j,i]

    # momentum equations Solution
    uprev = cp(us); vprev = cp(vs)
    for iterate_v in range(100):
        for i in range(1,nux-1):
            for j in range(1,nuy-1):
                us[j,i] = 1/apu[j,i]*(aeu[j,i]*us[j,i+1]+awu[j,i]*us[j,i-1]+\
                anu[j,i]*us[j+1,i]+asu[j,i]*us[j-1,i]+bu[j,i]) + \
                du[j,i]*(p[j,i]-p[j,i+1])
        for i in range(1,nvx-1):
            for j in range(1,nvy-1):
                vs[j,i] = 1/apv[j,i]*(aev[j,i]*vs[j,i+1]+awv[j,i]*vs[j,i-1]+\
                anv[j,i]*vs[j+1,i]+asv[j,i]*vs[j-1,i]+bv[j,i]) + \
                dv[j,i]*(p[j,i]-p[j+1,i])
        us[:,nux-1] = cp(us[:,nux-2])
        vs[:,nvx-1] = cp(vs[:,nvx-2])
        convergence_u = np.max(abs(uprev-us)); uprev = cp(us)
        convergence_v = np.max(abs(vprev-vs)); vprev = cp(vs)

        if convergence_u<1e-9 and convergence_v<1e-9:
            break

    # pressure correction equation coefficients computation
    for i in range(1,npx-1):
        for j in range(1,npy-1):
            aep[j,i] = rho*dy*du[j,i]
            awp[j,i] = rho*dy*du[j,i-1]
            anp[j,i] = rho*dx*dv[j,i]
            asp[j,i] = rho*dx*dv[j-1,i]
            app[j,i] = aep[j,i]+awp[j,i]+anp[j,i]+asp[j,i]
            Bp[j,i] = rho*(dy*(us[j,i-1]-us[j,i])+dx*(vs[j-1,i]-vs[j,i]))

    # pressure correction equation Solution
    pp = np.zeros([npy,npx], dtype = float); pprev = cp(pp)
    for iterate_p in range(100):
        for i in range(1,npx-1):
            for j in range(1,npy-1):
                pp[j,i] = 1/app[j,i]*(aep[j,i]*pp[j,i+1]+awp[j,i]*pp[j,i-1]+\
                anp[j,i]*pp[j+1,i]+asp[j,i]*pp[j-1,i] + Bp[j,i])
        pp[:,0] = cp(pp[:,1])
        pp[:,npx-1] = cp(pp[:,npx-2])
        pp[0,:] = cp(pp[1,:])
        pp[npy-1,:] = cp(pp[npy-2,:])

        convergence_p = np.max(abs(pprev-pp)); pprev = cp(pp)

        if convergence_p < 1e-7:
            break

    # pressure and velocity Correction
    p = p + 0.1*pp
    for i in range(1,nux-1):
        for j in range(1,nuy-1):
            u[j,i] = us[j,i] + du[j,i]*(pp[j,i]-pp[j,i+1])
    for i in range(1,nvx-1):
        for j in range(1,nvy-1):
            v[j,i] = vs[j,i] + dv[j,i]*(pp[j,i]-pp[j+1,i])
    u[:,nux-1] = cp(u[:,nux-2])
    v[:,nvx-1] = cp(v[:,nvx-2])

    print("\n TimeStep : ",itr+1)

    if np.isnan(p).any():
        print("\n ERROR!! Solution diverged")
        break
