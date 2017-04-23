#! /usr/bin/env python
#
# Main file for the autosteering
#

import cv2
import matplotlib.pyplot as plt
import os
from os import listdir
from os.path import isfile, join

import lanelinestools
import videotools
import screenshot as ss
import tfdata
from tfapplymodel import TFmodel

windowX = 1
windowY = 28

# Will draw lane lines onto a frame
def addLaneLines(frame):
    left, right = lanelinestools.getLaneLines(frame)

    try:
        if left: cv2.line(frame, (left[0], left[1]), (left[2], left[3]), (0, 0, 255), 5)
        if right: cv2.line(frame, (right[0], right[1]), (right[2], right[3]), (0, 255, 0), 5)
    except:
        print(left, right)
    finally:
        return frame

    return frame

# Draw lane lines obtained from tensorflow model
def tfAddLaneLines(tfm, frame):
    transformed = tfdata.transform(frame)
    array = tfdata.arrayify(transformed)
    left, right = tfm.getLines(array)
    print(left, right)

    # Convert back to pixels
    left = int(left * 1880 - 200)
    right = int(right * 1880 - 200)

    cv2.line(frame, (left, 720), (left, 600), (0, 0, 255), 8)
    cv2.line(frame, (right, 720), (right, 600), (0, 255, 0), 8)

    return frame

# Draw lane lines on all images in folder
def drawFolder(dir):
    files = [f for f in listdir(dir) if isfile(join(dir, f))]

    for file in files:
        image = cv2.imread(dir+file)
        image = addLaneLines(image)
        cv2.imwrite('out/'+file, image)

# Draw lane line on a single image file
def drawFile(filename):
    image = cv2.imread(filename)
    image = addLaneLines(image)
    cv2.imwrite("laned_"+filename, image)

# Grab screenshot and draw lines onto it
def scrDraw():
    while True:
        image = ss.grab((windowX, windowY, windowX + 1280, windowY + 720))

        left, right = lanelinestools.getLaneLines(image)

        if left: print(left[0], end=" ")
        if right: print(right[0], end=" ")
        print()

# Draw lines on all frames of a video file
def drawVideo(filename):
    video = videotools.openVideo(filename)
    laneVideo = videotools.applyFilter(video, addLaneLines)
    videotools.saveVideo(laneVideo, "laned_"+filename)

def tfDrawFolder(tfm, dir):
    files = [f for f in listdir(dir) if isfile(join(dir, f))]

    for file in files:
        image = cv2.imread(os.path.join(dir, file))
        image = tfAddLaneLines(tfm, image)
        cv2.imwrite(os.path.join("tflaned", file), image)


def main():
    #drawFolder("screenshots/")
    #scrDraw()
    #drawVideo("ets2.mp4")
    #drawFile("et.jpg")
    tfm = TFmodel("lane-model")
    tfDrawFolder(tfm, "nn_frames")

if __name__ == "__main__":
    main()
