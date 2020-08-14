import os
import numpy as np
import cv2
import random 
from collections import namedtuple
Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')


def create_BG_pattren(Atype , contextpath ):
    
    '''    
    background pattrn
            1- predifined color 
            2- random pixel  pattren
            3- random small rondon color squars
    dataset based pattrn 
            4- basic colours in image mean standerd diviation
            5- basic tiles in images includeing non-objects                  
    '''
    
    
    
    if (Atype == 0):
        c = random.randrange(0, 255, 3)
        A =  np.full((800,800,3), [c,c,c])        
        return  A
    if(Atype == 1):
        r =   random.randrange(0, 255, 3)
        g =   random.randrange(0, 255, 3)
        b =   random.randrange(0, 255, 3) 
          
        c = random.randrange(0, 255, 3)
        A =  np.full((800,800,3), [b,g,r]) 
        return  A  
    if(Atype == 2):
        A = np.zeros((800,800,3)) 
        
        for i  in range(0,32):
            for j in range(0,32):
                r =   random.randrange(0, 255, 1)
                g =   random.randrange(0, 255, 1)
                b =   random.randrange(0, 255, 1)       
                A[i*25:i*25 +25  ,j*25:j*25 +25] = [b,g,r]
        return  A 
    if(Atype == 3):            
        A = np.zeros((800,800,3)) 
        
        for i  in range(0,32):
            for j in range(0,32):
                r =   random.randrange(0, 255, 1)
                A[i*25:i*25 +25  ,j*25:j*25 +25] = [r,r,r]
        return  A   
    if(Atype == 4):
        
        mycontexts  = os.listdir(contextpath)
        imgc = cv2.imread(contextpath + mycontexts[0],1)  
        heightc =  imgc.shape[0]
            
                    
        A = np.zeros((800,800,3)) 
        
        for xshift  in range(0,800,heightc):
            for yshift in range(0,800,heightc):
                i = random.randrange(len(mycontexts))
                imgc     =   cv2.imread(contextpath +  mycontexts[i],1)
                height  =   imgc.shape[0]
                width   =   imgc.shape[1]
                 
                                             
                x1 = xshift
                y1 = yshift 
                x2 = x1 + width   
                y2 = y1 + height  
                                
                A[y1:y2 ,x1:x2,:] = imgc                 
                
        return  A   
    
    return A  







def interarea(x1, y1, x2,y2,  xp1,yp1,xp2,yp2):  # returns None if rectangles don't intersect
    
    a = Rectangle(x1, y1, x2,y2)
    b = Rectangle(xp1,yp1,xp2,yp2)
    
    dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
    dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)
    
    if dx < 0 or dy < 0: 
        return 0
    return 1



def  checkspace(xp1,yp1,xp2,yp2,imgletters):
    icount = 0
    for i in imgletters:
        [x1,y1,x2,y2] = i
        intersectarea = interarea(xp1,yp1,xp2,yp2 , x1,y1,x2,y2)  
        if intersectarea == 1 :
            icount = icount +1
    
    if icount: 
        return False
    else :
        return True 
            
            
        
        
        

def writemyimage(lessthan,filename):
    f = open( filename + ".txt", 'w')
    # A = np.zeros((800,800,3)) 
    imgwidth  = 800.0
    imaghight = 800.0
    imagearea = imgwidth *  imaghight
    
    A               = create_BG_pattren(4 , contextpath)
    cv2.imwrite( filename + imextent, A)
    imgletters      = []
        
    letterinfo =    lessthan.pop()
    [letterpath , clsindx, height,width] = letterinfo
    
    x1 = random.randrange(3, imgwidth - width  - 2, 3)
    y1 = random.randrange(3, imaghight - height - 2, 3)
            
    x2 = x1 + width
    y2 = y1 + height
    
    
    boxarea = width *   height
    imgletters.append([x1,y1,x2,y2])
    imgletterarea = boxarea  
                
    letterimg     =   cv2.imread(letterpath,1)
    A[y1:y2 ,x1:x2,:] = letterimg            
    xc = x1 +  width   / 2
    yc = y1 +  height  / 2
    lst = str(clsindx) + " "+  str(xc / imgwidth ) +" " + str(yc/imaghight)  + " " +  str(width/ imgwidth) +" " + str(height/imaghight)
    f.write( lst + "\n"   )    
    
    myiter = 0 
    while imgletterarea <  (1.0/2) * imagearea:
        if len(lessthan) == 0:break
        if myiter >= 150 : break  
        letterinfo =    lessthan.pop()
        
        [letterpath , clsindx, height,width] = letterinfo
        found = 0
        #print (str(imgletterarea * 1.0 / imagearea))
        for ii   in range (500):
            
            x1 = random.randrange(3, imgwidth - width  - 2, 3)
            y1 = random.randrange(3, imaghight - height - 2, 3)
            
           
            x2 = x1 + width
            y2 = y1 + height
           
            spcheck   =  checkspace(x1-3,y1-3,x2+3,y2+3,imgletters)                       
            if spcheck : 
                boxarea = width *   height
                imgletters.append([x1,y1,x2,y2])
                imgletterarea = imgletterarea + boxarea  
                
                
                letterimg     =   cv2.imread(letterpath,1)
                A[y1:y2 ,x1:x2,:] = letterimg 
                
                print(x1,y1)
                         
                xc = x1 +  width   / 2
                yc = y1 +  height  / 2
                lst = str(clsindx) + " "+  str(xc / imgwidth ) +" " + str(yc/ imaghight)  + " " +  str(width/ imgwidth) +" " + str(height/ imaghight)
                f.write( lst + "\n"   )
                found = 1
                #print("ok")
                break
            
       
        if not found : lessthan.append(letterinfo) 
        myiter =  myiter +1   
        print(myiter)  
                
    cv2.imwrite( filename + imextent, A)
    f.close()
    
    
    
   


