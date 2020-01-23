############################################
# cat dog classification model using keras #
# developed by Ramkumar                    #
############################################

from keras.models import Sequential
from keras.layers import Dense,Flatten,MaxPooling2D,Convolution2D,Conv2D,BatchNormalization, Activation, Dropout
from keras.preprocessing.image import ImageDataGenerator
from matplotlib.pyplot import imread
import os,glob, numpy as np
import keras

# model training----------------------------------------------------------------
epoches = 50
batch_size = 50

# CNN Model
model = Sequential()

# ------------------------------------------------------------------------------
# conv 1
model.add(Conv2D(16,(3,3), input_shape=(50,50,3)))
# model.add(BatchNormalization(axis=3))
model.add(Activation("relu"))

# max pool 1
model.add(MaxPooling2D(pool_size=(2,2),strides=2))

# ------------------------------------------------------------------------------
# conv 2
model.add(Conv2D(16,(3,3)))
# model.add(BatchNormalization(axis=3))
model.add(Activation("relu"))

# max pool 2
model.add(MaxPooling2D(pool_size=(2,2),strides=2))

# ------------------------------------------------------------------------------
# conv 3
model.add(Conv2D(32,(3,3)))
# model.add(BatchNormalization(axis=3))
model.add(Activation("relu"))

# max pool 3
model.add(MaxPooling2D(pool_size=(2,2),strides=2))

# ------------------------------------------------------------------------------
# conv 4
model.add(Conv2D(32,(3,3)))
# model.add(BatchNormalization(axis=3))
model.add(Activation("relu"))

# max pool 4
model.add(MaxPooling2D(pool_size=(2,2),strides=2))

# ------------------------------------------------------------------------------
# flattening
model.add(Flatten())

# adding dense layer 1
model.add(Dense(512, kernel_initializer="normal", activation="relu"))

# adding second layer
# model.add(Dense(2, activation="softmax"))
model.add(Dense(1, activation="sigmoid"))

# ------------------------------------------------------------------------------
# model compilation
# model.compile(loss = "categorical_crossentropy", optimizer="adam", \
#               metrics=["accuracy"])
model.compile(loss = "binary_crossentropy", optimizer="adam", \
              metrics=["accuracy"])

# ------------------------------------------------------------------------------
# reading image data for training
img = ImageDataGenerator()
traindata = img.flow_from_directory("training_set/",target_size=(50,50),\
                                    batch_size = 50, class_mode = "binary")

# ------------------------------------------------------------------------------
# fitting the model
hist = model.fit_generator(traindata, epochs = epoches, verbose = 1,\
                           steps_per_epoch = np.ceil(traindata.n/batch_size))

# ------------------------------------------------------------------------------
# saving the model
model.save_weights("weights.h5")
model.save('savefile.h5')

print("models saved..")

# ------------------------------------------------------------------------------
# reading image data for testing
img2 = ImageDataGenerator()
testfiles = img2.flow_from_directory("test_set/",target_size=(50,50),\
                                    batch_size = 10, class_mode = "binary")

score = model.evaluate_generator(testfiles,steps = np.ceil(testfiles.n/10),\
                                 verbose = 1)
print("evaluation done .. ")
print("loss : ",score[0]," acc : ",score[1])
