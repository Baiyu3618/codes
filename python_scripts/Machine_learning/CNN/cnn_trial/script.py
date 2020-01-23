###################################
# CNN script using keras module   #
# classification of dogs and cats #
# developed by Ramkumar           #
###################################

from keras.models import Sequential
from keras.layers import Dense,Flatten,MaxPooling2D,Convolution2D
# from matplotlib.pyplot import imread

# creating keras model----------------------------------------------------------
# initializing sequential cnn
model = Sequential()

# layer 1
model.add(Convolution2D(32,3,3,input_shape=(300,300,3), activation='relu')) # convolution
model.add(MaxPooling2D(pool_size = (2,2))) # pooling

# layer 2
model.add(Convolution2D(32,3,3,input_shape=(300,300,3), activation='relu')) # convolution
model.add(MaxPooling2D(pool_size = (2,2))) # pooling

# flattening
model.add(Flatten())

# feedForward neural network definition
model.add(Dense(output_dim = 128, activation='relu'))
model.add(Dense(output_dim = 1, activation='sigmoid'))

# network compilation
model.compile(optimizer='adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
