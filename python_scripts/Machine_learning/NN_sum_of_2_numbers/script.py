##########################################################################
# Machine learning script to identify the relationship between a pair of #
# numbers and their corresponding result of relationship,                #
# like sum, mean etc.. using tensorflow                                  #
#                                                                        #
# developed by Ramkumar                                                  #
##########################################################################

import tensorflow as tf
import pandas as pd
import numpy as np

# function definitions----------------------------------------------------------
def scale_down(x):
    minval = np.min(x)
    maxval = np.max(x)

    val = (x - minval)/(maxval - minval)

    return minval, maxval, val

def scale_down_t(x):            # scale down function for test inputs
    val = (x-minval)/(maxval - minval) # since the values to be on same scale
    return val

def scale_up(x):
    val = x*(maxval-minval)+minval
    return val

# reading the dataset for training----------------------------------------------
fid = pd.read_csv("Dataset.csv") # X,Y inputs Z output
Xtest = [[1,2]]                  # test dataset

minval, maxval, matrix = scale_down(fid.values)

mat = scale_down_t(Xtest)

# Y = matrix[:,2]
Y = matrix[:,2].reshape(fid.shape[0],1)
X = matrix[:,0:2]

# machine learning parameters setup---------------------------------------------
eta = 0.5
iteration = 10000

# tensorflow parameters setup---------------------------------------------------
# layer 0 input 
y = tf.compat.v1.placeholder(tf.float32, shape=(None))
x = tf.compat.v1.placeholder(tf.float32, shape=(None,2))
xt = tf.constant([[1,2]], dtype=tf.float32)

# layer 1 hidden 1
w1 = tf.Variable(tf.random_uniform([2,3], \
                        minval=0.1, maxval=0.9, dtype=tf.float32))
b1 = tf.Variable(tf.random_uniform([3], \
                        minval=0.1, maxval=0.9, dtype=tf.float32))
h1 = tf.tanh(tf.matmul(x,w1)+b1)

# layer 2 hidden 2
w2 = tf.Variable(tf.random_uniform([3,1], \
                        minval=0.1, maxval=0.9, dtype=tf.float32))
b2 = tf.Variable(tf.random_uniform([1], \
                        minval=0.1, maxval=0.9, dtype=tf.float32))
out = tf.tanh(tf.matmul(h1,w2)+b2)

# cost function
cost = tf.reduce_mean(tf.square(y-out))

# training function
train = tf.train.GradientDescentOptimizer(eta).minimize(cost)

# accuracy testing
error = abs(y - out)/y * 100.0

# output test
ho = tf.tanh(tf.matmul(xt,w1)+b1)
output = tf.tanh(tf.matmul(ho,w2)+b2)

fd = {y:Y, x:X}

# tensorflow initialization for training----------------------------------------
with tf.Session() as sess:
    # initializing all variables
    sess.run(tf.global_variables_initializer())

    # training the model
    for itr in range(iteration):
        sess.run(train, feed_dict=fd)
        print("Iteration : ",itr," Cost : ",sess.run(cost, feed_dict=fd))
    #
    # print("\n\n trained output : ")
    # print(scale_up(sess.run(out, feed_dict=fd)))
    print("\n\n Maximum Model Error Percentage : ")
    print(np.max(sess.run(error, feed_dict=fd)))

    print("\n\n Trial Output : ", scale_up(sess.run(output)))
