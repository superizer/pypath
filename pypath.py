import numpy as np


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