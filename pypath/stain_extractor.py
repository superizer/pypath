import spams
import numpy as np
import staintools
from pypath.transform import convert_RGB_to_OD, convert_OD_to_RGB


def HE_color_decon_Vahadane(I_RGB):
   ''' 
   matrix Factorization using spams library
   from A. Vahadane et al. 'Structure-Preserving Color Normalization and Sparse Stain Separation for Histological Images'
   input: I_RGB
   output: I_H, I_E
   '''

   OD    = convert_RGB_to_OD(I_RGB).reshape((-1, 3))


   param = { 'K' : 2, 'lambda1' : 0.1 }
   D     = spams.trainDL(X=OD.T, **param)

   # Sort I_H before I_E by pink color checking
   if np.abs(D[0, 0] - D[2, 0]) < np.abs(D[0, 1] - D[2, 1]): 
      D = D[:,[1,0]]

   param  = { 'pos' : True, 'lambda1' : 0.1 }
   Hs_vec = spams.lasso(X=OD.T, D=D, **param).T

   vdAs  = Hs_vec[:,0]*D[:,0].reshape((1,3))
   I_H  = convert_OD_to_RGB(vdAs).reshape(I_RGB.shape)

   vdAs  = Hs_vec[:,1]*D[:,1].reshape((1,3))
   I_E   = convert_OD_to_RGB(vdAs).reshape(I_RGB.shape)

   return I_H, I_E

def IHC_color_decon_Vahadane(I_RGB):
   '''
   Immunohistrochemistry color deconvolution
   Using same technique as H&E image
   input: I_RGB
   output: I_DAB, I_H
   '''
   color_img = staintools.LuminosityStandardizer.standardize(I_RGB)
   OD        = convert_RGB_to_OD(color_img).reshape((-1, 3))


   param = { 'K' : 2, 'lambda1' : 0.1 }
   D     = spams.trainDL(X=OD.T, **param)

   # Sort h before dab by blue color checking
   if D[2, 1] < D[2, 0]:
      D = D[:,[1,0]]

   param  = { 'pos' : True, 'lambda1' : 0.1 }
   Hs_vec = spams.lasso(X=OD.T, D=D, **param).T

   vdAs  = Hs_vec[:,0]*D[:,0].reshape((1,3))
   h     = convert_OD_to_RGB(vdAs).reshape(I_RGB.shape)

   vdAs  = Hs_vec[:,1]*D[:,1].reshape((1,3))
   dab   = convert_OD_to_RGB(vdAs).reshape(I_RGB.shape)
   return h, dab

def IHC_color_decon_Mouelhi(I_RGB):
   '''
   Immunohistrochemistry color deconvolution
   Using parameters from A. Mouelhia et al. 'A Novel Morphological Segmentation Method for Evaluating Estrogen Receptors' Status in Breast Tissue Images'
   input: I_RGB
   output: I_DAB, I_H
   '''
   I_RGB = staintools.LuminosityStandardizer.standardize(I_RGB)
   OD    = convert_RGB_to_OD(I_RGB).reshape((-1, 3))

   D = np.zeros((3, 2))
   D[0,0] = 0.3767
   D[0,1] = 0.9837
   D[1,0] = 0.8124
   D[1,1] = 0.5124
   D[2,0] = 0.9408
   D[2,1] = 0.4475
   D = np.asfortranarray(D, dtype=np.float64)

   # Sort h before dab by blue color checking
   if D[2, 1] < D[2, 0]:
      D = D[:,[1,0]]


   param  = { 'pos' : True, 'lambda1' : 0.1 }
   Hs_vec = spams.lasso(X=OD.T, D=D, **param).T

   vdAs  = Hs_vec[:,0]*D[:,0].reshape((1,3))
   h     = convert_OD_to_RGB(vdAs).reshape(I_RGB.shape)

   vdAs  = Hs_vec[:,1]*D[:,1].reshape((1,3))
   dab   = convert_OD_to_RGB(vdAs).reshape(I_RGB.shape)

   return h, dab