import pyautogui
import cv2
import numpy as np
import time
import pyautogui as pg
import matplotlib.pyplot as plt

dummy = input()
roi = [0,0,0,0]
base = [0,0,0,0]

def onMouse(event, x, y, flags, param):
    # print(img[x,y])
    global roi
    if event == cv2.EVENT_LBUTTONDOWN:
        print('l dwn')
        print(x,y)
        roi[0:2] = [x,y]
    if event ==cv2.EVENT_LBUTTONUP:
        print('l up')
        print(x,y)
        roi[2:4]=[x,y]
        print(roi)


def onMouse1(event, x, y, flags, param):
    # print(img[x,y])
    global base
    if event == cv2.EVENT_LBUTTONDOWN:
        print('l dwn')
        print(x,y)
        base[0:2] = [x,y]

scrn = pyautogui.screenshot()
img = np.array(scrn)


while 1:
    cv2.imshow('iwin',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.setMouseCallback('iwin', onMouse)
    if((roi[0]> 0) and (roi[2]>0)):
        print(roi)
        #roi[3] = roi[3]-roi[1]
        # roi = [0,0,0,0]
        break;

cv2.destroyWindow('iwin')
image_ref = img[roi[1]:roi[3],roi[0]:roi[2]]
dummy = input()

scrn = pyautogui.screenshot()
img = np.array(scrn)
while 1:
    cv2.imshow('base',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.setMouseCallback('base',onMouse1)
    if(base[0]>0):
        break;

cv2.destroyWindow('base')
print("Base value ", base)



cv2.imshow('cropped',image_ref)
cv2.waitKey(0)

base[2] =30
base[3] =30
count = 50
for a in range(count):
    scrn = pyautogui.screenshot(region=base)
    template = np.array(scrn)
    method = eval('cv2.TM_SQDIFF_NORMED')
    # Apply template Matching
    res = cv2.matchTemplate(image_ref, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    #if(min_val <= 0.1):
    top_left = min_loc
    print(min_val)
    bottom_right = (top_left[0] + 30, top_left[1] + 30)
    image_ref1 = image_ref.copy()
    cv2.rectangle(image_ref1,top_left,bottom_right,(0,0,255),2)
    cv2.imshow('detection',image_ref1)
    stemp = cv2.resize(template, (300, 300))
    cv2.imshow('template',stemp)
    cv2.waitKey(33)
    pg.moveTo(base[0],base[1])
    pg.dragTo(top_left[0]+roi[0],top_left[1]+roi[1],0.4)
