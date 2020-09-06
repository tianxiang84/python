# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 03:42:50 2020

@author: TSu
"""
import tensorflow as tf

x = tf.Variable(2.0)
with tf.GradientTape() as tape:
    y = x ** 2
print(tape.gradient(y,x))