import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import psutil
import os
import screens

def distance(x1,y1,x2,y2):
  dx=(x2-x1)**2
  dy=(y2-y1)**2

  dist=(dx+dy)**(0.5)
  return dist

def create_interface(img1,img2,pt1): 
  img2=cv2.resize(img2,(120,130))
  img1[pt1[0]:pt1[0]+130,pt1[1]:pt1[1]+120]=img2
  
  return img1
  
def put_files(img,dir_list):
  pt1=[70,70]
  for i in range(len(dir_list)):
      # print(i,pt1)
      img2=cv2.imread("imgs/"+dir_list[i])
      img=create_interface(img,img2,pt1)
      img_shape=img.shape

      if pt1[0]+140<img_shape[0]:
        pt1[0]+=140
        pt1[1]=70
      if pt1[0]+140>img_shape[0]:
        temp=pt1[1]
        pt1[0]=70
        pt1[1]=temp+150
      # elif pt1[0]+140>img_shape[0] and pt1[1]+150>img_shape[0]:
        # print("overload")


def power_status():
    battery=psutil.sensors_battery()
    plugged_in=psutil.sensors_battery()
    percent=str(battery.percent)
    # print(battery,plugged_in,percent)
    if not plugged_in.power_plugged:
        plugged_in=False
        return plugged_in, percent

    else:
        plugged_in=True 
        return plugged_in, percent

