############################################
# cat dog classification model using keras #
# developed by Ramkumar                    #
############################################

from keras.models import Sequential
from keras.layers import Dense,Flatten,MaxPooling2D,Convolution2D,Conv2D,BatchNormalization, Activation, Dropout
from matplotlib.pyplot import imread
import os,glob, numpy as np
import keras

# reading images----------------------------------------------------------------
traincatfiles = sorted(glob.glob1(os.getcwd()+"/training_set/cats/","*.jpg"))
traindogfiles = sorted(glob.glob1(os.getcwd()+"/training_set/dogs/","*.jpg"))

testcatfiles = sorted(glob.glob1(os.getcwd()+"/test_set/cats/","*.jpg"))
testdogfiles = sorted(glob.glob1(os.getcwd()+"/test_set/dogs/","*.jpg"))

train_size = len(traincatfiles) + len(traindogfiles)
test_size = len(testcatfiles) + len(testdogfiles)
xtrain = np.zeros([train_size,50,50,3]); ytrain = np.zeros([train_size,2])
xtest = np.zeros([test_size,50,50,3]); ytest = np.zeros([test_size,2])

count = 0
for file1,file2 in zip(traincatfiles,traindogfiles):
    xtrain[count,:,:,:] = imread("training_set/cats/"+file1)
    ytrain[count,0] = 1.0         # cat 1,0
    count += 1

    xtrain[count,:,:,:] = imread("training_set/dogs/"+file2)
    ytrain[count,1] = 1.0         # cat 1,0
    count += 1    
#

count = 0
for file1,file2 in zip(testcatfiles,testdogfiles):
    xtest[count,:,:,:] = imread("test_set/cats/"+file1)
    ytest[count,0] = 1.0         # cat 1,0
    count += 1

    xtest[count,:,:,:] = imread("test_set/dogs/"+file2)
    ytest[count,1] = 1.0         # cat 1,0
    count += 1    
#

# model training----------------------------------------------------------------
epoches = 50
batch_size = 50

# CNN Model
model = Sequential()

# ------------------------------------------------------------------------------
# conv 1
model.add(Conv2D(16,(3,3), input_shape=(50,50,3)))
model.add(BatchNormalization(axis=3))
model.add(Activation("relu"))

# max pool 1
model.add(MaxPooling2D(pool_size=(2,2),strides=2))

# ------------------------------------------------------------------------------
# conv 2
model.add(Conv2D(16,(3,3)))
model.add(BatchNormalization(axis=3))
model.add(Activation("relu"))

# max pool 2
model.add(MaxPooling2D(pool_size=(2,2),strides=2))

# ------------------------------------------------------------------------------
# conv 3
model.add(Conv2D(32,(3,3)))
model.add(BatchNormalization(axis=3))
model.add(Activation("relu"))

# max pool 3
model.add(MaxPooling2D(pool_size=(2,2),strides=2))

# ------------------------------------------------------------------------------
# conv 4
model.add(Conv2D(32,(3,3)))
model.add(BatchNormalization(axis=3))
model.add(Activation("relu"))

# max pool 4
model.add(MaxPooling2D(pool_size=(2,2),strides=2))

# ------------------------------------------------------------------------------
# flattening
model.add(Flatten())

# adding dense layer 1
model.add(Dense(512, activation="relu"))

# adding second layer
model.add(Dense(2, activation="softmax"))

# ------------------------------------------------------------------------------
# model compilation
model.compile(loss = "categorical_crossentropy", optimizer="adam", \
              metrics=["accuracy"])

# ------------------------------------------------------------------------------
# fitting the model
hist = model.fit(xtrain,ytrain, batch_size=batch_size,\
                 epochs = epoches, verbose = 1)
# ------------------------------------------------------------------------------
# evaluating the model
score,acc = model.evaluate(xtest,ytest)

print("Score of model : ",score)
print("Accuracy of Model : ",acc*100.0," %")
