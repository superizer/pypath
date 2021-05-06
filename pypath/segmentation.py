import cv2
import numpy as np

import scipy.ndimage as nd
from skimage.segmentation import watershed

def watershed_from_marker_to_boundary(binary_marker, binary_cell):
   '''
   Watersheding cells starting from the binary_marker to boundary from binary_cell
   input: binary_cell, binary_marker
   output: labels
   '''
   dist_img = cv2.distanceTransform(binary_cell, cv2.DIST_L2, 3)
   cv2.normalize(dist_img, dist_img, 0, 1.0, cv2.NORM_MINMAX)

   mask = np.zeros(binary_marker.shape, dtype=bool)
   mask[binary_marker == 255] = True
   markers, num_marker = nd.label(mask)

   bg_mark = np.zeros(binary_cell.shape, dtype=bool)
   bg_mark[binary_cell == 255] = True 
   bg_mark[binary_cell != 255] = False

   labels = watershed(-dist_img, markers, mask=bg_mark)
   
   return num_marker, labels