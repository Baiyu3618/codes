# error computation file for Re100 of LDC
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# reading data from files
fidg = pd.read_csv("ghia_data.csv")        # ghia data
cols = ["U","V","W","VTK","ARC","X","Y","Z"]
fidx = pd.read_csv("X_data.csv",names=cols,skiprows=1,header=None)
fidy = pd.read_csv("Y_data.csv",names=cols,skiprows=1,header=None)

# normalizing the data
X = fidx["X"]/fidx["X"].max()
Y = fidy["Y"]/fidy["Y"].max()
U = fidy["U"]/fidy["U"].max()
V = fidx["V"]/fidy["U"].max()   # normalized using plate velocity

# writing data for octave plottings
fid = pd.DataFrame({"X":X,"Xg":fidg["X"],"Y":Y,"Yg":fidg["Y"],\
                    "U":U,"Ug":fidg["U_1000"],"V":V,"Vg":fidg["V_1000"]})
fid.to_csv("PlotData_octave.csv",index=None,sep="\t")

# plotting the graphs
fig1 = plt.figure()
plt.plot(U,Y,'-k',label="Anupravaha")
plt.plot(fidg["U_1000"],fidg["Y"],'or',label="Ghia Reference")
plt.legend()
plt.xlabel("U velocity Magnitude")
plt.ylabel("Y distance")
fig1.savefig("Uvelocity.png",dpi=300)

fig2 = plt.figure()
plt.plot(X,V,'-k',label="Anupravaha")
plt.plot(fidg["X"],fidg["V_1000"],'or',label="Ghia Reference")
plt.legend()
plt.xlabel("X distance")
plt.ylabel("V velocity magnitude")
fig2.savefig("Vvelocity.png",dpi=300)

plt.show()

