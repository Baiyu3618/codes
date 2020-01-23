import numpy as np
import matplotlib.pyplot as plt
from copy import copy as cp

# GEOMETRY AND MESHING SECTION--------------------------------------------------
length = 1.0; width = 0.5
nx = 21; ny = 21

X,Y = np.meshgrid(np.linspace(0.0,length,nx),np.linspace(0.0,width,ny))
dx = length/float(nx-1); dy = width/float(ny-1)
npx = nx+1; npy = ny+1
nux = npx-1; nuy = npy
nvx = npx; nvy = npy-1

# FLUID FLOW PARAMETERS SECTION-------------------------------------------------
rho = 1.225             # density of the FLUID
mu = 1.789e-5           # dynamic viscosity of the FLUID
Re = 1000.0             # flow Reynolds number
dt = 1e-2               # computational timestep for the simulation
Iteration = 1000        # number of time steps

# COMPUTATIONAL VARIABLES SECTION-----------------------------------------------
Uplate = Re*mu/rho/length   # plate velocity based on Reynolds number
u = np.zeros([nuy,nux], dtype = float); u[nuy-1,:] = Uplate
us = cp(u); apu = cp(u); aeu = cp(u); awu = cp(u); anu = cp(u); asu = cp(u)
du = cp(u); bu = cp(u);
v = np.zeros([nvy,nvx], dtype = float)
vs = cp(v); apv = cp(v); aev = cp(v); awv = cp(v); anv = cp(v); asv = cp(v)
dv = cp(v); bv = cp(v);
p = np.zeros([npy,npx], dtype = float)
app = cp(p); aep = cp(p); awp = cp(p); anp = cp(p); asp = cp(p); Bp = cp(p)
pp = cp(p);

De = mu/dx*dy; Dw = cp(De); Dn = mu/dy*dx; Ds = cp(Dn)
ap0 = rho*dx*dy/dt

# COMPUTATION SECTION-----------------------------------------------------------
for itr in range(Iteration):
    # x-momentum equation coefficients computation
    for i in range(1,nux-1):
        for j in range(1,nuy-1):
            Fe = rho*dy*0.5*(u[j,i]+u[j,i+1])
            Fw = rho*dy*0.5*(u[j,i]+u[j,i-1])
            Fn = rho*dx*0.5*(v[j,i]+v[j,i+1])
            Fs = rho*dx*0.5*(v[j-1,i]+v[j-1,i+1])

            Pe = Fe/De; Pw = Fw/Dw; Pn = Fn/Dn; Ps = Fs/Ds

            aeu[j,i] = De*np.max([0.0,(1-0.1*abs(Pe))**5]) + np.max([0.0,-Fe])
            awu[j,i] = Dw*np.max([0.0,(1-0.1*abs(Pw))**5]) + np.max([0.0, Fw])
            anu[j,i] = Dn*np.max([0.0,(1-0.1*abs(Pn))**5]) + np.max([0.0,-Fn])
            asu[j,i] = Ds*np.max([0.0,(1-0.1*abs(Ps))**5]) + np.max([0.0, Fs])
            apu[j,i] = aeu[j,i]+awu[j,i]+anu[j,i]+asu[j,i]+ap0
            du[j,i] = dy/apu[j,i]; bu[j,i] = ap0*u[j,i]

    # y-momentum equation coefficients computation
    for i in range(1,nvx-1):
        for j in range(1,nvy-1):
            Fe = rho*dy*0.5*(u[j,i]+u[j+1,i])
            Fw = rho*dy*0.5*(u[j,i-1]+u[j+1,i-1])
            Fn = rho*dx*0.5*(v[j,i]+v[j+1,i])
            Fs = rho*dx*0.5*(v[j,i]+v[j-1,i])

            Pe = Fe/De; Pw = Fw/Dw; Pn = Fn/Dn; Ps = Fs/Ds

            aev[j,i] = De*np.max([0.0,(1-0.1*abs(Pe))**5]) + np.max([0.0,-Fe])
            awv[j,i] = Dw*np.max([0.0,(1-0.1*abs(Pw))**5]) + np.max([0.0, Fw])
            anv[j,i] = Dn*np.max([0.0,(1-0.1*abs(Pn))**5]) + np.max([0.0,-Fn])
            asv[j,i] = Ds*np.max([0.0,(1-0.1*abs(Ps))**5]) + np.max([0.0, Fs])
            apv[j,i] = aev[j,i]+awv[j,i]+anv[j,i]+asv[j,i]+ap0
            dv[j,i] = dx/apv[j,i]; bv[j,i] = ap0*v[j,i]

    # momentum equations solution
    # uprev = cp(us); vprev = cp(vs)
    uprev = np.zeros([nuy,nux], dtype=float)
    vprev = np.zeros([nvy,nvx], dtype=float)
    for iterate_v in range(100):
        for i in range(1,nux-1):
            for j in range(1,nuy-1):
                us[j,i] = 1/apu[j,i]*(aeu[j,i]*us[j,i+1]+awu[j,i]*us[j,i-1]+
                    anu[j,i]*us[j+1,i]+asu[j,i]*us[j-1,i]+bu[j,i]) + \
                    du[j,i]*(p[j,i]-p[j,i+1])
        for i in range(1,nvx-1):
            for j in range(1,nvy-1):
                vs[j,i] = 1/apv[j,i]*(aev[j,i]*vs[j,i+1]+awv[j,i]*vs[j,i-1]+
                    anv[j,i]*vs[j+1,i]+asv[j,i]*vs[j-1,i]+bv[j,i]) + \
                    dv[j,i]*(p[j,i]-p[j+1,i])
        convergence_u = np.max(abs(uprev-us)); uprev = cp(us)
        convergence_v = np.max(abs(vprev-vs)); vprev = cp(vs)

        if convergence_u < 1e-9 and convergence_v <1e-9:
            break

    # pressure correction equation coefficients computation
    pp = np.zeros([npy,npx], dtype = float); pprev = cp(pp)
    for i in range(1,npx-1):
        for j in range(1,npy-1):
            aep[j,i] = rho*dy*du[j,i]
            awp[j,i] = rho*dy*du[j,i-1]
            anp[j,i] = rho*dx*dv[j,i]
            asp[j,i] = rho*dx*dv[j-1,i]
            app[j,i] = aep[j,i]+awp[j,i]+anp[j,i]+asp[j,i]
            Bp[j,i] = rho*(dy*(us[j,i-1]-us[j,i])+dx*(vs[j-1,i]-vs[j,i]))

    # pressure correction equation solution
    for iterate_p in range(100):
        for i in range(1,npx-1):
            for j in range(1,npy-1):
                pp[j,i] = 1/app[j,i]*(aep[j,i]*pp[j,i+1]+awp[j,i]*pp[j,i-1]+ \
                    anp[j,i]*pp[j+1,i]+asp[j,i]*pp[j-1,i]+Bp[j,i])
        pp[:,0] = cp(pp[:,1]);
        pp[:,npx-1] = cp(pp[:,npx-2])
        pp[0,:] = cp(pp[1,:])
        pp[npy-1,:] = cp(pp[npy-2,:])

        convergence_p = np.max(abs(pprev-pp)); pprev = cp(pp)
        if convergence_p < 1e-6:
            break

    # update pressure and velocity
    p = p + 0.1*pp
    for i in range(1,nux-1):
        for j in range(1,nuy-1):
            u[j,i] = us[j,i] + du[j,i]*(pp[j,i]-pp[j,i+1])
    for i in range(1,nvx-1):
        for j in range(1,nvy-1):
            v[j,i] = vs[j,i] + dv[j,i]*(pp[j,i]-pp[j+1,i])

    print("\n TimeStep: ",itr+1)

    if np.isnan(pp).any():
        print("\n ERROR!! Solution Diverged")

