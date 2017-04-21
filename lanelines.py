#! /usr/bin/env python
#
# Contains functions to find lane lines from an image
#

import imagetools as it
import cv2
import math

resY = 720 # Resolution in Y direction

def getLeftAndRight(lines):
    # Get one line for each side
    left, right = None, None
    try:
        for line in lines:
            x0, y0, x1, y1 = line[0]
            angle = math.atan2(y1 - y0, x1 - x0)
            if angle < 0:  # A left line
                left = (x0, y0, x1, y1)
            else:  # A right line
                right = (x0, y0, x1, y1)
    except:
        print("Warning: Found no lines")
        print(lines)
        return None, None

    return left, right

def constrainLine(line, upperY, lowerY):
    x0, y0, x1, y1 = line

    if (x1 == x0):
        return ((x1, x0), (x1, y0))
    angle = (y1 - y0)/(x1 - x0)

    if angle == 0:
        angle = 1

    lowerX = int((lowerY - y0) / angle + x0)
    upperX = int((upperY - y0) / angle + x0)

    return lowerX, lowerY, upperX, upperY

def getLaneLines(image):
    # Convert to grayscale
    gray = it.toGrayscale(image)

    # Apply mask to remove unnecessary information
    masked = it.applyMask(gray, 'mask%i.png'%(resY))

    # Apply threshold filter
    l = int(0.50*len(masked[0]))
    t = int(0.66*len(masked))
    mean = cv2.mean(gray[t:t+5,l:l+5])[0] # Find mean brightness of road to be used as threshold
    thresh = it.applyThreshold(masked, 2*mean)

    # Apply gaussian blur to "grow" the white lines, and fill salty lane lines
    blur = it.applyBlur(thresh, 11)

    # Apply threshold again to get binary image
    thresh2 = it.applyThreshold(blur, 2)

    # Apply median filter to remove salt "noise"
    median = it.applyMedianFilter(thresh2, 11)

    # Run Canny edge detection to find edges
    edges = it.applyCanny(median, 150, 160)

    # Find lines from edges using Hough Transform
    lines = it.getHoughLines(edges, 50, 100, 100)

    # Get left and right lines
    left, right = getLeftAndRight(lines)

    # Constrain lines between y=750 and y=1080
    if left: left = constrainLine(left, int(0.7*resY), resY)
    if right: right = constrainLine(right, int(0.7*resY), resY)

    return left, right





