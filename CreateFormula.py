from utils import *



# multiply without pow
def createformula1(allletter_list):
    letternum=random.randint(1,3)
    blank=(255-np.zeros((SHAPE,SHAPE*letternum))).astype('uint8')
    rowset=set()
    for i in range(letternum):
        while True:
            row=random.randint(0,LETTERNUM-1)# no duplicate 
            if row not in rowset:
                rowset.add(row)
                break
        col=random.randint(0,PICNUM-1)
        lettertp=allletter_list[row][col]
        blank[:,i*SHAPE:i*SHAPE+SHAPE]=lettertp
    return blank

# fraction without pow
def createformula2(allletter_list):
    nnum=random.randint(1,2)
    dnum=random.randint(1,3)
    blank=(255-np.zeros((SHAPE*2+10,SHAPE*max(nnum,dnum)))).astype('uint8')
    rowlist=[]
    # first pick letters, no duplicate
    for i in range(nnum+dnum):
        while True:
            row=random.randint(0,LETTERNUM-1)
            if row not in rowlist:
                rowlist.append(row)
                break
    blank[SHAPE+3:SHAPE+7,:]=0 # fraction line
    if nnum>dnum: # make sure the formula is in the middle of the fraction
        for i in range(nnum):
            col=random.randint(0,PICNUM-1)
            lettertp=allletter_list[rowlist[i]][col]
            blank[:SHAPE,i*SHAPE:i*SHAPE+SHAPE]=lettertp
        delta=int((nnum-dnum)*SHAPE/2)
        for i in range(dnum):
            col=random.randint(0,PICNUM-1)
            lettertp=allletter_list[rowlist[nnum+i]][col]
            blank[SHAPE+10:SHAPE*2+10,delta+i*SHAPE:delta+i*SHAPE+SHAPE]=lettertp
    else:
        for i in range(dnum):
            col=random.randint(0,PICNUM-1)
            lettertp=allletter_list[rowlist[i]][col]
            blank[SHAPE+10:SHAPE*2+10,i*SHAPE:i*SHAPE+SHAPE]=lettertp
        delta=int((dnum-nnum)*SHAPE/2)
        for i in range(nnum):
            col=random.randint(0,PICNUM-1)
            lettertp=allletter_list[rowlist[dnum+i]][col]
            blank[:SHAPE,delta+i*SHAPE:delta+i*SHAPE+SHAPE]=lettertp
    return blank

