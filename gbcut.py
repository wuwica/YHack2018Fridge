import numpy as np
import cv2 as cv
import matplotlib
matplotlib.use("MacOSX")
import matplotlib.pyplot as plt
oriimg = cv.imread('cracker.jpg')
height, width, channels = oriimg.shape
W = 1000
imgScale = W/width
newX,newY = oriimg.shape[1]*imgScale, oriimg.shape[0]*imgScale
newimg = cv.resize(oriimg,(int(newX),int(newY)))

mask = np.zeros(newimg.shape[:2],np.uint8)
bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)

heightnew, widthnew, channelsnew = newimg.shape
print(heightnew)
print(widthnew)

rect = (1,1,widthnew-1,heightnew-1)
cv.grabCut(newimg,mask,rect,bgdModel,fgdModel,15,cv.GC_INIT_WITH_RECT)
mask2 = np.where((mask==1) + (mask==3),255,0).astype('uint8')
#newimg = newimg*mask2[:,:,np.newaxis]
newimg = cv.bitwise_and(newimg,newimg,mask=mask2)
'''
bar = np.zeros((newimg.shape[0],5,3),np.uint8)
res = np.hstack((new,bar,img,bar,output))
'''
cv.imwrite('cracker.png',newimg)
plt.imshow(newimg),plt.colorbar(),plt.show()
