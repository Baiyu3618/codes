import tensorflow as tf
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

housing = fetch_california_housing()
m,n = housing.data.shape

housing_data_plus_bias = np.c_[np.zeros((m,1)), housing.data]

scaled_housing_data_plus_bias = scaler.fit_transform(housing_data_plus_bias)

n_epochs = 10000
learning_rate = 0.01

X = tf.constant(scaled_housing_data_plus_bias, dtype = tf.float32, name = "X")
y = tf.constant(housing.target.reshape(-1,1), dtype = tf.float32, name = "y")
theta = tf.Variable(tf.random_uniform([n+1,1], -1.0, 1.0), name="theta")

y_pred = tf.matmul(X, theta, name = "prediction")

error = y_pred - y

mse = tf.reduce_mean(tf.square(error), name = "mse")

# gradients = 2.0/m * tf.matmul(tf.transpose(X), error)
# gradients = tf.gradients(mse, [theta])[0]

# training_op = tf.assign(theta, theta - learning_rate * gradients)

optimizer = tf.train.GradientDescentOptimizer(learning_rate = learning_rate)
training_op = optimizer.minimize(mse)

saver = tf.train.Saver()

init = tf.global_variables_initializer()

with tf.Session() as sess:
    init.run()

    for epoch in range(n_epochs):
        if epoch % 100 == 0:
            print("Epoch = ",epoch,"; MSE = ", mse.eval())
        sess.run(training_op)
    best_theta = theta.eval()
    print(best_theta)

    save_path = saver.save(sess,"test.ckpt")
