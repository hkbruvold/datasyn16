#! /usr/env/python
#
# Various functions to apply filters on image
#

import cv2
import numpy as np


def open(filename):
    return cv2.imread(filename)

def toGrayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def applyThreshold(image, threshold):
    ret, thresh = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    return thresh

def applyMedianFilter(image, kernelSize):
    return cv2.medianBlur(image, kernelSize)

def applyBlur(image, kernelSize):
    return cv2.GaussianBlur(image, (kernelSize, kernelSize), 0)

def applyMask(image, maskFilename):
    mask = cv2.imread(maskFilename, 0)
    return cv2.bitwise_and(image, image, mask=mask)

def applyCanny(image, thresh1, thresh2):
    return cv2.Canny(image, thresh1, thresh2)

def getHoughLines(image, threshold, minLineLength, maxLineGap):
    return cv2.HoughLinesP(image, 1, np.pi/180, threshold, minLineLength=minLineLength, maxLineGap=maxLineGap)


