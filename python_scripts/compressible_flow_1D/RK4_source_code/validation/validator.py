########################################################
# validation script for 1d supersonic flow solver code #
# developed by Ramkumar                                #
########################################################
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from copy import copy as cp

# input parameters--------------------------------------------------------------
rho0  = 1.5                 # inlet density of fluid
T0    = 500.0               # inlet temperature
Mach  = 3.0                 # inlet mach number
gamma = 1.4                 # ratio of specific heats
R     = 287.0               # gas constant
L     = 1.0                 # length of domain

# reading data from files-------------------------------------------------------
fid_21  = pd.read_csv('Data21.csv')
fid_41  = pd.read_csv('Data41.csv')
fid_81  = pd.read_csv('Data81.csv')

# computing errors from results-------------------------------------------------
Umax = Mach*np.sqrt(gamma*R*T0)   # analytical velocity throughout domain

Erms = np.zeros(3); Ep = cp(Erms) # initializing arrays

# computing rms errors
Erms[0] = np.sqrt(((Umax-fid_21["U"])**2).mean())
Erms[1] = np.sqrt(((Umax-fid_41["U"])**2).mean())
Erms[2] = np.sqrt(((Umax-fid_81["U"])**2).mean())

# computing percentage errors
Ep[0] = (abs(Umax-fid_21["U"])/Umax).mean()*100.0
Ep[1] = (abs(Umax-fid_41["U"])/Umax).mean()*100.0
Ep[2] = (abs(Umax-fid_81["U"])/Umax).mean()*100.0

# computing grid spaces
DX = [L/40,L/80,L/160]

# dumping error computations to file
fid = pd.DataFrame({"DX":DX,"Erms":Erms,"Ep":Ep})
fid.to_csv("Error_Data.csv",index=None)

# plotting graphs---------------------------------------------------------------
fig1 = plt.figure()             # plotting rms graph
plt.plot(DX,Erms,'-c')
plt.plot(DX[0],Erms[0],'ok',label = '21')
plt.plot(DX[1],Erms[1],'sk',label = '41')
plt.plot(DX[2],Erms[2],'^k',label = '81')
plt.xscale('log'); plt.yscale('log')
plt.xlabel('Grid Spaces')
plt.ylabel('RMS Error')
plt.title("RMS Error Plot")
plt.legend()
fig1.savefig("RMSError.png")

fig2 = plt.figure()             # plotting rms graph
plt.plot(DX,Ep,'-c')
plt.plot(DX[0],Ep[0],'ok',label = '21')
plt.plot(DX[1],Ep[1],'sk',label = '41')
plt.plot(DX[2],Ep[2],'^k',label = '81')
plt.xscale('log'); plt.yscale('log')
plt.xlabel('Grid Spaces')
plt.ylabel('Error Percentage')
plt.title("Error Percentage Plot")
plt.legend()
fig2.savefig("ErrorPercentage.png")

plt.show()
