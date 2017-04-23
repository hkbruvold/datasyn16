#! /usr/bin/env python
#
# Extcact frames from video
#

import imagetools as it
import videotools as vt
import lanelinestools as ll
from moviepy.editor import *
import os
import cv2


def extract(video, times, imagedir, id=""):
    for t in times:
        imgpath = os.path.join(imagedir, id+'{}.jpg'.format(t))
        video.save_frame(imgpath, t)

def processFrames(inDir, outDir):
    files = [f for f in os.listdir(inDir) if os.path.isfile(os.path.join(inDir, f))]

    for file in files:
        image = it.open(os.path.join(inDir, file))
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
        image = image[400:720,0:1280]

        # resize
        image = cv2.resize(image, (32, 10), interpolation = cv2.INTER_LINEAR)

        # threshold again
        image = it.applyThreshold(image, 2)

        cv2.imwrite(os.path.join(outDir, file), image)

def generateData(inDir, outDir, outFile):
    files = [f for f in os.listdir(inDir) if os.path.isfile(os.path.join(inDir, f))]
    outdata = []

    for file in files:
        image = it.open(os.path.join(inDir, file))
        left, right = ll.getLaneLines(image)

        if left == None: left = (0,0,0,0)
        if right == None: right = (0,0,0,0)

        try:
            if left[0] < -200 or left[0] > 300: l = 0
            else: l = (left[0] + 200) / (1280+400)
            if right[0] < 980 or right[0] > 1480: r = 0
            else: r = (right[0] + 200) / (1280+400)
        except:
            continue

        if left[0] == 0 or right[0] == 0 or l == 0 or r == 0:
            continue

        outdata.append("%s,%f,%f\n" %(os.path.join(outDir, file), l, r))

    f = open(outFile, 'a')
    f.writelines(outdata)
    f.close()




v = vt.openVideo('ets3_172.mp4')
times = [i for i in range(0, 172, 1)]

exDir = "nn_frames"
# extract frames
print("Extracting frames...")
#extract(v, times, exDir, "c")

dataDir = "nn_data"
# process frames
print("Processing frames...")
processFrames(exDir, dataDir)

# generate label data
print("Generating label data...")
generateData(exDir, dataDir, "label.csv")