import os
import numpy as np
import cv2
import random 

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
    
    

def writemyimage(lessthan,myclasses,step,filename):
    f = open( filename + ".txt", 'wb')
    # A = np.zeros((800,800,3)) 
    
    A = create_BG_pattren(Atype , contextpath)
    classcounts = [0, 0,0]
    for xshift in range(0, 800, step):
        for yshift in range(0, 800, step):
            if(len(lessthan) > 0):
                
                c       =   myclasses.pop()
                imgpath =   lessthan.pop()
                img     =   cv2.imread(imgpath,1)
                
                classcounts[c] = classcounts[c] + 1
               
                height  =   img.shape[0]
                width   =   img.shape[1]
                 
                                             
                x1 = step/2 -1 - width/2   + xshift
                y1 = step/2 -1 - height/2  + yshift 
                x2 = x1 + width   
                y2 = y1 + height  
                A[y1:y2 ,x1:x2,:] = img
                 
                xc = x1 +  width   / 2
                yc = y1 +  height  / 2
                lst = str(c) + " "+  str(xc / 800.0 ) +" " + str(yc/ 800.0)  + " " +  str(width/ 800.0) +" " + str(height/ 800.0)
                f.write( lst + "\n"   )
                
     
#          
    cv2.imwrite( filename + ".jpg", A)
    f.close()
    return  classcounts     


def  dividtraintest(imagesclasscounts, newimages):
    sumcounts = [0, 0 , 0]
    for i in imagesclasscounts:
        sumcounts[0] = sumcounts[0] + i[0]
        sumcounts[1] = sumcounts[1] + i[1]
        sumcounts[2] = sumcounts[2] + i[2]
        
    m =1
        
    
    

#Atype = 2  
trianval            = "val"
alfbaa              = ['plane', 'ship' , 'small-vehicle']    
imageprintpath      = "../data/alpha/bletters/exper3/val/alltrainletters/" 
contextpath         = "../data/alpha/bletters/exper3/val/alltraincontext100/"


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
    
for Atype in range(5):
    imagecollectedpath  = "../data/alpha/cwords/exper3/" + trianval  + str(Atype) + "/"
    
    filestxt            = "../data/alpha/cwords/exper3/" + trianval  + str(Atype)+".txt"
    counttxt            = "../data/alpha/cwords/exper3/" + trianval  + str(Atype)+".count"
    
    filestxt_train      = "../data/alpha/cwords/exper3/" + "train_" + trianval  + str(Atype)+".txt"
    filestxt_test       = "../data/alpha/cwords/exper3/" + "test_"  +  trianval  + str(Atype)+".txt"
    
    dirpath = os.getcwd() 
    
    linuxpath           = os.path.join(dirpath,imagecollectedpath )        #"data/obj/"
    
    
    # img = img.astype(np.uint8)
    # cv2.imshow('sample image',img)
    # cv2.waitKey(0) # waits until a key is pressed
    # cv2.destroyAllWindows() # destroys the window showing image
    
    x =1
    ftxt = open( filestxt , 'wb')
    ctxt = open( counttxt , 'wb')
     
    step = 50
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
                lessthan.append(imagesnames[i])
                ind = alfbaa.index(str.split(imagesnames[i],'_')[1])
                myclasses.append(ind)
      
        imround = 0
        lessthan.reverse()
        myclasses.reverse() 
        print(len(lessthan))       
        while (len(lessthan)):
                imgname  = 'train_'+str(step)+"_" + str(imround)
                filename =  imagecollectedpath +imgname
                classcounts = writemyimage(lessthan,myclasses,step,filename)
                ftxt.write( linuxpath + imgname  + ".jpg" + "\n"   )
                ctxt.write( str(classcounts[0]) + ","+ str(classcounts[1]) + ","+str(classcounts[2]) + "\n"   )
                
                imagesclasscounts.append(classcounts)
                newimages.append(linuxpath + imgname  + ".jpg" + "\n")
                
                imround = imround + 1 
         
        pstep = step
        step  = step * 2
         
    ftxt.close()
    ctxt.close() 
    
    random.shuffle(newimages)
    
    tsize = int (len(newimages) * .8)
    train_data = newimages[:tsize  ]
    test_data = newimages[tsize:]
    
    with open(filestxt_train, 'wb') as filehandle:
        for listitem in train_data:
            filehandle.write(listitem)
            
    with open(filestxt_test, 'wb') as filehandle:
        for listitem in test_data:
            filehandle.write(listitem)
    m =1
    
    
   
         
