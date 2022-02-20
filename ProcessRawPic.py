import numpy as np
import os
from PIL import Image

os.chdir(os.path.join(__file__,os.path.pardir))

LETTERNUM=5 # the number of different letters
PICNUM=5 # the number of different images of each letters

OPERATORLIST=['p','m'] # operator list, p:plus m:multiply
NUMBERLIST=['2','3'] # number list

NUMBERNUM=len(NUMBERLIST)

NUMBERSHAPE=15 # size of numbers
SHAPE=40 # size of letters
BACKGROUNDSHAPE=550 # size of background image
BACKGROUNDPICNUM=5 # number of background image

PATH1="source/letterpicsn/"

def get_letter_pics():
    allletter_list=[]
    for i in range(LETTERNUM):
        allletter_list.append(list())

    for i in range(LETTERNUM):
        letter=chr(ord('a')+i)
        for j in range(1,PICNUM+1):
            num=str(j)
            path=PATH1+letter+num+".jpg"
            a=Image.open(path)
            picarray=np.array(Image.fromarray(cutpics(a)).resize((SHAPE, SHAPE),Image.ANTIALIAS))
            picarray[picarray<240]=0
            allletter_list[i].append(picarray)
    return allletter_list

def get_operation_pics():
    alloperator_list=[]
    for i in range(len(OPERATORLIST)):
        alloperator_list.append(list())

    for i in range(len(OPERATORLIST)):
        opi=OPERATORLIST[i]
        for j in range(1,PICNUM+1):
            num=str(j)
            path=PATH1+"_"+opi+num+".jpg"
            a=Image.open(path)
            picarray=np.array(Image.fromarray(cutpics_withoutrow(a)).resize((SHAPE, SHAPE),Image.ANTIALIAS)) # for minus images
            picarray[picarray<240]=0
            alloperator_list[i].append(picarray)
    return alloperator_list

def get_number_pics():
    allnumber_list=[]
    for i in range(len(NUMBERLIST)):
        allnumber_list.append(list())
    
    for i in range(len(NUMBERLIST)):
        ni=NUMBERLIST[i]
        for j in range(1,PICNUM+1):
            num=str(j)
            path=PATH1+ni+num+".jpg"
            a=Image.open(path)
            picarray=np.array(Image.fromarray(cutpics(a)).resize((NUMBERSHAPE, NUMBERSHAPE),Image.ANTIALIAS))
            picarray[picarray<240]=0
            allnumber_list[i].append(picarray)
    return allnumber_list

def cutpics(a):#裁剪，最小外接框
    a=255-np.array(a.convert('L'))
    VB1,VB2=0,1
    HB1,HB2=0,1
    aa=(a>50)
    vbool=aa.any(axis=0)
    hbool=aa.any(axis=1)
    for i in range(len(hbool)):
        if hbool[i]:
            VB1=i
            break
    for i in range(len(hbool)-1,-1,-1):
        if hbool[i]:
            VB2=i
            break
    for i in range(len(vbool)):
        if vbool[i]:
            HB1=i
            break
    for i in range(len(vbool)-1,-1,-1):
        if vbool[i]:
            HB2=i
            break
    return 255-a[VB1:VB2+1][:,HB1:HB2+1]

def cutpics_withoutrow(a):#裁剪，纵向最小外接框
    a=255-np.array(a.convert('L'))
    #VB1,VB2=0,1
    HB1,HB2=0,1
    aa=(a>50)
    vbool=aa.any(axis=0)
    for i in range(len(vbool)):
        if vbool[i]:
            HB1=i
            break
    for i in range(len(vbool)-1,-1,-1):
        if vbool[i]:
            HB2=i
            break
    return 255-a[:,HB1:HB2+1]