#####################################################################################
# Architecture-Constrained Neural Network for solving Advection-Diffusion Equations #
# developed by Ramkumar                                                             #
#####################################################################################

# hiding unnecessary system warnings
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["KMP_WARNINGS"] = "FALSE"

import numpy as np
import pandas as pd
import tensorflow as tf
from copy import copy as cp
impot matplotlib.pyplot as plt

# hiding unnecessary tensorflow warnings
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

# disabling eager execution to make physics-constraining feasable.
tf.compat.v1.disable_eager_execution()

####################################
# simulation parameters definition #
####################################
n = 51
a = 0.5
nu = 0.1
length = 1.0
Time = 10.0
dt = 1e-3
dx = length/(n-1)

########################################
# Neural Network Parameters Definition #
########################################
lrate = 1e-4                               # learning rate
act_func = None       # activation function
kernel_init = tf.keras.initializers.RandomUniform() # kernel initializer
bias_init = tf.keras.initializers.RandomUniform()   # bias initializer
optimizer = tf.keras.optimizers.Adam(learning_rate = lrate)     # optimizer
loss = tf.keras.losses.MeanSquaredError()  # loss function
epochs = 100                                # number of epochs
batch_size = 5                             # batch_size

#############################
# weight matrix definitions #
#############################
mat = np.zeros([2*n,n-2])
A = -a/2.0/dx - nu/dx**2
B = -1/dt + 2.0*nu/dx**2
C = a/2.0/dx - nu/dx**2

for i in range(n-2):
    mat[i+1,i] = 1.0/dt
    mat[i+n,i] = cp(A)
    mat[i+n+1,i] = cp(B)
    mat[i+n+2,i] = cp(C)

####################
# reading datasets #
####################
X = pd.read_csv("X.csv", header = None)
Y = pd.read_csv("Y.csv", header = None)

##############################
# Neural Network Development #
##############################

# input layer definition
Uin = tf.keras.Input(shape = (n), name = "Input_layer")

# layer 1 definition
layer1 = tf.keras.layers.Dense(units = 25, activation = act_func, kernel_initializer = kernel_init,
                               bias_initializer = bias_init, name = "layer1")(Uin)

# layer 2 definition
layer2 = tf.keras.layers.Dense(units = 15, activation = act_func, kernel_initializer = kernel_init,
                               bias_initializer = bias_init, name = "layer2")(layer1)

# layer 3 definition
layer3 = tf.keras.layers.Dense(units = 25, activation = act_func, kernel_initializer = kernel_init,
                               bias_initializer = bias_init, name = "layer3")(layer2)

# output layer definition
Uout = tf.keras.layers.Dense(units = 51, activation = act_func, kernel_initializer = kernel_init,
                               bias_initializer = bias_init, name = "output")(layer3)

# concatenation of IP & OP for feeding into Physics-constrained layer
Ypc = tf.keras.layers.concatenate([Uout, Uin], name = "IO_concatenation_layer")

# Physics-constrained layer definition
Ures = tf.keras.layers.Dense(units = 49, activation = abs, trainable = False,
                             kernel_initializer = tf.keras.initializers.constant(mat),
                             bias_initializer = tf.keras.initializers.Zeros(),
                             name = "Phyics_constrained_layer")(Ypc)
# concatenation of OP and residual from physics-constrained layer
Yout = tf.keras.layers.concatenate([Uout,Ures], name = "residual_concatenation_layer")

# model definition
model = tf.keras.Model(inputs = Uin, outputs = Yout)

# model compilation
model.compile(optimizer = optimizer, loss = loss)

##################
# Model Training #
##################

hist = model.fit(X,Y,epochs = epochs, batch_size = batch_size)
model.save("model.h5")

#####################
# Sample Prediction #
#####################
N = 1000
out = model.predict(X.values[N].reshape(1,51))
xc = np.linspace(0,1,n)
plt.plot(xc,Y.values[N,:51],'-b', label = "Actual")
plt.plot(xc,out[0,:51], 'or', label = "ACNet", markerfacecolor = "none")
plt.legend()
plt.show()
