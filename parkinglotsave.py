import cv2
import pickle
import cvzone
import numpy as np
width,height=95,205
#this is for saving the parking lot that is craeted by us
#Video feed
capture=cv2.VideoCapture('parkinglotVideo2.mov')
with open('lots','rb') as f:
    position=pickle.load(f)
#this is for checking the parking lot in parking area
def checkParkingLot(Imagepro):
    spacecnt=0
    for pos in position:
        x,y=pos
        imageCrop=Imagepro[y:y+height,x:x+width]
       # cv2.imshow(str(x*y),imageCrop)
        cnt=cv2.countNonZero(imageCrop)
        cvzone.putTextRect(image,str(cnt),(x,y+height-10), scale=1,thickness=2, offset=0)
        if cnt<900:
            color=(0,255,0)
            thickness=5
            spacecnt+=1
        else:
            color=(0,0,255)
            thickness=2

        cv2.rectangle(image, pos, (pos[0] + width, pos[1] + height), color, thickness)

    cvzone.putTextRect(image,f'Free:{spacecnt}/{len(position)}',(100,50), scale=3,thickness=5, offset=20,colorR=(0,200,0))


while True:
    if capture.get(cv2.CAP_PROP_POS_FRAMES)==capture.get(cv2.CAP_PROP_FRAME_COUNT):
        capture.set(cv2.CAP_PROP_POS_FRAMES,0)

    success, image=capture.read()
    imageGray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    imageBlur=cv2.GaussianBlur(imageGray,(3,3),1)
    imagThreshold=cv2.adaptiveThreshold(imageBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
    imgMedian=cv2.medianBlur(imagThreshold,5)
    kernal=np.ones((3,3),np.uint8)
    imgdialate=cv2.dilate(imgMedian,kernal,iterations=1)

    checkParkingLot(imgdialate)
    cv2.imshow("image",image)
    cv2.waitKey(10)

