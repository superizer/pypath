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

def geometric_distance(filled_img):
   '''
   Calculate geometric distance from binary image.
   The input image consists of white object on black background.
   input: binary image
   output: geometric distance
   '''
   return cv2.distanceTransform(filled_img, cv2.DIST_L2, 3)

def geometric_and_color_gradient_distance(color_img, filled_img):
   '''
   The special distance that combine the geometric distance with the color gradient transform
   from Mouelhi et al. 'A new automatic image analysis method for assessing estrogen receptors’ status in breast tissue specimens'
   input: color image and binary image
   output: special distance that merge geometric distance with color gradeint transform
   '''
   b_img = color_img[:,:,0].copy()
   g_img = color_img[:,:,1].copy()
   r_img = color_img[:,:,2].copy()

   grad_x     = cv2.Sobel(r_img,cv2.CV_64F,1,0,ksize=5)
   grad_y     = cv2.Sobel(r_img,cv2.CV_64F,0,1,ksize=5)
   abs_grad_x = cv2.convertScaleAbs(grad_x)
   abs_grad_y = cv2.convertScaleAbs(grad_y)
   r_grad     = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

   grad_x     = cv2.Sobel(g_img,cv2.CV_64F,1,0,ksize=5)
   grad_y     = cv2.Sobel(g_img,cv2.CV_64F,0,1,ksize=5)
   abs_grad_x = cv2.convertScaleAbs(grad_x)
   abs_grad_y = cv2.convertScaleAbs(grad_y)
   g_grad     = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

   grad_x     = cv2.Sobel(b_img,cv2.CV_64F,1,0,ksize=5)
   grad_y     = cv2.Sobel(b_img,cv2.CV_64F,0,1,ksize=5)
   abs_grad_x = cv2.convertScaleAbs(grad_x)
   abs_grad_y = cv2.convertScaleAbs(grad_y)
   b_grad     = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

   height, width = filled_img.shape

   g = np.zeros((height,width,3), np.uint8)

   g[:,:,0] = b_grad
   g[:,:,1] = g_grad
   g[:,:,2] = r_grad


   g_min = np.min(g)
   g_max = np.max(g)

   g_and_cg_dist = np.zeros((height,width,3), np.uint8)
   g_dist        = geometric_distance(filled_img)

   for i in range(3):
      g_and_cg_dist[:,:,i] = g_dist * np.exp(1 - (g[:,:,i] - g_min)/(g_max - g_min))

   sigma        = 15
   max_d        = np.max(g_and_cg_dist)
   g_and_cg_dist = max_d - g_and_cg_dist 
   g_and_cg_dist = cv2.GaussianBlur(g_and_cg_dist,(sigma,sigma),0)

   cv2.normalize(g_and_cg_dist, g_and_cg_dist, 0, 1, cv2.NORM_MINMAX)

   return g_and_cg_dist
