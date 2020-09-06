import tensorflow.compat.v1 as tf
#from tensorflow.compat.v1.examples.tutorials.mnist import input_data

mnist = tf.keras.datasets.mnist
#mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

with tf.Session() as sess:
    x = tf.placeholder(tf.float32,shape=[None,784])
    W = tf.Variable(tf.zeros([784,10]))
    b = tf.Variable(tf.zeros([10]))
    y = tf.nn.softmax(tf.matmul(x,W) + b)
    
    y_ = tf.placeholder(tf.float64,shape=[None,10])
    
    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
    
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
    
    sess.run(tf.global_variables_initializer())
    
    for i in range(1000):
        batch_xs, batch_ys = 