# polynomial without pow
def createformula3(allletter_list,alloperator_list,num,firstminus=False):
    '''param:
    num: number of terms
    firstminus: determine whether the first term is negative
    '''
    DIVIDE=5 # division in fraction
    # first determine the number of terms in polynomial
    if num>1:
        fracnum=random.randint(0,num//2)
        if (not fracnum) and random.randint(0,1):
            fracnum=num
    else:
        fracnum=random.randint(0,1)
    multnum=num-fracnum
    # create the multiplication and fractions
    multlen,fraclen=0,0
    fraclist=[]
    multlist=[]
    blank=0
    for _ in range(fracnum):
        tp=createformula2(allletter_list)
        fraclist.append(tp)
        fraclen+=tp.shape[1]
    for _ in range(multnum):
        tp=createformula1(allletter_list)
        multlist.append(tp)
        multlen+=tp.shape[1]
    rowdelta,coldelta=0,0
    
    # adjust horizontal division
    if firstminus:
        coldelta=SHAPE+DIVIDE
    
    # calculate the length of formula
    if fracnum==0:# no fraction
        brow,bcol=SHAPE,multlen+(num-1+firstminus)*SHAPE+(2*num-2+firstminus)*DIVIDE
        blank=(255-np.zeros((brow,bcol))).astype('uint8')
    else:# if there are fractions, the place of multiplications needs to be adjusted
        brow,bcol=SHAPE*2+10,fraclen+multlen+(num-1+firstminus)*SHAPE+(2*num-2+firstminus)*DIVIDE
        blank=(255-np.zeros((brow,bcol))).astype('uint8')
        rowdelta=int((SHAPE+10)/2)

    multlist.extend(fraclist)
    random.shuffle(multlist)

    nextcol=0
    if firstminus:
        blank[rowdelta:rowdelta+SHAPE][:,nextcol:nextcol+SHAPE]=getop(alloperator_list,1)
        nextcol+=SHAPE+DIVIDE
    
    for i in range(len(multlist)):
        tp=multlist[i]
        if tp.shape[0]==SHAPE: # multiplication
            blank[rowdelta:rowdelta+tp.shape[0]][:,nextcol:nextcol+tp.shape[1]]=tp
            nextcol+=DIVIDE+tp.shape[1]
            if i==len(multlist)-1:
                break
            blank[rowdelta:rowdelta+SHAPE][:,nextcol:nextcol+SHAPE]=getop(alloperator_list,random.randint(0,1))
            nextcol+=SHAPE+DIVIDE
        else: # fraction
            blank[:,nextcol:nextcol+tp.shape[1]]=tp
            nextcol+=DIVIDE+tp.shape[1]
            if i==len(multlist)-1:
                break
            blank[rowdelta:rowdelta+SHAPE][:,nextcol:nextcol+SHAPE]=getop(alloperator_list,random.randint(0,1))
            nextcol+=SHAPE+DIVIDE
    if (255-blank)[:,-45:].any()==0:
        blank=blank[:,:-45]
    return blank

# multiplication with pow
def createformula_square1(allnumber_list,allletter_list):
    letternum=random.randint(1,3)
    squarenum=random.randint(1,letternum)
    blank=(255-np.zeros((SHAPE+NUMBERSHAPE,SHAPE*letternum))).astype('uint8')

    # pick letters
    rowset=set()
    for i in range(letternum):
        while True:
            row=random.randint(0,LETTERNUM-1)
            if row not in rowset:
                rowset.add(row)
                break
        col=random.randint(0,PICNUM-1)
        lettertp=allletter_list[row][col]
        blank[NUMBERSHAPE:,i*SHAPE:i*SHAPE+SHAPE]=lettertp

    idxs=random.sample(np.arange(0,letternum,1).tolist(),squarenum)# index of letters to add pow
    
    def array_add(array):
        s=0
        for i in array:
            s+=i
        return s
    
    for i in range(len(idxs)):
        temp=255-np.zeros((SHAPE+NUMBERSHAPE,NUMBERSHAPE)).astype(int)
        temp[:NUMBERSHAPE]=getnumber(allnumber_list)
        addn=array_add(np.array(idxs[:i])<idxs[i])
        blank=np.concatenate([blank[:,:SHAPE*(idxs[i]+1)+NUMBERSHAPE*addn],temp,blank[:,SHAPE*(idxs[i]+1)+NUMBERSHAPE*addn:]],axis=1)
    return blank

# fraction with pow
def createformula_square2(allnumber_list,allletter_list):
    def array_add(array):
        s=0
        for i in array:
            s+=i
        return s

    def create_frac_square(letterlist):
        letternum=len(letterlist)
        squarenum=random.randint(1,letternum)
        blank=(255-np.zeros((SHAPE+NUMBERSHAPE,SHAPE*letternum))).astype('uint8')
        for i in range(letternum):
            col=random.randint(0,PICNUM-1)
            lettertp=allletter_list[letterlist[i]][col]
            blank[NUMBERSHAPE:,i*SHAPE:i*SHAPE+SHAPE]=lettertp

        idxs=random.sample(np.arange(0,letternum,1).tolist(),squarenum)# index of letters to add pow
        for i in range(len(idxs)):
            temp=255-np.zeros((SHAPE+NUMBERSHAPE,NUMBERSHAPE)).astype(int)
            temp[:NUMBERSHAPE]=getnumber(allnumber_list)
            addn=array_add(np.array(idxs[:i])<idxs[i])
            blank=np.concatenate([blank[:,:SHAPE*(idxs[i]+1)+NUMBERSHAPE*addn],temp,blank[:,SHAPE*(idxs[i]+1)+NUMBERSHAPE*addn:]],axis=1)
        return blank


    INTERVAL=10

    nnum=random.randint(1,2)
    dnum=random.randint(1,3)
    rowlist=[]
    for i in range(nnum+dnum):
        while True:
            row=random.randint(0,LETTERNUM-1)
            if row not in rowlist:
                rowlist.append(row)
                break

    narray=create_frac_square(rowlist[:nnum])
    darray=create_frac_square(rowlist[nnum:])
    nshape1=narray.shape[1]
    dshape1=darray.shape[1]

    if nshape1>dshape1:
        ablank=(255-np.zeros((SHAPE*2+10+2*NUMBERSHAPE,nshape1+INTERVAL*2))).astype('uint8')
        itv=int((ablank.shape[1]-dshape1)/2)
        ablank[:SHAPE+NUMBERSHAPE][:,INTERVAL:INTERVAL+nshape1]=narray
        ablank[-(SHAPE+NUMBERSHAPE):][:,itv:itv+dshape1]=darray
    else:
        ablank=(255-np.zeros((SHAPE*2+10+2*NUMBERSHAPE,dshape1+INTERVAL*2))).astype('uint8')
        itv=int((ablank.shape[1]-nshape1)/2)
        ablank[:SHAPE+NUMBERSHAPE][:,itv:itv+nshape1]=narray
        ablank[-(SHAPE+NUMBERSHAPE):][:,INTERVAL:INTERVAL+dshape1]=darray
        
    ablank[SHAPE+NUMBERSHAPE+3:SHAPE+NUMBERSHAPE+7]=0

    return ablank

# polynomial with pow
def createformula4(allnumber_list,allletter_list,alloperator_list,num,firstminus=False):
    DIVIDE=5
    if num>1:
        fracnum=random.randint(0,num//2)
        if (not fracnum) and random.randint(0,1):
            fracnum=num
    else:
        fracnum=random.randint(0,1)
    multnum=num-fracnum
    multlen,fraclen=0,0
    fraclist=[]
    multlist=[]
    blank=0
    for _ in range(fracnum):
        judgenumber=random.randint(0,2)
        if judgenumber:
            tp=createformula_square2(allnumber_list,allletter_list)
        else:
            tp=createformula2(allletter_list)
        fraclist.append(tp)
        fraclen+=tp.shape[1]
    for _ in range(multnum):
        judgenumber=random.randint(0,2)
        if judgenumber:
            tp=createformula_square1(allnumber_list,allletter_list)
        else:
            tp=createformula1(allletter_list)
        multlist.append(tp)
        multlen+=tp.shape[1]

    coldelta=0
    if firstminus:
        coldelta=SHAPE+DIVIDE
    
    brow,bcol=SHAPE*2+10+NUMBERSHAPE*2,fraclen+multlen+(num-1+firstminus)*SHAPE+(2*num-2+firstminus)*DIVIDE
    blank=(255-np.zeros((brow,bcol))).astype('uint8')

    multlist.extend(fraclist)
    random.shuffle(multlist)

    nextcol=0
    if firstminus:
        blank[int((brow-SHAPE)/2):int((brow-SHAPE)/2)+SHAPE][:,nextcol:nextcol+SHAPE]=getop(alloperator_list,1)
        nextcol+=SHAPE+DIVIDE
    
    for i in range(len(multlist)):
        tp=multlist[i]
        blank[int((brow-tp.shape[0])/2):int((brow-tp.shape[0])/2)+tp.shape[0]][:,nextcol:nextcol+tp.shape[1]]=tp
        nextcol+=DIVIDE+tp.shape[1]
        if i==len(multlist)-1:
            break
        blank[int((brow-SHAPE)/2):int((brow-SHAPE)/2)+SHAPE][:,nextcol:nextcol+SHAPE]=getop(alloperator_list,random.randint(0,1))
        nextcol+=SHAPE+DIVIDE
    if (255-blank)[:,-45:].any()==0:
        blank=blank[:,:-45]
    return blank

def createformula(allletter_list,alloperator_list,allnumber_list):
    judge=random.randint(0,99)
    if judge<=9: # multiply without pow 10%
        return createformula1(allletter_list)
    elif judge<=19: # fraction without pow 10%
        return createformula2(allletter_list)
    elif judge<=34: #multiply with pow 15%
        return createformula_square1(allnumber_list,allletter_list)
    elif judge<=49: #fraction with pow 15%
        return createformula_square2(allnumber_list,allletter_list)
    elif judge<=69: #polynomial without pow 20%
        num,fm=random.randint(2,3),random.randint(0,2)
        return createformula3(allletter_list,alloperator_list,num=num,firstminus=fm)
    elif judge<=89: #polynomial with pow 20%
        num,fm=random.randint(2,3),random.randint(0,2)
        return createformula4(allnumber_list,allletter_list,alloperator_list,num=num,firstminus=fm)
    elif judge<=94: # multiply without pow with negative first term 5%
        return createformula3(allletter_list,alloperator_list,1,True)
    else: # multiply with pow with negative first term 5%
        return createformula4(allnumber_list,allletter_list,alloperator_list,1,True)