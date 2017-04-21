#! /usr/bin/env python
#
#
#

from moviepy.editor import VideoFileClip

def openVideo(filename):
    return VideoFileClip(filename)

def saveVideo(video, filename):
    video.write_videofile(filename, audio=False)

def applyFilter(video, filterFunction):
    return video.fl_image(filterFunction)

