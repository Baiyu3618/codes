import numpy as np
import matplotlib.pyplot as plt

fid = open("p_residual.txt")

PR = np.zeros(200000, dtype = float)

for i in range(200000):
	PR[i] = fid.readline()

fid.close()

plt.plot(PR,'-b', linewidth = 2); plt.ylabel("P Residual") 
plt.title("Pressure Residual Plot"); plt.xlabel("Time Steps")
plt.grid()
plt.show()
