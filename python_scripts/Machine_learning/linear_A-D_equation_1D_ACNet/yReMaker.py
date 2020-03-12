import pandas as pd
import numpy as np

fid = pd.read_csv("Y_orig.csv", header = None)

zero = pd.DataFrame(np.zeros(fid.shape[0]))

for i in range(49):
    fid = pd.concat([fid,zero], axis = "columns")

fid.to_csv("Y.csv", index = None, header = None)
