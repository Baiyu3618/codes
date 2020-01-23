###########################################
# damped sine wave problem solved by LSTM #
# developed by Ramkumar                   #
###########################################

from math import sin, pi,exp
import matplotlib.pyplot as plt
from numpy.random import randint, uniform
from numpy import array
from keras.models import Sequential
from keras.layers import LSTM, Dense

# damped sine wave function
def generate_sequence(length, period, decay):
    return [0.5 + 0.5*sin(2 * pi * i/period) * exp(-decay * i) for i in range(length)]

# exmples generator
def generate_examples(length, n_patterns, output):
    X, y = list(), list()

    for _ in range(n_patterns):
        p = randint(10,20)
        d = uniform(0.01, 0.1)
        sequence = generate_sequence(length + output, p,d)
        X.append(sequence[:-output])
        y.append(sequence[-output:])
    X = array(X).reshape(n_patterns, length, 1)
    y = array(y).reshape(n_patterns, output)

    return X,y

# configure problem
length = 50
output = 5

# define model
model = Sequential()
model.add(LSTM(20, return_sequences = True, input_shape = (length,1)))
model.add(LSTM(20))
model.add(Dense(output))

model.compile(loss = "mse", optimizer = "adam", metrics = ["acc"])

# fit model
X,y = generate_examples(length, 10000, output)
model.fit(X,y,batch_size = 10, epochs = 1, verbose = 1)

# evaluate model
X,y = generate_examples(length, 1000, output)
loss = model.evaluate(X,y, verbose = 1)
print("loss ",loss)

# make predictions
X,y = generate_examples(length, 1, output)
yhat = model.predict(X, verbose = 1)

plt.plot(y[0], label = "Y")
plt.plot(yhat[0], label = "Yhat")
plt.legend()
plt.show()
