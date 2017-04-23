#! /usr/bin/env python
#
# functions to apply model to images
#

import cv2
import tfdata
import tfmodel

import tensorflow as tf


class TFmodel:
    def __init__(self, modelname):
        # create model
        Xsize = tfmodel.Xsize  # number of neurons on input side
        Ysize = tfmodel.Ysize  # number of neurons on output side

        # Define model entry-points
        self.X = tf.placeholder(tf.float32, shape=(None, Xsize))

        weights = tfmodel.genWeights(tfmodel.weightsList)
        self.lineOp = tfmodel.makeModel(self.X, weights)

        saver = tf.train.Saver()
        self.sess = tf.Session()

        saver.restore(self.sess, "./"+modelname)

    def getLines(self, input):
        output = self.sess.run(self.lineOp, feed_dict={self.X: input})
        left, right = output[0][0], output[0][1]
        return left, right


if __name__ == "__main__":
    image = cv2.imread("nn_frames/a12.jpg")
    transformed = tfdata.transform(image)
    array = tfdata.arrayify(transformed)

    tfm = TFmodel("lane-model")
    print(tfm.getLines(array))