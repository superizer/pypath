import cv2
from pypath.transform import convert_RGB_to_OD, convert_OD_to_RGB
from pypath.stain_extractor import HE_color_decon
from pypath.texture import cal_lbp

I_BGR    = cv2.imread('images/he.png')
I_RGB    = cv2.cvtColor(I_BGR, cv2.COLOR_BGR2RGB)
I_OD     = convert_RGB_to_OD(I_RGB)

I_H, I_E = HE_color_decon(I_RGB)

# convert to show true color in monitor
I_H = cv2.cvtColor(I_H, cv2.COLOR_RGB2BGR)
I_E = cv2.cvtColor(I_E, cv2.COLOR_RGB2BGR)

I_LBP    = cal_lbp(I_BGR)

cv2.imshow('I_BGR', I_BGR)
cv2.imshow('I_OD', I_OD)
cv2.imshow('I_H', I_H)
cv2.imshow('I_E', I_E)
cv2.imshow('I_LBP', I_LBP)
cv2.waitKey(0)
cv2.destroyAllWindows()