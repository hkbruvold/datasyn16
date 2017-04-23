#! /usr/bin/env python
#
# helper functions for loading data for neural network
#

import imagetools as it

import numpy as np
import cv2


# Transform 720p image to be used in neural network
def transform(image):
    image = it.toGrayscale(image)
    image = it.applyMask(image, 'mask720.png')

    # Apply threshold filter
    l = int(0.50 * len(image[0]))
    t = int(0.66 * len(image))
    mean = cv2.mean(image[t:t + 5, l:l + 5])[0]  # Find mean brightness of road to be used as threshold
    image = it.applyThreshold(image, 2 * mean)

    image = it.applyBlur(image, 11)
    image = it.applyThreshold(image, 2)
    image = it.applyMedianFilter(image, 11)

    # crop
    image = image[400:720, 0:1280]

    # resize
    image = cv2.resize(image, (32, 10), interpolation=cv2.INTER_LINEAR)

    # threshold again
    image = it.applyThreshold(image, 2)

    return image


# Convert image to np.array
def arrayify(image):
    im = image.flatten()
    cond = im == 255
    im[cond] = 1

    return np.reshape(im,(-1, 32*10))


# Extract data from lines
def extractData(lines):
    X = []
    Y = []
    for line in lines:
        l = line.split(',')

        # load image, flatten, and convert to 1 or 0
        im = cv2.imread(l[0], 0)
        X.append(arrayify(im))

        # load answer
        left = float(l[1])
        right = float(l[2])

        Y.append(np.array([[left, right]]))

    return X, Y


# Load test and training data and return X and Y for tensorflow
def load(traingfile, testfile):
    ## Read training data
    f = open(traingfile, 'r')
    lines = f.readlines()
    f.close()

    trainX, trainY = extractData(lines)

    ## Read test data
    f = open(testfile, 'r')
    lines = f.readlines()
    f.close()

    testX, testY = extractData(lines)

    return np.array(trainX), np.array(trainY), np.array(testX), np.array(testY)







