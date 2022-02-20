from CreateFormula import *
import matplotlib.pyplot as plt
import random
from tqdm import tqdm

os.chdir(os.path.join(__file__,os.path.pardir))

# import letter images
allletter_list=get_letter_pics()

# import operator images
alloperator_list=get_operation_pics()

# import number images
allnumber_list=get_number_pics()

# create dataset image and target
def newbackpic(b,num=1,frame=False):
    '''param
    b: background image
    num: target number
    frame: whether to show the bounding box of formulas

    return: image, target list, target num
    ''' 
    barray=get_barray(b)
    carray=np.zeros(barray.shape).astype(int)
    res=[]
    count=0
    while count<num:
        formula=createformula(allletter_list,alloperator_list,allnumber_list)
        fx,fy=formula.shape
        if fy>=550:
            continue
        formula[formula>200]=255
        formula[formula<=200]=0
        bx,by=begincoords(barray.shape,fx,fy)
        if not coverjudge(carray,bx,by,fx,fy): # no cover
            carray[bx:bx+fx][:,by:by+fy]=1
            for fi in range(fx):
                for fj in range(fy):
                    if formula[fi][fj]<50:
                        barray[fi+bx][fj+by]=0
            count+=1
            res.append([(bx,by),(bx,by+fy),(bx+fx,by),(bx+fx,by+fy)])#left top, right top, left bottom, right bottom
            
    if frame:
        for fr in res:
            bx,by=fr[0][0],fr[0][1]
            fx,fy=fr[2][0]-fr[0][0],fr[1][1]-fr[0][1]
            barray[bx-3:bx+1][:,by-3:by+fy+4]=0 # top boundary
            barray[bx+fx:bx+fx+4][:,by-3:by+fy+4]=0 # bottom boundary
            barray[bx-3:bx+fx+4][:,by-3:by+1]=0 # left boundary
            barray[bx-3:bx+fx+4][:,by+fy:by+fy+4]=0 # right boundary
        
    return Image.fromarray(barray.astype('uint8')),res,len(res)

# create random formula in random background
def create_random_pic(mtn=3,frame=False):
    '''params
    mtn: max target number
    frame: whether to create bounding box of formulas
    '''
    bpath="source/backgroundpics/"+str(random.randint(1,BACKGROUNDPICNUM))+".png"
    background=Image.open(bpath).convert('L')
    num=random.randint(1,mtn)
    return newbackpic(background,num=num,frame=frame)

# create the label in the form that yolov4 needs
def create_txt_target(target_list):
    for i in range(len(target_list)):
        f=open('dataset/label/{}.txt'.format(i),'w',encoding='utf-8')
        targets=target_list[i]
        s='0'
        for t in range(len(targets)):
            target=targets[t]
            width0=target[1][1]-target[0][1] # width
            height0=target[2][0]-target[0][0] # height
            ym=(target[0][0]+target[2][0])/2 # y coords of middle
            xm=(target[0][1]+target[1][1])/2 # x coords of middle
            width=width0/BACKGROUNDSHAPE
            height=height0/BACKGROUNDSHAPE
            xm=xm/BACKGROUNDSHAPE
            ym=ym/BACKGROUNDSHAPE
            stp='0 {0:.3f} {1:.3f} {2:.3f} {3:.3f}\n'.format(xm,ym,width,height)
            f.write(stp)
        f.close()

def create_dataset(num,max_targetnum=3,frame=False):
    targetlist=[]
    numlist=[]
    for i in tqdm(range(num)):
        temp=create_random_pic(mtn=max_targetnum,frame=frame)
        pathtp='dataset/pic/'+str(i)+'.'+'jpg'
        temp[0].save(pathtp)
        targetlist.append(temp[1])
        numlist.append(temp[2])
    create_txt_target(targetlist)

# create dataset
create_dataset(num=10,frame=False)