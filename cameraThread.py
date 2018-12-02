import threading
import cv2
import numpy as np
import urllib
import requests

MIN_MATCH_COUNT=10
CUSHION = 8
NEGCUSHION = -8

def setTarget(targetName, dirBool):
    requests.post('https://wuwicajon.wixsite.com/test/_functions-dev/setTarget',
    params=urllib.parse.urlencode({
    'target': targetName, 'add': dirBool}))

class CameraThread(threading.Thread):

    MIN_MATCH_COUNT=10
    imgList = []
    kpList = []
    descList = []

    detector=cv2.xfeatures2d.SURF_create(4000)

    FLANN_INDEX_KDITREE=0
    flannParam=dict(algorithm=FLANN_INDEX_KDITREE,tree=5)
    flann=cv2.FlannBasedMatcher(flannParam,{})

    
    def __init__(self):
        self.foundList = []
        self.imgList = []
        self.kpList = []
        self.descList = []
        self.labelList = []
        self.sentFlag = []
        img1 = cv2.imread("cracker.png",0)
        self.labelList.append('cracker')
        self.foundList.append(NEGCUSHION)
        self.sentFlag.append(True)
        self.imgList.append(img1)
        trainKP,trainDesc=CameraThread.detector.detectAndCompute(img1,None)
        self.kpList.append(trainKP)
        self.descList.append(trainDesc)
        img2 = cv2.imread("creamcheese.png",0)
        self.labelList.append('creamcheese')
        self.foundList.append(NEGCUSHION)
        self.sentFlag.append(True)
        self.imgList.append(img2)
        trainKP2,trainDesc2=CameraThread.detector.detectAndCompute(img2,None)
        self.kpList.append(trainKP2)
        self.descList.append(trainDesc2)
    
    def run(self):
        print ("Starting camThread")
        cam=cv2.VideoCapture(0)
        print ('Got cam')
        i = 0
        while True:
            '''
            self.imgList = CameraThread.imgList
            self.kpList = CameraThread.kpList
            self.descList = CameraThread.descList
            '''
            ret, QueryImgBGR=cam.read()
            QueryImg=cv2.cvtColor(QueryImgBGR,cv2.COLOR_BGR2GRAY)
            queryKP,queryDesc=CameraThread.detector.detectAndCompute(QueryImg,None)
            if (i):
                i = 0
            else:
                i = 1
            matches=CameraThread.flann.knnMatch(queryDesc,self.descList[i],k=2)
            goodMatch=[]
            for m,n in matches:
                if(m.distance<0.75*n.distance):
                    goodMatch.append(m)
            if(len(goodMatch)>MIN_MATCH_COUNT):
                tp=[]
                qp=[]
                for m in goodMatch:
                    tp.append(self.kpList[i][m.trainIdx].pt)
                    qp.append(queryKP[m.queryIdx].pt)
                tp,qp=np.float32((tp,qp))
                Hret,status=cv2.findHomography(tp,qp,cv2.RANSAC,3.0)
                h,w=self.imgList[i].shape
                trainBorder=np.float32([[[0,0],[0,h-1],[w-1,h-1],[w-1,0]]])
                if Hret is not None:
                    queryBorder=cv2.perspectiveTransform(trainBorder,Hret)
                    #print(queryBorder)
                    cv2.putText(QueryImgBGR,self.labelList[i],(queryBorder[0][0][0],queryBorder[0][0][1]),cv2.FONT_HERSHEY_SIMPLEX,2,[255,255,255],lineType=cv2.LINE_AA)
                    cv2.polylines(QueryImgBGR,[np.int32(queryBorder)],True,(255,255,0),5) 
                    
                    if (self.foundList[i] == 0):
                        self.sentFlag[i] = False
                        self.foundList[i] += 1
                    elif (self.foundList[i] < CUSHION):
                        self.foundList[i] += 1
                    elif (self.foundList[i] == CUSHION and self.sentFlag[i] == False):
                        targetName = self.labelList[i]
                        setTarget(targetName,True)
                        print("send found %s", targetName)
                        self.sentFlag[i] = True         
            else:
                #print ("Not Enough match found- %d/%d img %d" ,len(goodMatch),MIN_MATCH_COUNT,i)
                if (self.foundList[i] == 0):
                    self.sentFlag[i] = False
                    self.foundList[i] -= 1
                elif (self.foundList[i] > NEGCUSHION):
                    self.foundList[i] -= 1
                elif (self.foundList[i] == NEGCUSHION and self.sentFlag[i] == False):
                    targetName = self.labelList[i]
                    setTarget(targetName,False)
                    print("send remove %s", targetName)
                    self.sentFlag[i] = True    
            #print("i %d foundList count %d", i, self.foundList[i] )
            cv2.imshow('camera',QueryImgBGR)
            if cv2.waitKey(10)==ord('q'):
                break
        cam.release()
        cv2.destroyAllWindows()
