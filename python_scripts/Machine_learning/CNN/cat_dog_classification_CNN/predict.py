##################################################
# cat dog classification prediction using keras  #
# developed by Ramkumar                          #
##################################################

from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from matplotlib.pyplot import imread
import os,glob, numpy as np

model = load_model("savefile.h5")
model.load_weights("weights.h5")

model.compile(loss = "binary_crossentropy", optimizer="adam", \
              metrics=["accuracy"])

datagen = ImageDataGenerator()

testfiles = datagen.flow_from_directory("test_set", target_size = (50,50), batch_size = 10, class_mode = "binary", shuffle = False)

score = model.evaluate_generator(testfiles,steps = np.ceil(testfiles.n/10), verbose = 1)

print("evaluation done .. ")
print("loss : ",score[0]," acc : ",score[1])
