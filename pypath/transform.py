import numpy as np
import cv2

import skimage.morphology
from skimage.util import img_as_float, img_as_ubyte
import scipy.ndimage as nd


def convert_RGB_to_OD(I_RGB):
   '''
   convert RGB to optical density space
   from eqation I_RGB = 255 * exp(-I_OD)
   input: I_RGB
   output: I_OD
   '''
   mask        = (I_RGB == 0)
   I_RGB[mask] = 1
   return np.maximum(-1 * np.log(I_RGB / 255), 1e-6)


def convert_OD_to_RGB(I_OD):
   '''
   convert optical density space to RGB
   from eqation I_RGB = 255 * exp(-I_OD)
   input: I_OD
   output: I_RGB
   '''
   assert I_OD.min() >= 0, 'Negative optical density'
   I_OD = np.maximum(I_OD, 1e-6)
   return (255 * np.exp(-1 * I_OD)).astype(np.uint8)

def mopho_process(I_GRAY, kernels):
   '''
   Morphological processing based on modified Laplacian filtering
   from A. Mouelhi et al. 'Fast unsupervised nuclear segmentation and classification scheme for automatic allred cancer scoring in immunohistochemical breast tissue images'
   input: I_GRAY, kernels
   output: cells_images
   '''
   dilate_imgs = []
   dilate_sum  = []

   for i, k in enumerate(kernels):
      dilate_img = cv2.dilate(I_GRAY, k)
      dilate_imgs.append(dilate_img.copy())
      dilate_sum.append(np.sum(dilate_img.copy()))

   i = np.argmin(np.array(dilate_sum))
   dilate_img = dilate_imgs[i]

   erosion_imgs = []
   erosion_sum  = []

   for i, k in enumerate(kernels):
      erosion_img = cv2.erode(I_GRAY, k)
      erosion_imgs.append(erosion_img.copy())
      erosion_sum.append(np.sum(erosion_img.copy()))

   i = np.argmax(np.array(erosion_sum))
   erosion_img = erosion_imgs[i]

   inv_img = cv2.bitwise_not(I_GRAY)
   alpha   = 1
   new_img = alpha*(dilate_img - erosion_img) - inv_img



   new_img   = cv2.bitwise_not(new_img)
   kernel    = np.ones((3, 3), np.uint8)
   new_img   = cv2.erode(new_img, kernel)

   

   radius  = 2
   circle  = skimage.morphology.disk(radius)
   new_img    = cv2.bitwise_not(new_img)
   new_img    = img_as_float(new_img)
   close_img  = skimage.morphology.binary_closing(new_img, selem=circle)
   
   filled_img   = nd.morphology.binary_fill_holes(close_img)
   
   close_img    = img_as_ubyte(close_img)
   cells_images = img_as_ubyte(filled_img)

   return cells_images