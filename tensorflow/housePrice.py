# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 01:42:34 2020

@author: TSu
"""

#import tensorflow as tf
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

num_house = 160
np.random.seed(42)
house_size = np.random.randint(low=1000,high=3500,size=num_house)

np.random.seed(420)
house_price = 100*house_size + np.random.randint(low=20000,high=70000,size=num_house)

plt.plot(house_size,house_price,'bx')
plt.show()

def normalize(array):
    return (array - array.mean()) / array.std()

num_train_samples = math.floor(num_house * 0.7)
train_house_size = np.asarray(house_size[:num_train_samples])
train_price = np.asarray(house_price[:num_train_samples])

train_house_size_norm = normalize(train_house_size)
train_price_norm = normalize(train_price)

tf_house_size = tf.placeholder("float",name="house_size")
tf_price = tf.placeholder("float",name="price")

tf_size_factor = tf.Variable(np.random.randn(),name="size_factor")
tf_price_offset = tf.Variable(np.random.randn(),name="price_offset")

tf_price_pred = tf.add(tf.multiply(tf_house_size,tf_size_factor),tf_price_offset)

tf_cost = tf.reduce_sum(tf.pow(tf_price_pred-tf_price,2.0))/(2*num_train_samples)
learning_rate = 0.1
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(tf_cost)

init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    tbWriter = tf.summary.FileWriter('./logFile/',sess.graph)
    
    display_every = 2
    num_training_iter = 50
    
    for iteration in range(num_training_iter):
        for (x,y) in zip(train_house_size_norm,train_price_norm):
            sess.run(optimizer, feed_dict={tf_house_size:x, tf_price:y})
        #sess.run(optimizer, feed_dict={tf_house_size:train_house_size_norm, tf_price:train_price_norm})
            
        if (iteration + 1) % display_every == 0:
            c = sess.run(tf_cost, feed_dict={tf_house_size:train_house_size_norm, tf_price:train_price_norm})
            print(c, sess.run(tf_size_factor), sess.run(tf_price_offset))
             
    print("Done")
    c = sess.run(tf_cost, feed_dict={tf_house_size:train_house_size_norm, tf_price:train_price_norm})
    print(c, sess.run(tf_size_factor), sess.run(tf_price_offset))