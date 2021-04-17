import cv2
import pypath as pp

I_BGR = cv2.imread('images/he.png')
I_RGB = cv2.cvtColor(I_BGR, cv2.COLOR_BGR2RGB)
I_OD  = pp.convert_RGB_to_OD(I_RGB)


cv2.imshow('I_RGB', I_RGB)
cv2.imshow('I_OD', I_OD)
cv2.waitKey(0)
cv2.destroyAllWindows()