import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import psutil
import os
import utils, screens


startDist=None

cap=cv2.VideoCapture(0)

detector=HandDetector(detectionCon=0.8)

def reset(cap):

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


def pick_image(img,img1,handloc,detector,hands):
  y_main,x_main=img.shape[0:2]
  # print(x_main,y_main)
  y2,x2=img1.shape[0:2]
  x1,y1=handloc[8][0:2]

  new_x1=x1-x2//2
  new_x2=x1+x2//2

  new_y1=y1-y2//2
  new_y2=y1+y2//2


  if (new_y2<y_main and new_x2<x_main and new_y1>0 and new_x1>0):

    if detector.fingersUp(hands[0])==[1,1,0,0,0] or detector.fingersUp(hands[0])==[0,1,0,0,0] :

      img[new_y1:new_y2,new_x1:new_x2]=img1

      global current_pos_of_pic
      current_pos_of_pic=[new_x1,new_y1]
  return img,y1-y2//2,x1-x2//2


def zoom(img,img1,hands,detector,current_pos):
  if len(hands)==2:
    if detector.fingersUp(hands[0])==[0,1,0,0,0] and detector.fingersUp(hands[1])==[0,1,0,0,0]:
  
        lmList1=hands[0]["lmList"]
        lmList2=hands[1]["lmList"]
        global startDist
        if startDist==None:
          length,info,img=detector.findDistance(lmList1[8][0:2],lmList2[8][0:2],img)
          startDist=length
        length,info,img=detector.findDistance(lmList1[8][0:2],lmList2[8][0:2],img)
        scale=int((length-startDist)//2)
    
        cx,cy=info[4],info[5]

        w1,h1=current_pos[0:2]
        new_h,new_w=((h1+scale)//2)*2,((w1+scale)//2)*2
        img1=cv2.resize(img1,[new_h,new_w])

        global current_size_of_pic
        current_size_of_pic=[new_w,new_h]
        global current_pos_of_pic

        current_pos_of_pic=[cx-new_w//2,cy-new_h//2]

        
  else:
    startDist=None


  return img

pic_counter=0
file_counter1=2
screen_counter1=0


current_pos_of_pic=[140,140]
current_size_of_pic=[140,120]

current_filter=None

current_pos=current_pos_of_pic

while True:
    __,img=cap.read()


    img=cv2.flip(img,2)
    img=cv2.resize(img,[1280,720])


    hands, img=detector.findHands(img,flipType=False)

    plugged,percent=utils.power_status()
    
    # battery
    cv2.rectangle(img,[5,16],[15,30],[0,0,0],1)
    cv2.rectangle(img,[7,12],[13,16],[0,0,0],1)

    cv2.circle(img,[img.shape[0],20],15,[0,0,256],-1)
    # cv2.circle(img,[img.shape[0]+140,20],15,[0,256,0],-1)
    img=screens.screen1(img,screen_counter1)

    cv2.putText(img,percent,[40,22],cv2.FONT_HERSHEY_COMPLEX,0.5,[0,0,0])
    if plugged==True:

      # baseline
      cv2.line(img,[25,30],[27,30],[0,0,0],1)

      # small curved lines
      cv2.line(img,[25,30],[20,25],[0,0,0],1)
      cv2.line(img,[27,30],[32,25],[0,0,0],1)

      # lines from baseline
      cv2.line(img,[32,25],[32,20],[0,0,0],1)
      cv2.line(img,[20,25],[20,20],[0,0,0],1)

      # common line
      cv2.line(img,[18,20],[34,20],[0,0,0],1)

      # pins
      cv2.line(img,[22,20],[22,15],[0,0,0],1)
      cv2.line(img,[30,20],[30,15],[0,0,0],1)


  
    dir_list = os.listdir("imgs")
  
    pt1=[70,70]

    images_rest=img
    
    length_final_reset=35
    length_final_img=35
    if len(hands)>=1:

      lmList1=hands[0]["lmList"]
      # cancel
      length_final_reset=utils.distance(lmList1[8][0],lmList1[8][1],img.shape[0],20)
      if screen_counter1==0:
        length_final_img=utils.distance(lmList1[8][0],lmList1[8][1],img.shape[0]+140,20)


      if len(hands)==2:
        lmList2=hands[1]["lmList"]
        # green
        length_final_reset=utils.distance(lmList2[8][0],lmList2[8][1],img.shape[0],20)
        if screen_counter1==0:
          length_final_img=utils.distance(lmList2[8][0],lmList2[8][1],img.shape[0]+140,20)

      if screen_counter1==1:
        # enter image menu
        length_btn1=utils.distance(lmList1[8][0],lmList1[8][1],img.shape[0]+440,320)
        if length_btn1<25:
          screen_counter1=2
          screens.screen1(img,screen_counter1)

      if screen_counter1==1:
        # filters
        length_btn1=utils.distance(lmList1[8][0],lmList1[8][1],img.shape[0]+440,180+300)
        
        if length_btn1<25:
          screen_counter1=4
          screens.screen1(img,screen_counter1)

      # filters
      if screen_counter1==4:
        length_btn41=utils.distance(lmList1[8][0],lmList1[8][1],img.shape[0]+480,20+250)
        

        if length_btn41<25:
          # print("b&w")
          current_filter=None
          screen_counter1=5
          screens.screen1(img,screen_counter1)

      ###############
      if screen_counter1==4:
        length_btn42=utils.distance(lmList1[8][0],lmList1[8][1],img.shape[0]+480,100+250)
        # img1=filters(img1,1)
        if length_btn42<25:
          current_filter=1
          screen_counter1=5
          # print(screen_counter1,"red")
          screens.screen1(img,screen_counter1)

      # img.shape[0]+400,20
      if screen_counter1==4:
        length_btnbck=utils.distance(lmList1[8][0],lmList1[8][1],img.shape[0]+400,20)
        if length_btnbck<25:
          screen_counter1=1
          screens.screen1(img,screen_counter1)

      if screen_counter1==4:
        length_btn43=utils.distance(lmList1[8][0],lmList1[8][1],img.shape[0]+480,180+250)
        # img1=filters(img1,2)
        if length_btn43<25:
          current_filter=2
          screen_counter1=5
        
          screens.screen1(img,screen_counter1)

      if screen_counter1==4:
        length_btn44=utils.distance(lmList1[8][0],lmList1[8][1],img.shape[0]+480,260+250)
        # img1=filters(img1,3)
        if length_btn44<25:
          current_filter=3
          screen_counter1=5
    
          screens.screen1(img,screen_counter1)

      if screen_counter1==2:
        length_btn12=utils.distance(lmList1[8][0],lmList1[8][1],img.shape[0]+440,220)
        if length_btn12<25:
          screen_counter1=1
          screens.screen1(img,screen_counter1)

      if screen_counter1==1:
        length_btn2=utils.distance(lmList1[8][0],lmList1[8][1],img.shape[0]+440,400)
        if length_btn2<25:
          screen_counter1=3
          screens.screen1(img,screen_counter1)
      

      if screen_counter1==3:
        length_btn21=utils.distance(lmList1[8][0],lmList1[8][1],img.shape[0]+440,220)
        if length_btn21<25:
          screen_counter1=1
          screens.screen1(img,screen_counter1)

      if screen_counter1 == 1:
        lmList1=hands[0]["lmList"]
        
        if len(lmList1) != 0:

          distIM=utils.distance(lmList1[8][0],lmList1[8][1],lmList1[12][0],lmList1[12][1])

          if distIM < 20:
            # print("YES")
            pic_counter+=1




    if length_final_reset<25:
      screen_counter1=0
      reset(cap)

    if length_final_img<25:
      file_counter1+=1
      screen_counter1=1
    if length_final_img<25 or screen_counter1>=1:
      img=screens.screen1(img,screen_counter1)
      if pic_counter==len(dir_list):
        pic_counter=0
        
      img1=cv2.imread("imgs/"+dir_list[pic_counter])
      
      img1=cv2.resize(img1,current_size_of_pic)
      img1=screens.filters(img1,current_filter)
      
      img[current_pos_of_pic[1]:current_pos_of_pic[1]+current_size_of_pic[1],current_pos_of_pic[0]:current_pos_of_pic[0]+current_size_of_pic[0]]=img1

      
      if screen_counter1==3:

        if (len(hands)==1) and (detector.fingersUp(hands[0])==[1,1,0,0,0]):
          
          img,cur_x,cur_y=pick_image(img,img1,lmList1,detector,hands)

      if screen_counter1==2:
        img=zoom(img,img1,hands,detector,current_pos_of_pic)
        
      if screen_counter1==5:
        length_btn41=screens.distance(lmList1[8][0],lmList1[8][1],img.shape[0]+440,220)
        
        if length_btn41<25:
          screen_counter1=4
          screens.screen1(img,screen_counter1)

    cv2.imshow("image",img)
    if cv2.waitKey(5) & 0xFF == 27:
      break

cap.release()