import numpy as np
import cv2

def select_cell(color_img, contours, con_num):
   '''
   Calculate tiny rectangle that consists only single selected cell
   input: color_img, contours, con_num -> selected contour number
   output: color_cell, binary_cell
   '''
   assert con_num < len(contours), 'Contour out of range'
   height, width, channel = color_img.shape
   
   binary_cell    = np.zeros((height,width), np.uint8)
   cv2.drawContours(binary_cell, [contours[con_num]], -1, 255, -1)
   
   x,y,w,h  = cv2.boundingRect(contours[con_num])
   color_cell  = color_img[y:y+h,x:x+w]
   binary_cell = binary_cell[y:y+h,x:x+w]
   
   return color_cell, binary_cell