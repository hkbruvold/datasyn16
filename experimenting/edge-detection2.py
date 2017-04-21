#! /usr/bin/env python
#
# Simple edge detection testing
# Now with hough transform
#

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read image
img = cv2.imread('ets.jpg')

# Convert to gray scale
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# Run threshhold filter
ret, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

# Add blur to fill "holes" in lines
#blur = cv2.blur(img, (10,10))
#kernel = np.ones((10,10),np.float32)/100
#blur = cv2.filter2D(img,-1,kernel)
blur = cv2.medianBlur(thresh, 11)

# Detecte edges
edges = cv2.Canny(blur, 150, 160)

# Hough transform
minLineLength = 10
maxLineGap = 10
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)

# Draw lines from hough transform
for line in lines:
    x1,y1,x2,y2 = line[0]
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),5)
    cv2.line(edges,(x1,y1),(x2,y2),(0,255,0),5)

plt.subplot(121),plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

#plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#cv2.imshow('image',img)
cv2.imwrite('houghlines5.jpg',img)
plt.show()
