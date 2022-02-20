import random
import os
from ProcessRawPic import *

os.chdir(os.path.join(__file__,os.path.pardir))

# get coordinate to print formula
def begincoords(bshape,blankx,blanky):
    while True:
        xlim=bshape[0]-blankx
        ylim=bshape[1]-blanky
        if xlim>=6 and ylim>=6:
            break
        #time+=1
        #if time>100:
        else:
            return 0,0
    x=random.randint(3,xlim-3)
    y=random.randint(3,ylim-3)
    return x,y

# cover judge
def coverjudge(carray,bx,by,fx,fy):
    tp=carray[bx:bx+fx][:,by:by+fy]
    if tp.any():
        return True # cover
    else:
        return False # no cover

# get random operator
def getop(alloperator_list,kind):
    return alloperator_list[kind][random.randint(0,PICNUM-1)]

# get random number images
def getnumber(allnumber_list):
    return allnumber_list[random.randint(0,NUMBERNUM-1)][random.randint(0,PICNUM-1)]

# randomly crop background image to the given size
def get_barray(b):
    barray=np.array(b).astype(int)
    bx,by=barray.shape
    rx=random.randint(0,bx-BACKGROUNDSHAPE-1)
    ry=random.randint(0,by-BACKGROUNDSHAPE-1)
    return barray[rx:rx+BACKGROUNDSHAPE][:,ry:ry+BACKGROUNDSHAPE]