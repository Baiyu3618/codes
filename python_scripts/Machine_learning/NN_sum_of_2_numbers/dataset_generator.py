###########################################
# data set generator for ML 2 nums script #
###########################################

import numpy as np
import pandas as pd

# input and output variables
a = np.linspace(1,10,101)
b = np.linspace(2,20,101)

y = b + a

# writing the dataset to a file
fid = pd.DataFrame({"X":a,"Y":b,"Z":y})
fid.to_csv("Dataset.csv",index=None)
