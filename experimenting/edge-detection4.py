#! /usr/bin/env python
#
# Simple edge detection testing
# Now with hough transform
# And trapeziodal filter
# And find the two lines that matter
#

import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

# Read image
img = cv2.imread('ets3.jpg')

# Open mask
mask = cv2.imread('mask720.png', 0)

# Convert to gray scale
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

l = int(0.50*len(gray[0]))
t = int(0.66*len(gray))
m = cv2.mean(gray[t:t+5,l:l+5])[0]
print(2*m)
# Run threshhold filter
ret, thresh = cv2.threshold(gray, 2*m, 255, cv2.THRESH_BINARY)
#thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 7, 5)

# Run another blur
blur2 = cv2.GaussianBlur(thresh, (11, 11), 0)

# Then a new threshold filter
ret, thresh2 = cv2.threshold(blur2, 2, 255, cv2.THRESH_BINARY)


# Add blur to fill "holes" in lines
#blur = cv2.blur(img, (10,10))
#kernel = np.ones((10,10),np.float32)/100
#blur = cv2.filter2D(img,-1,kernel)
blur = cv2.medianBlur(thresh2, 11)


# Apply mask to image
masked = cv2.bitwise_and(blur, blur, mask=mask)

# Detecte edges
edges = cv2.Canny(masked, 150, 160, apertureSize=3)

# Hough transform
minLineLength = 70
maxLineGap = 100
lines = cv2.HoughLinesP(edges,1,np.pi/180,50,minLineLength=minLineLength,maxLineGap=maxLineGap)
#lines = cv2.HoughLines(edges,1,np.pi/180,700)


# Draw lines from hough transform
if lines != None:
    for line in lines:
        x1,y1,x2,y2 = line[0]
        a = math.atan2(y2-y1,x2-x1)
        if a<0:
            left = (x1,y1,x2,y2)
            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
        else:
            right = (x1,y1,x2,y2)   
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
        
        #print(x2-x1,y2-y1, math.atan2(y2-y1,x2-x1))
else:
    print("NO LINES FOUND")


#cv2.line(img,(left[0],left[1]),(left[2],left[3]), (0,0,255),2)
#cv2.line(img,(right[0],right[1]),(right[2],right[3]), (0,255,0),2)


#plt.subplot(121),plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#plt.title('Original Image'), plt.xticks([]), plt.yticks([])
#plt.subplot(122),plt.imshow(edges,cmap = 'gray')
#plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

#plt.imshow(blur, cmap='gray')
#plt.imshow(thresh2, cmap='gray')
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#cv2.imshow('image',img)
cv2.imwrite('houghlines5.jpg',img)
plt.show()
