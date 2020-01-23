################################################################
# Script to test the Simple Linear Regression Class            #
#                                                              #
# developed by     : Ramkumar                                  #
#                                                              #
# test data source : https://www.kaggle.com/mohochirps/test123 #
################################################################

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from SLRClass import Linear_Regression

# reading the data
fid = pd.read_csv("data.csv")

# spliting the dataset for training and testing
Xtrain, Xtest, Ytrain, Ytest = train_test_split(fid.x, fid.y)

# initializing/training the model
model = Linear_Regression(Xtrain, Ytrain)

# predicting the output of test data
y_predict = model.predict(Xtest)

# computing accuracy of model for current dataset
accuracy = model.accuracy(Xtest, Ytest)

# plotting the predicted and actual output, along with given data
plt.figure()                    # printing given data
plt.plot(fid.x, fid.y, '*r')
plt.xlabel("X Data")
plt.ylabel("Y Data")
plt.title("Given Dataset")
plt.savefig("GivenData.png", dpi = 300)
plt.close()

plt.figure()
plt.plot(Xtest, Ytest, '*b', label="actual data")
plt.plot(Xtest, y_predict, '*r', label='predicted data')
plt.xlabel("X data")
plt.ylabel("Y data")
plt.title("Actual vs Predicted Data Plot")
plt.legend()
plt.savefig("ActualVsPredictedData.png", dpi = 300)
plt.close()

# printing the accuracy of the model
print("\n\n\n Accuracy of the Model for given dataset : ", accuracy," %")
