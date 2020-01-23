# dummy variables in pandas and how its useful in machine learning
import numpy as np
import pandas as pd
from sklearn import linear_model

""" The main concept of using dummy variables is due to the fact
that, the machine learning stuff works best with numbers only 
not the words, because word arguments are 'nominals' which doesnot 
have any precedence like one is greater/lesser than the other. whereas
numerical arguments are opposite, they have precedence, in order not to 
make machine learining model to sort nominal parameters, the nominal 
parameters are replaced with binary values either 1 or 0.

for example, if there are three object names, A B C, then what the
function pd.get_dummies() does is that it will create additional 
columns in the name of those object names, and each column will 
contain either 1 or 0 correspondingly to take particular 
value over the each record i.e. rows in pandas dataframe"""

# reading the dataset
fid = pd.read_csv("car_prices.csv") # now the dummy variables are not alloted to the dataframe

# alloting dummy variables
dummy_df = pd.get_dummies(fid["Model"]) # here, Model is the column that contains nominal parameters

# for this particular example, the car models names are aligned in alphabetical order
# so the order of columns will be "Audi A5","BMW X5","Mercedes ... "
# and the respective column will contain 1 for its presence in the record and 0 for not present
# so for input of Audi will be [..., 1,0,0], and that of Mercedes will be [...,0,0,1]

# appending the dummy df to original df
added = pd.concat([fid,dummy_df],axis='columns')

# dropping one of the dummy columns along with "Models" columns
df = added.drop(["Model","Mercedez Benz C class"], axis="columns")
# the reason for dropping a dummy is to make the result "not complicated",
# after droping, the result will be like this, for Audi it will be 1,0, for BMW it will be 0,1 and
# for mercedes it will be 0,0.
# the reason for droping Model column is, it is no longer needed

# creating model
reg = linear_model.LinearRegression()

# fitting the data to it i.e. training it
X = df.drop(["Price"], axis="columns") # taking all the feature columns except output i.e. price
Y = df.Price                           # the output column

reg.fit(X,Y)

# now predicting the price of two data sets
# BENZ with 4yrs of age and 45000 mileage
# BMW with 7 yrs of age and 86000 milage

Benz_price = reg.predict([[45000,4,0,0]])
BMW_price = reg.predict([[86000,7,0,1]])

# printing the output
print("Benz Price : ",Benz_price[0])
print("BMW Price : ",BMW_price[0])
print("Accuracy of Model is : ",reg.score(X,Y)*100.0," %")
