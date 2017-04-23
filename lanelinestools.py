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
    #cv2.imwrite("out1_gray.jpg", gray)

    # Apply mask to remove unnecessary information
    masked = it.applyMask(gray, 'mask%i.png'%(resY))
    #cv2.imwrite("out2_masked.jpg", masked)

    # Apply threshold filter
    l = int(0.50*len(masked[0]))
    t = int(0.66*len(masked))
    mean = cv2.mean(gray[t:t+5,l:l+5])[0] # Find mean brightness of road to be used as threshold
    thresh = it.applyThreshold(masked, 2*mean)
    #cv2.imwrite("out3_thresh.jpg", thresh)

    # Apply gaussian blur to "grow" the white lines, and fill salty lane lines
    blur = it.applyBlur(thresh, 11)
    #cv2.imwrite("out4_gauss.jpg", blur)

    # Apply threshold again to get binary image
    thresh2 = it.applyThreshold(blur, 2)
    #cv2.imwrite("out5_thresh2.jpg", thresh2)

    # Apply median filter to remove salt "noise"
    median = it.applyMedianFilter(thresh2, 11)
    #cv2.imwrite("out6_median.jpg", median)

    # Run Canny edge detection to find edges
    edges = it.applyCanny(median, 150, 160)
    #cv2.imwrite("out7_canny.jpg", edges)

    # Find lines from edges using Hough Transform
    lines = it.getHoughLines(edges, 50, 100, 100)

    # Get left and right lines
    left, right = getLeftAndRight(lines)

    # Constrain lines between y=750 and y=1080
    if left: left = constrainLine(left, int(0.7*resY), resY)
    if right: right = constrainLine(right, int(0.7*resY), resY)

    #im = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    #for line in lines:
    #    x1,y1,x2,y2 = line[0]
    #    a = math.atan2(y2-y1,x2-x1)
    #    if a<0:
    #        left = (x1,y1,x2,y2)
    #        cv2.line(im,(x1,y1),(x2,y2),(0,0,255),2)
    #    else:
    #        right = (x1,y1,x2,y2)
    #        cv2.line(im,(x1,y1),(x2,y2),(0,255,0),2)

    #cv2.imwrite("out8_hough.jpg", im)

    return left, right





