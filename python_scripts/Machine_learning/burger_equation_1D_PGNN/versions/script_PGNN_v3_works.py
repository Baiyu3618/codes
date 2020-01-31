#!/home/ramkumar/Public/anaconda/bin/python

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
import matplotlib.pyplot as plt

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

# training parameters definition
n_epoch = 100000
learning_rate = 0.01

# graph definition phase--------------------------------------------------------
n_inputs = 52
n_outputs = 51

n_hidden1 = 39
n_hidden2 = 13
n_hidden3 = 39

x = tf.placeholder(tf.float32, shape = (None, n_inputs - 1), name = "x")
t = tf.placeholder(tf.float32, shape = (None, 1), name = "t")
Y = tf.placeholder(tf.float32, shape = (None, n_outputs), name = "Y")

pi = tf.constant(np.pi)              # mathematical constant

# constructing DNN
with tf.name_scope("DNN"):
    X = tf.concat([x,t], 1)
    hidden1 = tf.layers.dense(X, n_hidden1, name = "hidden1", activation = tf.nn.tanh, reuse = tf.AUTO_REUSE)
    hidden2 = tf.layers.dense(hidden1, n_hidden2, name = "hidden2", activation = tf.nn.tanh, reuse = tf.AUTO_REUSE)
    hidden3 = tf.layers.dense(hidden2, n_hidden3, name = "hidden3", activation = tf.nn.tanh, reuse = tf.AUTO_REUSE)
    output = tf.layers.dense(hidden3, n_outputs, name = "output_layer", activation = tf.nn.tanh, reuse = tf.AUTO_REUSE)
#

# constructing physics loss function
def F(U,t):

    u_t = tf.gradients(U, t)
    u_x = tf.gradients(U, x)
    u_xx = tf.gradients(u_x, x)

    f = u_t + U*u_x - tf.constant(0.01)*u_xx

    return f

# constructing statistical loss function
with tf.name_scope("loss"):
    mse_u = tf.reduce_mean(tf.square(output - Y))
    mse_f = tf.reduce_mean(tf.square(F(output, t)))
    loss = mse_f + mse_u
#

# training
with tf.name_scope("train"):
    optimizer = tf.train.GradientDescentOptimizer(learning_rate = learning_rate)
    training_op = optimizer.minimize(loss)
#

saver = tf.train.Saver()
init = tf.global_variables_initializer()

# reading data
xdata = pd.read_csv("xdata.csv", header=None).values
ydata = pd.read_csv("ydata.csv", header=None).values

# fixing prediction values
n = -1
X_predict = np.reshape(xdata[n,:], [1,xdata.shape[1]])
y_act = ydata[n,:]

# execution phase definition----------------------------------------------------

with tf.Session() as sess:
    init.run()

    for epoch in range(n_epoch):
        sess.run(training_op, feed_dict = {x:xdata[:,0:51], t:xdata[:,51].reshape(1000,1), Y:ydata})

        lossVal = loss.eval(feed_dict = {x:xdata[:,0:51], t:xdata[:,51].reshape(1000,1), Y:ydata})

        print(epoch," Loss : ",lossVal)
    savePath = saver.save(sess,"./model.ckpt")

    # saver.restore(sess, "./model.ckpt")
    U_pred = output.eval(feed_dict = {x:X_predict[:,0:51], t:X_predict[:,51].reshape(1,1), Y:ydata})
#

# prediction error computation
error_pred = np.mean((y_act - U_pred)**2) * 100

plt.close("all")
fid,ax = plt.subplots()
ax.plot(X_predict[0,0:n_inputs-1], y_act,'-b', label = "Numerical result")
ax.plot(X_predict[0,0:n_inputs-1], U_pred.reshape(n_inputs-1),'*r', label = "PGNN result")
plt.xlabel("x-location")
plt.ylabel("U")
ax.legend(loc='lower left', bbox_to_anchor= (0.0, 1.01), ncol=2, borderaxespad=0, frameon=False)
plt.savefig("comparison.png", dpi = 300)
plt.close()

print("Error in prediction : ",error_pred,"%")