# INTERPOLATION SECTION---------------------------------------------------------
U = np.zeros([ny,nx],dtype = float); V = cp(U); P = cp(U)

U[0,:] = cp(u[0,:]); U[ny-1,:] = cp(u[nuy-1,:])
for j in range(1,ny-1):                     # interpolating u velocity
    U[j,:] = 0.5*(u[j,:] + u[j+1,:])

V[:,0] = cp(v[:,0]); V[:,nx-1] = cp(v[:,nvx-1])
for i in range(1,nx-1):                     # interpolating v velocity
    V[:,i] = 0.5*(v[:,i] + v[:,i+1])

for i in range(nx):                       # interpolating static pressure
    for j in range(ny):
        P[j,i] = 0.25*(p[j,i]+p[j,i+1]+p[j+1,i]+p[j+1,i+1])

# DATA EXPORT SECTION-----------------------------------------------------------
fid = open("Data.csv","w")
for i in range(nx):
    for j in range(ny):
        fid.writelines('%f,%f,%f,%f,%f\n' %(X[j,i],Y[j,i],U[j,i],V[j,i],P[j,i]))

fid.close()

# POST-PROCESSING SECTION-------------------------------------------------------
fig1 = plt.figure()
plt.contourf(X,Y,np.sqrt(U**2+V**2),100,cmap = 'jet'); plt.axis('image');
plt.colorbar(); plt.title("Velocity Magnitude")
fig1.savefig("Velocity.png",dpi=300)

fig2 = plt.figure()
plt.contourf(X,Y,P,100,cmap = 'jet'); plt.axis('image');
plt.colorbar(); plt.title("Pressure")
fig2.savefig("Pressure.png",dpi=300)

fig3 = plt.figure()
plt.streamplot(X,Y,U,V,2); plt.axis([0,length,0,width]);
plt.title("Streamlines Contour");
fig3.savefig("Streamline.png", dpi=300)
