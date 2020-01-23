import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
# from sklearn.datasets import load_sample_image

# loading sample images
# img1 = load_sample_image("image1.jpg")
# img2 = load_sample_image("image2.jpg")
img1 = plt.imread("image1.jpg")
img2 = plt.imread("image2.jpg")


dataset = np.array([img1,img2], dtype = np.float32)
batch_size,height,width,channels = dataset.shape

# creating 2 filters
filters = np.zeros(shape=(7,7,channels,2), dtype = np.float32) # 2 filters for each RGB channel
filters[:,3,:,0] = 1                                           # vertical line
filters[3,:,:,1] = 1                                           # horizontal filter

filters2 = np.zeros(shape=(4,4,channels,2), dtype = np.float32) # 2 filters for each RGB channel
filters2[:,1,:,0] = 1                                           # vertical line
filters2[1,:,:,1] = 1                                           # horizontal filter

# create a graph with input x plus a convolution layer applying 2 filters
X = tf.placeholder(tf.float32, shape=(None, height, width, channels))
step1 = tf.nn.conv2d(X, filters, strides=[1,2,2,1], padding="SAME")

step2 = tf.nn.conv2d(step1, filters2, strides=[1,2,2,1], padding="SAME")


with tf.Session() as sess:
    output = sess.run(step1, feed_dict = {X: dataset})
#

imag1 = output[0,:,:,:]
imag2 = output[1,:,:,:]

plt.close("all")
plt.imshow(imag1)
plt.show()
