#########################################################################################
# data maker script for PGNN Burger's equation                                          #
# developed by Ramkumar                                                                 #
#                                                                                       #
# Data format                                                                           #
# INPUT = 51 x nodes with initial data + 1 node with time specification; total 52 nodes #
# OUTPUT = 51 x nodes with data for that specified time; total 51 nodes                 #
#########################################################################################

import os,glob, pandas as pd, numpy as np
from tqdm import tqdm

tqdm.pandas()

# reading all the filenames
files = sorted(glob.glob1(os.getcwd()+"/dataset_preparation","*.csv"))

# grid definition
X = np.linspace(0,1,51)

# initializing data holders
Xdata = []; Ydata = []

# looping through files
for file in files:
    # reading file data
    fid = pd.read_csv("dataset_preparation/"+file, header=None, delim_whitespace = True).values

    # getting parameters for initial data
    _,tmp1,tmp2,tmp3 = file.split("_")
    n = int(tmp1.split("n")[1])
    phi = float(tmp2.split("i")[1])
    A = float(tmp3.split("A")[1].split(".c")[0])

    # defining initial condition
    Uinit = A*np.sin(n*np.pi*(X - phi))

    # computing the time step size
    dt = 1.0/fid.shape[0]

    # appending the data in master list
    for i in range(fid.shape[0]):
        Xdata.append(list(Uinit) + list([(i+1)*dt]))
        Ydata.append(list(fid[i,:]))
    #

    print("Appended data from file : ",file)
#

# creating dataframe
print("creating dataframe .. ")
X = pd.DataFrame(Xdata)
Y = pd.DataFrame(Ydata).progress_apply(lambda x: x)
print("done.")

# writing datafame
print("writing data to file .. ")

X.to_csv("Xdata.csv", header=None, index=None).progress_apply(lambda x: x)
Y.to_csv("Ydata.csv", header=None, index=None)

print("Done")
