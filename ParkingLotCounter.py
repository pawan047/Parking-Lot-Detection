import cv2
import pickle

#image=cv2.imread('back-parking.jpg')
width,height=95,205
try:
    with open('lots','rb') as f:
        position=pickle.load(f)
except:
    position=[]

#this is for selecting parking lot in parking area
def mouseClick(events,x,y,flags,params):
    if events==cv2.EVENT_LBUTTONDOWN:
        position.append((x,y))
    if events==cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(position):
            x1,y1=pos
            if x1<x<x1+width and y1<y<y1+height:
                position.pop(i)
    with open('lots','wb') as f:
        pickle.dump(position,f)


while True:
   image=cv2.imread('parkingLotImage.jpg')
   #cv2.rectangle(image,(175,120),(290,330),(255,0,255),4)
   for pos in position:
       cv2.rectangle(image,pos,(pos[0]+width,pos[1]+height),(255,0,255),2)
   cv2.imshow("Image",image)
   cv2.setMouseCallback("Image",mouseClick)
   cv2.waitKey(1)


