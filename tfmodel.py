#! /usr/bin/env python
#
# Functions for creating the tensorflow model
#

import tensorflow as tf


Xsize = 32*10 # number of neurons on input side
Ysize = 2 # number of neurons on output side

weightsList = [Xsize, 320, 120, Ysize] # number of neurons per layer


# Create weights
def create_weights(shape):
    # See paper by Xavier Glorot and Yoshua Bengio for more information:
    # "Understanding the difficulty of training deep feedforward neural networks"
    # We employ the Caffe version of the initialiser: 1/(in degree)
    return tf.random_normal(shape, stddev=1/shape[0])


# Generate weights based on a list of desired neurons per layer
def genWeights(wList):
    weights = {}
    prev = wList[0]
    for i in range(1, len(wList)):
        weights['w' + str(i)] = tf.Variable(create_weights((prev, wList[i])), name='w'+str(i))
        weights['b' + str(i)] = tf.Variable(tf.zeros(wList[i]), name='b'+str(i))
        prev = wList[i]

    return weights


# Generate model based on number of weight list and return the last
def makeModel(first, weights):
    nWeights = int(len(weights.values()) / 2)  # remove /2 if no bias weights
    prev = first
    for i in range(1, nWeights + 1):
        prev = tf.nn.relu(tf.matmul(prev, weights['w' + str(i)]) + weights['b' + str(i)], name='m'+str(i))

    return prev
