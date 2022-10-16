import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import psutil
import os
import utils

pic_counter=0
file_counter1=2
screen_counter1=0


current_pos_of_pic=[140,140]
current_size_of_pic=[140,120]

current_filter=None

current_pos=current_pos_of_pic


def distance(x1,y1,x2,y2):
  dx=(x2-x1)**2
  dy=(y2-y1)**2

  dist=(dx+dy)**(0.5)
  return dist

def reset(cap):
  # img1=original
  _,img=cap.read()
  img=cv2.flip(img,2)
  img=cv2.resize(img,[1280,720])
  global file_counter1
  file_counter1=2

  global current_pos_of_pic,current_size_of_pic,current_filter
  current_pos_of_pic=[140,140]
  current_size_of_pic=[140,120]
  current_filter=None

  return img

def screen1(img,button):
  cancel=cv2.imread("buttons/close.png")
  back=cv2.imread("buttons/back.png")
  zoom=cv2.imread("buttons/resize.png")
  cancel=cv2.resize(cancel,(16,16))
  back=cv2.resize(back,(16,16))
  zoom=cv2.resize(zoom,(16,16))

  if button==0:
    img[20-16//2:20+16//2,img.shape[0]-16//2:img.shape[0]+16//2]=cancel
    # cv2.circle(img,[img.shape[0],20],15,[0,0,256],-1)
    cv2.circle(img,[img.shape[0]+140,20],15,[0,256,0],-1)
  elif button==1:
    img[20-16//2:20+16//2,img.shape[0]-16//2:img.shape[0]+16//2]=cancel
    # cv2.circle(img,[img.shape[0],20],15,[0,0,256],-1) 
    cv2.circle(img,[img.shape[0]+440,20+300],15,[0,200,80],-1) #zoom
    img[20+300-16//2:20+300+16//2,img.shape[0]+440-16//2:img.shape[0]+440+16//2]=zoom
    cv2.circle(img,[img.shape[0]+440,100+300],15,[200,56,0],-1) #pick
    cv2.circle(img,[img.shape[0]+440,180+300],15,[140,6,140],-1) #filters
    cv2.rectangle(img,[0,0],[img.shape[1],img.shape[0]],[0,256,0],3)
    
  elif button==2:
    img[20-16//2:20+16//2,img.shape[0]-16//2:img.shape[0]+16//2]=cancel
    # cv2.circle(img,[img.shape[0],20],15,[0,0,256],-1)
    # cv2.circle(img,[img.shape[0]+440,100+300],15,[0,256,256],-1)
    cv2.circle(img,[img.shape[0]+440,220],15,[0,256,256],-1)
    img[220-16//2:220+16//2,img.shape[0]+440-16//2:img.shape[0]+440+16//2]=back

  elif button==3:
    img[20-16//2:20+16//2,img.shape[0]-16//2:img.shape[0]+16//2]=cancel
    # cv2.circle(img,[img.shape[0],20],15,[0,0,256],-1)
    cv2.circle(img,[img.shape[0]+440,100+120],15,[0,256,256],-1)
    img[220-16//2:220+16//2,img.shape[0]+440-16//2:img.shape[0]+440+16//2]=back

  elif button==4:
    img[20-16//2:20+16//2,img.shape[0]-16//2:img.shape[0]+16//2]=cancel
    # cv2.circle(img,[img.shape[0],20],15,[0,0,256],-1)
    cv2.circle(img,[img.shape[0]+400,20],15,[256,0,256],-1) #back
    cv2.circle(img,[img.shape[0]+480,20+250],15,[0,0,0],-1) #reset
    cv2.circle(img,[img.shape[0]+480,100+250],15,[5,0,160],-1) #filter1
    cv2.circle(img,[img.shape[0]+480,180+250],15,[20,201,150],-1) #filter2
    cv2.circle(img,[img.shape[0]+480,260+250],15,[50,216,20],-1) #filter3

    # img[220-16//2:220+16//2,img.shape[0]+400-16//2:img.shape[0]+400+16//2]=back

  elif button==5:
    img[20-16//2:20+16//2,img.shape[0]-16//2:img.shape[0]+16//2]=cancel
    # cv2.circle(img,[img.shape[0],20],15,[0,0,256],-1)
    cv2.circle(img,[img.shape[0]+440,100+120],15,[0,256,256],-1)
    img[220-16//2:220+16//2,img.shape[0]+440-16//2:img.shape[0]+440+16//2]=back

  return img

def filters(img,filter_no):
  if filter_no==0:
    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  elif filter_no==1:
    img=cv2.convertScaleAbs(img, beta=60)
  elif filter_no==2:
    img = np.array(img, dtype=np.float64)
    img = cv2.transform(img, np.matrix([[0.272, 0.534, 0.131],[0.349, 0.686, 0.168],[0.393, 0.769, 0.189]]))
    img[np.where(img > 255)] = 255
    img = np.array(img, dtype=np.uint8)
  elif filter_no==3:
    img = cv2.detailEnhance(img, sigma_s=12, sigma_r=0.15)
  elif filter_no==None:
    pass

  return img
