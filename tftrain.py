#! /usr/bin/env python
#
# TensorFlow training of neural network
#

import tfdata
import tfmodel

import tensorflow as tf
import random


## Various parameters
lr = 0.01 # learning rate
epochs = 1000 # number of epochs to train


Xsize = tfmodel.Xsize # number of neurons on input side
Ysize = tfmodel.Ysize # number of neurons on output side

## Load dataset
trainX, trainY, testX, testY = tfdata.load("training_label.csv", "test_label.csv")
trainSize = len(trainX)
testSize = len(testX)

#### Generate model ####
# Define model entry-points
X = tf.placeholder(tf.float32, shape=(None, Xsize))
y = tf.placeholder(tf.float32, shape=(None, Ysize))

weights = tfmodel.genWeights(tfmodel.weightsList)
getLines = tfmodel.makeModel(X, weights)

# Define error
#error = - tf.reduce_mean(tf.multiply(y, tf.log(getLines)) + tf.multiply(1 - y, tf.log(1 - getLines)))
error = tf.sqrt(tf.reduce_mean(tf.square(tf.subtract(y, getLines))))
#error = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y, getLines))


optimiser = tf.train.GradientDescentOptimizer(lr).minimize(
    error, var_list=weights.values())

#tf.add_to_collection('lineOp', getLines)
# Generate Op that initialises global variables in the graph
init = tf.global_variables_initializer()

with tf.Session() as sess:
    # Initialise variables and start the session
    sess.run(init)

    for epoch in range(epochs):
        # Pick a random training data
        index = random.randint(0, trainSize-1)

        # Train the network
        sess.run(optimiser, feed_dict={X: trainX[index], y: trainY[index]})

        # Print some data once in a while
        if epoch%100 == 0:
            index = random.randint(0, testSize-1)
            err = sess.run(error, feed_dict={X: testX[index], y: testY[index]})
            yh = sess.run(getLines, feed_dict={X: testX[index], y: testY[index]})
            print("Epoch "+ str(epoch) + " Error: " + str(err) +
                  " Testindex: " + str(index) + " Output: " + str(yh[0][0]) + "  " + str(yh[0][1]))

    # Save model
    saver = tf.train.Saver()
    saver.save(sess, 'lane-model')

del sess
