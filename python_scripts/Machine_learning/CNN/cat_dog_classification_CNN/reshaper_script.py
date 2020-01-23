############################################################
# reshaper script: This script actually reshapes the given #
# image to the required size of 300 by 300 pixels          #
# developed by Ramkumar                                    #
############################################################

import cv2, os, glob, matplotlib.pyplot as plt

# reshaping the train datasets--------------------------------------------------
# dealing with cat files
os.chdir("training_set/cats")
files = glob.glob1(os.getcwd(),"*.jpg")

for file in files:
    img = plt.imread(file)
    tmp = cv2.resize(img,(50,50))
    plt.imsave(file,tmp)
    print("done with file : ",file)

# dealing with dog files
os.chdir("../dogs/")
files = glob.glob1(os.getcwd(),"*.jpg")

for file in files:
    img = plt.imread(file)
    tmp = cv2.resize(img,(50,50))
    plt.imsave(file,tmp)
    print("done with file : ",file)
#
os.chdir("../../")

# # reshaping the test datasets---------------------------------------------------
# # dealing with cat files
# os.chdir("test_set/cats")
# files = glob.glob1(os.getcwd(),"*.jpg")

# for file in files:
#     img = plt.imread(file)
#     tmp = cv2.resize(img,(50,50))
#     plt.imsave(file,tmp)
#     print("done with file : ",file)

# # dealing with dog files
# os.chdir("../dogs/")
# files = glob.glob1(os.getcwd(),"*.jpg")

# for file in files:
#     img = plt.imread(file)
#     tmp = cv2.resize(img,(50,50))
#     plt.imsave(file,tmp)
#     print("done with file : ",file)
# #
# os.chdir("../../")
