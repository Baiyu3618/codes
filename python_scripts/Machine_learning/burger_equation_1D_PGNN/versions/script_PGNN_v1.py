####################################
# Physics-Guided Neural Networks   #
# Solution of 1D Burger's Equation #
# developed by Ramkumar            #
####################################

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["KMP_WARNINGS"] = "FALSE"

import numpy as np
import pandas as pd
import tensorflow as tf

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

# training parameters definition
n_epoch = 100
learning_rate = 1

# graph definition phase--------------------------------------------------------
n_inputs = 52
n_outputs = 51

n_hidden1 = 39
n_hidden2 = 13
n_hidden3 = 39

X = tf.placeholder(tf.float32, shape = (None, n_inputs), name = "X")
Y = tf.placeholder(tf.float32, shape = (None, n_outputs), name = "Y")

x = tf.linspace(0.0,1.0, n_inputs-1) # grid points
pi = tf.constant(np.pi)              # mathematical constant

# constructing DNN
with tf.name_scope("DNN"):
    hidden1 = tf.layers.dense(X, n_hidden1, name = "hidden1", activation = tf.nn.relu, reuse = tf.AUTO_REUSE)
    hidden2 = tf.layers.dense(hidden1, n_hidden2, name = "hidden2", activation = tf.nn.relu, reuse = tf.AUTO_REUSE)
    hidden3 = tf.layers.dense(hidden2, n_hidden3, name = "hidden3", activation = tf.nn.relu, reuse = tf.AUTO_REUSE)
    output = tf.layers.dense(hidden3, n_outputs, name = "output_layer", activation = tf.nn.sigmoid, reuse = tf.AUTO_REUSE)
#

# constructing physics loss function
def F(U,t):
    # gradient function definition for auto-differentiation
    U = 1.0/2/pi/t*tf.sin(2*pi*(x - U*t)) # nothing but the exact solution to burger's equation

    u_t = tf.gradients(U, t)
    u_x = tf.gradients(U, x)
    u_xx = tf.gradients(u_x, x)

    f = u_t + output*u_x - tf.constant(0.1)*u_xx

    return f

# constructing statistical loss function
with tf.name_scope("loss"):
    mse_u = tf.reduce_mean(tf.square(output - Y))
    mse_f = tf.reduce_mean(tf.square(F(output,X[:,:-1])))
    loss = mse_u# + mse_f
#

# training
with tf.name_scope("train"):
    optimizer = tf.train.GradientDescentOptimizer(learning_rate = learning_rate)
    training_op = optimizer.minimize(loss)
#

saver = tf.train.Saver()
init = tf.global_variables_initializer()

# reading data
xdata = pd.read_csv("Xdata.csv", header=None)#, nrows = 1000)
ydata = pd.read_csv("Ydata.csv", header=None)#, nrows = 1000)

# execution phase definition----------------------------------------------------

with tf.Session() as sess:
    init.run()

    for epoch in range(n_epoch):
        sess.run(training_op, feed_dict = {X:xdata, Y:ydata})

        lossVal = loss.eval(feed_dict = {X:xdata, Y:ydata})

        print(epoch," Loss : ",lossVal)
    # savePath = saver.save(sess,"./model.ckpt")
