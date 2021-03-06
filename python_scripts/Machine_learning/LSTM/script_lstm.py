###########################################
# simple lstm model to determine the next #
# sequence of number in the list          #
###########################################

import numpy as np
import pandas as pd
from copy import copy as cp

from keras.models import Sequential
from keras.layers import Dense,LSTM,Activation, Dropout, BatchNormalization

from sklearn.preprocessing import MinMaxScaler

# function definitions----------------------------------------------------------
def data_generator(nsets, n_lookBack):
    # dataset initializer
    # Xdata = np.zeros([nsets,1, n_lookBack])
    # Ydata = np.zeros([nsets,1])
    dataset = np.zeros([nsets,n_lookBack+1])
    
    # dataset initializer
    master_count = 0
    for j in range(nsets):
        count = cp(master_count)
        for i in range(n_lookBack+1):
            dataset[j,i] = cp(count)
            count += 1
        master_count += 1
        # Ydata[j] = cp(count)
    #    
    return dataset

def scale_down(dataset):
    minval = dataset.min()
    maxval = dataset.max()

    return (dataset - minval)/(maxval - minval),minval,maxval

def scale_up(dataset,m,n):
    return dataset*(m-n) + n

# model generation--------------------------------------------------------------
nsets = 100
n_lookBack = 5
epoches = 10

dataset = data_generator(nsets, n_lookBack)

scaler = MinMaxScaler(feature_range=(0, 1))
dataset_scaled = scaler.fit_transform(dataset.transpose()).transpose()

# dataset_scaled,minval,maxval = scale_down(dataset)

Xtrain = dataset_scaled[:,:-1].reshape(nsets,n_lookBack,1)
Ytrain = dataset_scaled[:,-1:].reshape(nsets,1)

# keras begin

model = Sequential()

model.add(LSTM(units=n_lookBack, input_shape = (n_lookBack,1))) # lstm layer
model.add(Dropout(0.1))

# model.add(Dense(25, activation="relu"))
# model.add(BatchNormalization())
# model.add(Dropout(0.1))

model.add(Dense(1, activation="sigmoid"))

model.compile(loss='mse', optimizer='sgd',metrics=['accuracy'])

model.fit(Xtrain,Ytrain, epochs = epoches, batch_size=1)
