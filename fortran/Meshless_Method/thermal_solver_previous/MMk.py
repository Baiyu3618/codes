# 2D heat conduction equation solution using Meshless Method
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from copy import copy as cp

# geometry section--------------------------------------------------------------
length = 1.0                        # length of domain
width = 1.0                         # width of domain
Ni = 10                             # no of interior points
Nb = 13                             # no of points in boundary
Lc = length/5.0                    # cut-off length

# Xi,Yi = length*np.random.rand(Ni), width*np.random.rand(Ni) # interior points

dx = length/float(Nb-1); dy = width/float(Nb-1)
Xi,Yi = np.meshgrid(np.linspace(dx,length-dx,Ni),np.linspace(dy,width-dy,Ni))
Xi = Xi.flatten()
Yi = Yi.flatten()
                                    # creating boundary nodes
Xn = np.linspace(0,length,Nb); Yn = Xn*0 + width
Xs = cp(Xn); Ys = Xs*0
Ye = np.linspace(dy,width-dy,Nb-2); Xe = Ye*0 + length
Yw = cp(Ye); Xw = Yw*0

Xb = np.array(list(Xn)+list(Xs)+list(Xe)+list(Xw))  # combining boundary nodes
Yb = np.array(list(Yn)+list(Ys)+list(Ye)+list(Yw))

X = np.array(list(Xb)+list(Xi))         # combining entire nodes
Y = np.array(list(Yb)+list(Yi))

# N = Ni + Nb*4 - 4                       # total number of points
N = Ni*Ni + Nb*4 - 4                       # total number of points

BNODES = range(Nb*4-4)                  # total boundary nodes
INODES = range((Nb*4-4),N)            # total interior nodes
NBNODES = range(Nb)                     # Northern boundary nodes
SBNODES = range(Nb,2*Nb)              # southern boundary nodes
EBNODES = range(2*Nb,3*Nb-2)          # eastern boundary nodes
WBNODES = range(3*Nb-2,4*Nb-4)          # western boundary nodes

# Thermal parameters section----------------------------------------------------
T_init = 310.0          # initial temperature value
T_north = 350.0         # northern boundary temperature
T_south = 310.0         # southern boundary temperature
T_east = 350.0          # eastern boundary temperature
T_west = 310.0          # western boundary temperature

density = 2700.0        # density of aluminum
K = 205.0               # thermal conductivity aluminum
C = 0.9e3               # specific heat of aluminum

Nstep = 50000
dt = 1e-2

# computation variables section-------------------------------------------------
T = np.zeros(N, dtype = float)  # temperature array pre-allocation
dTx = cp(T); dTy = cp(T)        # 1st derivative array pre-allocation
alpha = K/density/C             # thermal diffusivity value

T[INODES] = cp(T_init)          # applying initial and boundary conditions
T[NBNODES] = cp(T_north)
T[SBNODES] = cp(T_south)
T[EBNODES] = cp(T_east)
T[WBNODES] = cp(T_west)

Ts = cp(T)

NENODES = np.zeros([N,int(N/4)], dtype = int) + np.nan

# neighbouring nodes computation section----------------------------------------
count = np.zeros(N,dtype = int)
for i in range(N):
    for j in range(N):
        if i != j:
            dist = np.sqrt((X[i]-X[j])**2 + (Y[i]-Y[j])**2)
            if dist <= Lc:
                NENODES[i,count[i]] = cp(j)
                count[i] += 1
    if np.isnan(NENODES[i,:]).all():
        raise Exception("Idle Nodes detected,\
         increase cutoff_width or no. of points")

# computation section-----------------------------------------------------------
for itr in range(Nstep):
    # 1st order derivatives computation
    for i in INODES:
        j = 0
        dFidXi = 0.0; dFidYi = 0.0; dXi2 = 0.0; dYi2 = 0.0; dXidYi = 0.0
        while not(np.isnan(NENODES[i,j])):
            k = int(NENODES[i,j])
            dFidXi += abs(T[i]-T[k])*abs(X[i]-X[k])
            dFidYi += abs(T[i]-T[k])*abs(Y[i]-Y[k])
            dXi2 += (X[i]-X[k])**2
            dYi2 += (Y[i]-Y[k])**2
            dXidYi += abs(X[i]-X[k])*abs(Y[i]-Y[k])
            j += 1
        det = dXi2*dYi2 - dXidYi**2
        dTx[i] = (dFidXi*dYi2 - dFidYi*dXidYi)/det
        dTy[i] = (dFidYi*dXi2 - dFidXi*dXidYi)/det

    # heat equation solution
    for i in INODES:
        j = 0
        dFidXi = 0.0; dFidYi = 0.0; dXi2 = 0.0; dYi2 = 0.0; dXidYi = 0.0
        while not(np.isnan(NENODES[i,j])):
            k = int(NENODES[i,j])
            dFidXi += abs(dTx[i]-dTx[k])*abs(X[i]-X[k])
            dFidYi += abs(dTx[i]-dTx[k])*abs(Y[i]-Y[k])
            dXi2 += (X[i]-X[k])**2
            dYi2 += (Y[i]-Y[k])**2
            dXidYi += abs(X[i]-X[k])*abs(Y[i]-Y[k])
            j += 1
        det = dXi2*dYi2 - dXidYi**2
        dTxx = (dFidXi*dYi2 - dFidYi*dXidYi)/det # 2nd derivative in x
        dTxy = (dFidYi*dXi2 - dFidXi*dXidYi)/det

        j = 0
        dFidXi = 0.0; dFidYi = 0.0; dXi2 = 0.0; dYi2 = 0.0; dXidYi = 0.0
        while not(np.isnan(NENODES[i,j])):
            k = int(NENODES[i,j])
            dFidXi += abs(dTy[i]-dTy[k])*abs(X[i]-X[k])
            dFidYi += abs(dTy[i]-dTy[k])*abs(Y[i]-Y[k])
            dXi2 += (X[i]-X[k])**2
            dYi2 += (Y[i]-Y[k])**2
            dXidYi += abs(X[i]-X[k])*abs(Y[i]-Y[k])
            j += 1
        det = dXi2*dYi2 - dXidYi**2
        dTyx = (dFidXi*dYi2 - dFidYi*dXidYi)/det
        dTyy = (dFidYi*dXi2 - dFidXi*dXidYi)/det # 2nd derivative in y

        Ts[i] = T[i] + alpha*(dTxx + dTyy)*dt

    print("Timestep : ",itr+1)

    if (Ts>500).any():
        raise ValueError("Solution Diverged")

    convergence = np.max(abs(Ts - T)); T = cp(Ts)
    if convergence < 1e-8:
        print("Soluion Converged")
        break

# data export section-----------------------------------------------------------
fid = open("Data.csv","w")
fid.writelines("X,Y,Z,T\n")
for i in range(N):
    fid.writelines("%f,%f,%f,%f\n" %(X[i],Y[i],0.0,T[i]))
fid.close()


triang = tri.Triangulation(X,Y)
plt.tricontourf(triang,T,100); plt.axis("image")
plt.colorbar(); plt.show()
