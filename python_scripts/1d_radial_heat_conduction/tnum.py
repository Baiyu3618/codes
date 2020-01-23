# complete radial heat conduction equation solution

import numpy as np
import matplotlib.pyplot as plt
from copy import copy as cp

# geometry and meshing section
R1 = 0.02
R2 = 0.04
N = 50

R = np.linspace(R1,R2,N)
dr = R[1]-R[0]

# thermal parameters
T1 = 373
T2 = 293
k= 205
rho = 2700
C = 900     #J/kgK

dt = 1e-4

# computation variables section
T = np.zeros(N, dtype = float)+T2; T[0] = cp(T1); Ts = cp(T)

# alpha = k/rho/C

# solution section
for iterate in range(100000):
    # solution
    for i in range(1,N-1):
        C1 = k*(T[i+1]-2*T[i]+T[i-1])/dr**2
        C2 = k/R[i]*(T[i+1]-T[i-1])/dr/2

        F = (C1 + C2)/rho/C

        Ts[i] = T[i] + F*dt

    convergence = np.max(abs(T-Ts)); T = cp(Ts)

    print(iterate)

    if convergence<1e-9:
        print("solution converged")
        break

# analytical solution computation
Ta = T1 + (T1-T2)/np.log(R1/R2)*np.log(R/R1)

# post computation section
plt.plot(R,T,'-k',linewidth = 2, label="numerical")
plt.plot(R,Ta,'or',linewidth = 2, label="Analytical")
plt.xlabel("radial direction"); plt.legend()
plt.ylabel("Temperature"); plt.grid(); plt.title("Temperature Variation")
plt.show()
