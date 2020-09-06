# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tensorflow as tf

#tf.compat.v1.enable_eager_execution() #enable_eager_execution()

a = tf.constant(1,dtype='float32',shape=[],name='a')
print(a.dtype)
b = tf.constant(2,dtype='float32',shape=[],name='b')
print(b)
c = tf.add(a,b,name='c')
print(c)

tf.compat.v1.disable_eager_execution()
#tf.compat.v1.enable_eager_execution()
print(tf.compat.v1.executing_eagerly())
tf.compat.v1.reset_default_graph()

sess = tf.compat.v1.Session()
a = tf.constant(1,dtype='float32',shape=[],name='a')
print(a.dtype)
b = tf.constant(2,dtype='float32',shape=[],name='b')
print(b)
c = tf.add(a,b,name='c')
print(c)
print(sess.run(c))
print(c)
sess.close()

# with tf.compat.v1.Session() as sess:
#     a = tf.constant(20)
#     b = tf.constant(22)
#     print(sess.run(a+b))
    
#     hello = tf.constant("hello from TS")
#     print(sess.run(hello))

