import numpy as np
import cv2 as cv
import matplotlib
matplotlib.use("MacOSX")
import matplotlib.pyplot as plt

def gbcutImg(picname):
    #inputname = "banana.jpg" example
    #outputname = "banana.png" example
    inputname = picname + 'jpg'
    outputname = picname + 'png'
    #rescale img
    oriimg = cv.imread(inputname)
    height, width, channels = oriimg.shape
    W = 480
    imgScale = W/width
    newX,newY = oriimg.shape[1]*imgScale, oriimg.shape[0]*imgScale
    newimg = cv.resize(oriimg,(int(newX),int(newY)))

    #create mask for newimg
    mask = np.zeros(newimg.shape[:2],np.uint8)
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    heightnew, widthnew, channelsnew = newimg.shape
    
    print(heightnew) #debug
    print(widthnew)

    #rect assuming the user has already pre cropped the image
    rect = (1,1,widthnew-1,heightnew-1)

    #running grabCut 15 times for good luck :)
    cv.grabCut(newimg,mask,rect,bgdModel,fgdModel,15,cv.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==1) + (mask==3),255,0).astype('uint8')
    #newimg = newimg*mask2[:,:,np.newaxis]
    newimg = cv.bitwise_and(newimg,newimg,mask=mask2)

    #save the segmented image to local
    cv.imwrite(outputname,newimg)
    print('finish segment')
    #plt.imshow(newimg),plt.colorbar(),plt.show()