def  dividtraintest(imagesclasscounts, newimages):
    sumcounts = [0, 0 , 0]
    for i in imagesclasscounts:
        sumcounts[0] = sumcounts[0] + i[0]
        sumcounts[1] = sumcounts[1] + i[1]
        sumcounts[2] = sumcounts[2] + i[2]
        
    m =1
        
    
    

#Atype = 2  
trianval            = "val"
#alfbaa              = ['plane', 'ship' , 'small-vehicle'] 
alfbaa              = ['plane', 'large-vehicle', 'small-vehicle', 'ship', 'harbor', 'ground-track-field', 'soccer-ball-field', 'tennis-court', 'baseball-diamond', 'swimming-pool', 'roundabout', 'basketball-court', 'storage-tank', 'bridge', 'helicopter']
   
imageprintpath      = r"E:\1MyWork\1mypapers\paper6\Object\DOTA dataset compriszed\sample\res\l\\" 
contextpath         = r"E:\1MyWork\1mypapers\paper6\Object\DOTA dataset compriszed\sample\res\c\\"

outputlinuxpath     = r"E:\1MyWork\1mypapers\paper6\Object\DOTA dataset compriszed\sample\words\\"

linuxpathsource     = r"E:\1MyWork\1mypapers\paper6\Object\DOTA dataset compriszed\sample\words\\"

imextent            = ".jpg"


myimages  = os.listdir(imageprintpath)
print(len(myimages))
 
imagesnames = []
imagedim = []         
for i in myimages:
             
    image_file  =  imageprintpath + i 
    imagesnames.append(image_file)  
    
    img = cv2.imread(image_file,1)  
    height =  img.shape[0]
    width  =  img.shape[1]
    imagedim.append([height,width])
    
for Atype in range(4,5):
    imagecollectedpath  = outputlinuxpath+ trianval  + str(Atype) + "\\"
    
    filestxt            = outputlinuxpath + trianval  + str(Atype)+".txt"
    counttxt            = outputlinuxpath + trianval  + str(Atype)+".count"
    
    filestxt_train      = outputlinuxpath + "train_" + trianval  + str(Atype)+".txt"
    filestxt_test       = outputlinuxpath + "test_"  +  trianval  + str(Atype)+".txt"
    
    linuxpath           = linuxpathsource + trianval  + str(Atype) + "\\"
    
    
    # img = img.astype(np.uint8)
    # cv2.imshow('sample image',img)
    # cv2.waitKey(0) # waits until a key is pressed
    # cv2.destroyAllWindows() # destroys the window showing image
    
    x =1
    ftxt = open( filestxt , 'w')
    
     
    step = 800
    pstep = 0  
    
    imagesclasscounts  = []
    newimages        = []
    while(step  <= 800):  
        if(not(  os.path.isdir(imagecollectedpath)) ): 
            os.mkdir(imagecollectedpath)
        lessthan    = []
        myclasses   = []
        for i in range( len(imagesnames)):
            [height,width] =  imagedim[i]               
            
            if height < width:
                    print(str(height) + str(width))
                     
            if height < step and height >= pstep  :
                ind = alfbaa.index(str.split(imagesnames[i],'_')[1])
                lessthan.append([imagesnames[i], ind, height,width])
                
                #myclasses.append(ind)
      
        imround = 0
        lessthan.reverse()
        myclasses.reverse() 
        print(len(lessthan))       
        while (len(lessthan)):
                imgname  = 'train_'+ str(imround)
                filename =  imagecollectedpath +imgname
                writemyimage(lessthan,filename)
                ftxt.write( linuxpath + imgname  + imextent + "\n"   )                                  
                newimages.append(linuxpath + imgname  + imextent + "\n")
                
                imround = imround + 1 
         
        pstep = step
        step  = step * 2
         
    ftxt.close()
    
    
    random.shuffle(newimages)
    
    tsize = int (len(newimages) * 0.8)
    train_data = newimages[:tsize  ]
    test_data = newimages[tsize:]
    
    with open(filestxt_train, 'w') as filehandle:
        for listitem in train_data:
            filehandle.write(listitem)
            
    with open(filestxt_test, 'w') as filehandle:
        for listitem in test_data:
            filehandle.write(listitem)
    m =1
    
    
   
         
