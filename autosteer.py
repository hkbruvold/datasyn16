#! /usr/bin/env python
#
# Main file for the autosteering
#

import cv2
import matplotlib.pyplot as plt

import lanelines
import videotools
import screenshot as ss

#image = cv2.imread('ets3.jpg')
image = ss.grab((22,90,22+1280,90+720))

left, right = lanelines.getLaneLines(image)

print(left, right)
if left: cv2.line(image, (left[0],left[1]), (left[2],left[3]), (0,0,255),5)
if right: cv2.line(image, (right[0],right[1]), (right[2],right[3]), (0,255,0),5)

plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.show()
"""
def addLaneLines(frame):
    left, right = lanelines.getLaneLines(frame)

    try:
        if left: cv2.line(frame, (left[0], left[1]), (left[2], left[3]), (0, 0, 255), 5)
        if right: cv2.line(frame, (right[0], right[1]), (right[2], right[3]), (0, 255, 0), 5)
    except:
        print(left, right)
    finally:
        return frame

    return frame

video = videotools.openVideo("ets.mp4")
laneVideo = videotools.applyFilter(video, addLaneLines)
videotools.saveVideo(laneVideo, "ets_laned.mp4")
"""