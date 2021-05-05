
import cv2
import numpy as np
from skimage.morphology import h_maxima

def remove_intersec(components_A, components_B, size=1):
   '''
   Remove intersection regions between components_A and components_B
   input: components_A, components_B
   return: selected_components
   '''
   intersec_components = cv2.bitwise_and(components_A, components_B)
   intersec_components[intersec_components == 255] = 1

   nb_components, output = cv2.connectedComponents(components_B)
   selected_components = np.zeros((output.shape), np.uint8)

   for i in range(0, nb_components-1):
      components_B = np.zeros((output.shape), np.uint8)
      components_B[output == i + 1] = intersec_components[output == i + 1]
      if np.sum(components_B) < size:
         selected_components[output == i + 1] = 255

   return selected_components

def eliminate_small(image, min_size):
   '''
   Eliminate small regions that larger or equal to min_size
   input: image,min_size
   output:large_components
   '''
   nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(image)
   sizes = stats[1:, -1]; nb_components = nb_components - 1

   large_components = np.zeros((output.shape), np.uint8)
   for i in range(0, nb_components):
      if sizes[i] >= min_size:
         large_components[output == i + 1] = 255
   return large_components

def iterative_h_minima(RGB_distance):
   '''
   Iterative H-Minima 
   from Koyuncu et al. 'Iterative H-Minima-Based Marker-Controlled Watershed for Cell Nucleus Segmentation'
   input: RGB_distance
   output: markers
   '''
   h,w,c   = RGB_distance.shape
   maxima  = np.zeros((h,w), np.uint8)
   dist_img = cv2.cvtColor(RGB_distance*255, cv2.COLOR_BGR2GRAY)

   dist_img = cv2.bitwise_not(dist_img)

   h_adp1 = 1
   H_adp1 = h_maxima(dist_img, h=h_adp1)
   H_adp1 = H_adp1*255

   h_adp2 = 2
   H_adp2 = h_maxima(dist_img, h=h_adp2)
   H_adp2 = H_adp2*255


   eli1 = eliminate_small(H_adp1, 2)
   eli2 = eliminate_small(H_adp2, 2)

   intersec_img = remove_intersec(eli1, eli2)

   nb_components, output = cv2.connectedComponents(intersec_img)
   
   intersec_img = cv2.bitwise_or(eli1, intersec_img)

   h = 3
   while nb_components > 1: # only background
      eli1         = intersec_img.copy()

      H_adp        = h_maxima(dist_img, h=h)
      H_adp        = H_adp*255
      eli2         = eliminate(H_adp, 2)

      intersec_img = remove_intersec(eli1, eli2)
      nb_components, output = cv2.connectedComponents(intersec_img)
      
      intersec_img = cv2.bitwise_or(eli1, intersec_img)

      h = h + 1

   markers = intersec_img

   return markers