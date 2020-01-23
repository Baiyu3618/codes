#######################################################
# Iris dataset classifier using neural networks       #
# with tensorflow                                     #
# dataset source=https://gist.github.com/netj/8836201 #
#                                                     #
# developed by Ramkumar                               #
#######################################################

import tensorflow as tf
import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split

# functions definition section--------------------------------------------------
def scale_down(x):
    maxval, minval = np.max(x), np.min(x)
    val = (x - minval)/(maxval - minval)
    return val

def organizer(x):
    # simplyfies output by taking maximum value as chosen one
    r,c = np.shape(x)
    val = np.zeros([r,c])
    for i in range(r):
        maxval = np.max(x[i][:])
        for j in range(c):
            if x[i][j] == maxval:
                val[i][j] = 1.0
            #
        #
    #
    return val

# manipulating dataset to fit NN -----------------------------------------------
cols = ["sl","sw","pl","pw","t"]
fid = pd.read_csv("iris.csv", names=cols, skiprows=1)   # reading the dataset

dummies = pd.get_dummies(fid["t"]) # getting dummy variables for "type" column

fid = pd.concat([fid,dummies], axis="columns") # concatenating with old frame

fid.drop("t",axis="columns",inplace=True) # dropping "type" column

fid.columns = ["sl","sw","pl","pw","t1","t2","t3"] # renaming columns \
              # t1 - setosa, t2 - versicolor, t3 - virginica

x = fid[["sl","sw","pl","pw"]]  # spliting input and output data
y = fid[["t1","t2","t3"]]

xtrain,xtest,ytrain,ytest = train_test_split(x,y,test_size = 0.2)

# neural network parameters-----------------------------------------------------
eta = 1                       # learning rate
iteration = 50000                 # no of iterations

# tensorflow parameters setup---------------------------------------------------

# chosen neural network shape
# 4(input) --> 4(hidden) --> 3(output)

# layer 0: input
xt = tf.placeholder(dtype = tf.float32, shape=(None,4))
yt = tf.placeholder(dtype = tf.float32, shape=(None,3))

xt2= tf.placeholder(dtype = tf.float32, shape=(None,4)) # for testing

# layer 1: hidden
w1 = tf.Variable(tf.random_uniform([4,6], dtype=tf.float32))
b1 = tf.Variable(tf.random_uniform([6], dtype=tf.float32))
h1 = tf.tanh(tf.matmul(xt,w1) + b1)

# layer 2: output
w2 = tf.Variable(tf.random_uniform([6,3], dtype=tf.float32))
b2 = tf.Variable(tf.random_uniform([3], dtype=tf.float32))
out = tf.tanh(tf.matmul(h1,w2) + b2)

# cost function definition
cost = tf.reduce_mean(tf.square(yt-out))

# gradient descent function for training
train = tf.train.GradientDescentOptimizer(eta).minimize(cost)

# feed dictionary for training
fd = {xt:xtrain, yt:ytrain}

# feed dictionary for testing
fd2 = {xt2:xtest, yt:ytest}

# testing parameters
ho = tf.tanh(tf.matmul(xt2,w1) + b1)
output = tf.tanh(tf.matmul(ho,w2) + b2)

# training the tensorflow model-------------------------------------------------
with tf.Session() as sess:
    # initializing all variables 
    sess.run(tf.global_variables_initializer())

    print("Iterating ... ")

    for itr in range(iteration):
        sess.run(train, feed_dict = fd)

        # print("iteration : ",itr," cost : ",sess.run(cost, feed_dict=fd))
    #
    print("iteration completed.. cost function = ",sess.run(cost, feed_dict=fd))

    # testing
    print("\n\n Test output = \n",organizer(scale_down(sess.run(output, feed_dict=fd2))))
