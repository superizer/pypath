import numpy as np
import cv2


def threshold(I, thresh_value):
   '''
   Threshold value more than thresh_value to be 255
                   otherwise to be 0
   input: I
   output: I_thresh
   '''
   more    = I > thresh_value
   less    = I <=  thresh_value
   I[more] = 255
   I[less] = 0

   return I

def bitwise_not(I):
   '''
   Toggle value 255 to 0
                0   to 255
   input: I
   output: not_I
   '''

   return 255 - I

def gen_kernels():
   '''
   Generate 4 kernels
   There are |1|0|0| |0|1|0| |0|0|1| |0|0|0|
             |0|1|0| |0|1|0| |0|1|0| |1|1|1|
             |0|0|1| |0|1|0| |1|0|0| |0|0|0|
   output: 4 kernels
   '''
   kernels = []

   kernel    = np.zeros((3, 3), np.uint8)
   for i in range(3):
      for j in range(3):
         if i == j:
            kernel[i][j] = 1
         else:
            kernel[i][j] = 0
   kernels.append(kernel.copy())
   for i in range(3):
      for j in range(3):
         if i + j == 2:
            kernel[i][j] = 1
         else:
            kernel[i][j] = 0
   kernels.append(kernel.copy())
   for i in range(3):
      for j in range(3):
         if i == 1:
            kernel[i][j] = 1
         else:
            kernel[i][j] = 0
   kernels.append(kernel.copy())
   for i in range(3):
      for j in range(3):
         if j == 1:
            kernel[i][j] = 1
         else:
            kernel[i][j] = 0
   kernels.append(kernel.copy())

   return kernels

def find_contour_area(cells_image, contours):
   '''
   Find areas of contours in cells_image
   input: cells_image, contours
   output: contour_areas
   '''
   contour_areas = []
   for c in contours:
      if c.shape[0] > 5:
         x, y, w, h = cv2.boundingRect(c)
         area = np.sum(cells_image[y:y+h,x:x+w])
         contour_areas.append(area)
   return contour_areas