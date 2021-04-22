import cv2
import numpy as np
from tqdm import tqdm

def get_pixel(img, center, x, y):
   '''
   from https://github.com/arsho/local_binary_patterns
   '''
   new_value = 0
   try:
      if img[x][y] >= center:
         new_value = 1
   except:
      pass
   return new_value

def lbp_calculated_pixel(img, x, y):
   '''
    from https://github.com/arsho/local_binary_patterns
     64 | 128 |   1
    ----------------
     32 |   0 |   2
    ----------------
     16 |   8 |   4    
   '''    
   center = img[x][y]
   val_ar = []
   val_ar.append(get_pixel(img, center, x-1, y+1))     # top_right
   val_ar.append(get_pixel(img, center, x, y+1))       # right
   val_ar.append(get_pixel(img, center, x+1, y+1))     # bottom_right
   val_ar.append(get_pixel(img, center, x+1, y))       # bottom
   val_ar.append(get_pixel(img, center, x+1, y-1))     # bottom_left
   val_ar.append(get_pixel(img, center, x, y-1))       # left
   val_ar.append(get_pixel(img, center, x-1, y-1))     # top_left
   val_ar.append(get_pixel(img, center, x-1, y))       # top
    
   power_val = [1, 2, 4, 8, 16, 32, 64, 128]
   val = 0
   for i in range(len(val_ar)):
      val += val_ar[i] * power_val[i]
   return val  

def cal_lbp(I_BGR):
   '''
   Local Binary Pattern (LBP)
   from https://github.com/arsho/local_binary_patterns
   input: I_BGR
   output: I_LBP
   '''
   I_GRAY           = cv2.cvtColor(I_BGR, cv2.COLOR_BGR2GRAY)
   height, width, _ = I_BGR.shape

   I_LBP = np.zeros((height, width,3), np.uint8)

   print('Calculate LBP ...')
   for i in tqdm(range(0, height)):
      for j in range(0, width):
         I_LBP[i, j] = lbp_calculated_pixel(I_GRAY, i, j)
   
   return I_LBP