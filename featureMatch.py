import cv2
import numpy as np
MIN_MATCH_COUNT=10

detector=cv2.xfeatures2d.SURF_create(4000)

FLANN_INDEX_KDITREE=0
flannParam=dict(algorithm=FLANN_INDEX_KDITREE,tree=5)
flann=cv2.FlannBasedMatcher(flannParam,{})

imgList = []
descList = []
kpList = []
trainImg=cv2.imread("granolabar.png",0)
trainKP,trainDesc=detector.detectAndCompute(trainImg,None)
imgList.append(trainImg)
descList.append(trainDesc)
kpList.append(trainKP)
trainImg2=cv2.imread("cracker.png",0)
trainKP2,trainDesc2=detector.detectAndCompute(trainImg2,None)
imgList.append(trainImg2)
descList.append(trainDesc2)
kpList.append(trainKP2)

isOne = False
#print(len(trainKP))
#print(len(trainKP2))

cam=cv2.VideoCapture(0)
while True:
    ret, QueryImgBGR=cam.read()
    QueryImg=cv2.cvtColor(QueryImgBGR,cv2.COLOR_BGR2GRAY)
    #QueryImg = QueryImg.astype('uint8')
    queryKP,queryDesc=detector.detectAndCompute(QueryImg,None)
    if (isOne):
        trainImg = imgList[0]
        trainDesc = descList[0]
        trainKP = kpList[0]
    else:
        trainImg = imgList[1]
        trainDesc = descList[1]
        trainKP = kpList[1]
    matches=flann.knnMatch(queryDesc,trainDesc,k=2)

    goodMatch=[]
    for m,n in matches:
        if(m.distance<0.75*n.distance):
            goodMatch.append(m)
    if(len(goodMatch)>MIN_MATCH_COUNT):
        tp=[]
        qp=[]
        for m in goodMatch:
            tp.append(trainKP[m.trainIdx].pt)
            qp.append(queryKP[m.queryIdx].pt)
        tp,qp=np.float32((tp,qp))
        H,status=cv2.findHomography(tp,qp,cv2.RANSAC,3.0)
        h,w=trainImg.shape
        trainBorder=np.float32([[[0,0],[0,h-1],[w-1,h-1],[w-1,0]]])
        queryBorder=cv2.perspectiveTransform(trainBorder,H)
        cv2.polylines(QueryImgBGR,[np.int32(queryBorder)],True,(0,255,0),5)
        '''
        if (isOne):
            isOne = False
        else:
            isOne = True
        '''
        
    else:
        print ("Not Enough match found- %d/%d" ,len(goodMatch),MIN_MATCH_COUNT)
    cv2.imshow('result',QueryImgBGR)
    if cv2.waitKey(10)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
