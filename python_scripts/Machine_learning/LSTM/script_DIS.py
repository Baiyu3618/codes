##################################################
# LSTM script for DIS stockMarket data structure #
# developed by Ramkumar                          #
##################################################
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization, LSTM
from copy import copy as cp
from sklearn.preprocessing import MinMaxScaler

# reading the data from file----------------------------------------------------
file = "DIS.csv"
fid = pd.read_csv("DIS.csv", header=None, sep=",", names="D123456")
fid.drop(["D","6"], axis = "columns", inplace = True)

# converting data to LSTM suitable format---------------------------------------
nsteps, nfeatures = fid.shape
df = fid.values

scaler = MinMaxScaler(feature_range=(0,1))
df_scaled = scaler.fit_transform(df)

ntime = 20                     # number of look-back time samples
nout = 1                      # number of output sequence time samples, FOR NOW ITS 1 only!!

nsamples = nsteps-ntime-nout+1  # formula for proper usage of all data

Xtrain = np.zeros([nsamples,ntime,nfeatures]) # X data array
Ytrain = np.zeros([nsamples,nout,nfeatures]) # Y data array

count_a = 0

for sample in range(nsamples):
    count_b = 0
    for time in range(ntime):
        Xtrain[sample,time,:] = cp(df_scaled[count_a + count_b,:])
        count_b += 1
    for out in range(nout):
        Ytrain[sample,out,:] = cp(df_scaled[count_a + count_b,:])
        count_b += 1
    #
    count_a += 1
#
Ytrain = Ytrain.reshape(nsamples,nfeatures)

# creating keras model----------------------------------------------------------

epoches = 2000
batch_size = 10

# creating model
model = Sequential()

# adding lstm layer
model.add( LSTM( units = ntime*nfeatures, activation = "tanh", input_shape = (ntime,nfeatures)))
# model.add(keras.layers.LSTM(units, activation='tanh', recurrent_activation='hard_sigmoid',
#                             use_bias=True, kernel_initializer='glorot_uniform',
#                             recurrent_initializer='orthogonal', bias_initializer='zeros',
#                             unit_forget_bias=True, kernel_regularizer=None, recurrent_regularizer=None,
#                             bias_regularizer=None, activity_regularizer=None, kernel_constraint=None,
#                             recurrent_constraint=None, bias_constraint=None, dropout=0.0, recurrent_dropout=0.0,
#                             implementation=1, return_sequences=False, return_state=False, go_backwards=False,
#                             stateful=False, unroll=False)

# adding dense setup layers
model.add(Dense(units = 40, activation = "relu"))
model.add(BatchNormalization(axis =-1, momentum = 0.9))
model.add(Dropout(rate = 0.1))

model.add(Dense(units = 15, activation = "relu"))
model.add(BatchNormalization(axis =-1, momentum = 0.9))
model.add(Dropout(rate = 0.1))

model.add(Dense(units = nfeatures, activation = "sigmoid"))

# compiling the model
model.compile(optimizer = "rmsprop", loss = "mse", metrics=["accuracy"])

# fitting the model
model.fit(Xtrain,Ytrain, batch_size= batch_size, epochs = epoches, verbose = 1)

# saving model
model.save("model_DIS.h5")
model.save_weights("model_DIS_weights.h5")
