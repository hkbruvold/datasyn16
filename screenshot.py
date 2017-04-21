#! /usr/bin/env python
#
# Functions to help with taking screenshot
#

import pyscreenshot as ps
import numpy as np
import cv2

def grab(region):
    return cv2.cvtColor(np.array(ps.grab(bbox=region)), cv2.COLOR_BGR2RGB)