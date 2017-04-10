#! /usr/bin/env python
#
# Simple edge detection testing
#

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read image
img = cv2.imread('ets4.jpg', 0)

# Run threshhold filter
ret, thresh = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY)

# Add blur to fill "holes" in lines
#blur = cv2.blur(img, (10,10))
#kernel = np.ones((10,10),np.float32)/100
#blur = cv2.filter2D(img,-1,kernel)
blur = cv2.medianBlur(thresh, 11)

# Detecte edges
edges = cv2.Canny(blur, 150, 160)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(blur,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()
