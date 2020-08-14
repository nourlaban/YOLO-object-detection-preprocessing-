import os
import numpy as np
import cv2
import imutils
import random 
# import matplotlib.pyplot as plt
# import pandas as pd
# from sklearn.datasets.samples_generator import make_blobs
# from sklearn.cluster import KMeans




def get_text_data(annotation_file):
    f = open(annotation_file, "r")
    annolines = f.readlines()
    annolines= annolines[2:]
    boxes = []
    cats =  []
    difs = []
    rects = []
    end =  len(annolines)
    for j in range(end):
        anno_values = annolines[j].split()
        x1 = int(anno_values[0])
        y1 = int(anno_values[1])
        x2 = int(anno_values[2])
        y2 = int(anno_values[3])
        x3 = int(anno_values[4])
        y3 = int(anno_values[5])
        x4 = int(anno_values[6])
        y4 = int(anno_values[7])
        
        xs = [x1,x2,x3,x4]
        ys = [y1,y2,y3,y4]
        
        xmin =   min(xs)
        ymin =   min(ys)
        
        xmax =   max(xs)
        ymax =   max(ys)
        category  = anno_values[8]
        difficult = anno_values[9]
        rect = [xmin,ymin,xmax,ymin,xmin,ymax,xmax,ymax]
        box = np.int0(rect)
        box = box.reshape([4, 2])
        rect1 = cv2.minAreaRect(box)
        #xc, yc, w, h, theta = rect1[0][0], rect1[0][1], rect1[1][0], rect1[1][1], rect1[2]
        boxes.append(rect1)
        cats.append(category)
        rects.append(rect)
        difs.append(difficult)
   
    return boxes,cats,difs,rects


datapath          = r'E:\1MyWork\1mypapers\paper6\Object\DOTA dataset compriszed\R2CNN\DOTA\val\v1\labelTxt\\'
imagepth          = r'E:\1MyWork\1mypapers\paper6\Object\DOTA dataset compriszed\R2CNN\DOTA\val\images\images\\' 
imageleterspath   = "../data/alpha/bletters/exper5alldata/train/alltrainletters/" 
imagecontextspath = '../data/alpha/bletters/exper5alldata/train/alltraincontext100/'
tilewidth  = 100
tile_img   = 10


wh =  []
l =0    
myimages  = os.listdir(datapath)
for i in myimages:
    name = i.split('.')
    annotation_file  =  datapath + name[0]+ ".txt" 
    boxes,cats,difs,rects = get_text_data(annotation_file)
        
    image_file  =  imagepth + name[0]+ ".png" 
    img = cv2.imread(image_file,1)
        
    
    l= l+  len(boxes)
    
    for j in range( len(boxes)):
            rect = boxes[j]         
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            
            width = int(rect[1][0])
            height = int(rect[1][1])
            x = np.array([width,height])
            wh = np.append(wh,x)
            
            src_pts = box.astype("float32")
            dst_pts = np.array([[0, height-1],
                                [0, 0],
                                [width-1, 0],
                                [width-1, height-1]], dtype="float32")
            M = cv2.getPerspectiveTransform(src_pts, dst_pts)
            warped = cv2.warpPerspective(img, M, (width, height))
            width  = warped.shape[1]
            height = warped.shape[0]
            if width  >  height :
                warped = imutils.rotate_bound(warped, 90)
                t      =  width
                width  = height
                height = t 
                                       
            m =1    
            subimagename =  imageleterspath + name[0] +'_'+ cats[j]+'_'+ difs[j]+"_"+ str(j)+'.png'
            if np.max(warped) > 0:
                cv2.imwrite( subimagename, warped)
            with open('somefile.txt', 'a') as the_file:
                the_file.write(subimagename + "\t" +str(width) + "\t" + str(height) + "\n" )
                
            
    
    
    for j in range( len(boxes)):
        rect = boxes[j]         
        box = cv2.boxPoints(rect)
        box = np.int0(box)
            
        width = int(rect[1][0])
        height = int(rect[1][1])  
        cv2.drawContours(img, [box], 0, (0, 0, 0),height)      
            
        
#     cv2.imshow('sample image',img)
#     cv2.waitKey(0) # waits until a key is pressed
#     cv2.destroyAllWindows() # destroys the window showing image
    
   
    
    imgwidth   =  img.shape[1]
    imghieght  =  img.shape[0]
    imgwstep   = int(imgwidth/tilewidth) 
    imghstep   = int(imghieght/tilewidth)
    imgstatics = []  
    meanarr    = []    
    for wi  in range(0,imgwstep):
        for hj in range(0,imghstep):
            
            
            subimg  = img[ hj*tilewidth:hj*tilewidth +tilewidth, wi*tilewidth:wi*tilewidth +tilewidth]
            subgray = cv2.cvtColor(subimg, cv2.COLOR_BGR2GRAY)
            
            if  np.mean(subgray) > 20 :
                imgstat =  [hj,wi]
                meanarr.append(np.var(subgray))               
                imgstatics.append(imgstat)           
            
            
            #imgmean = mean(subimg)        
            
            m =11 
      
    a =  np.argsort(meanarr)
    alen = len(a)
    if alen > tile_img  :
        astep = alen / tile_img
        for stile in range (0,alen, astep):
            imgindex        = a[stile]
            imgxy           = imgstatics[imgindex]
            hj              = imgxy[0]
            wi              = imgxy[1]
            subimg          = img[ hj*tilewidth:hj*tilewidth +tilewidth, wi*tilewidth:wi*tilewidth +tilewidth]
            
            subimagename    = imagecontextspath + str(tilewidth)+ '_' +  name[0] +'_'+ str(stile) +'.png'
            cv2.imwrite( subimagename, subimg)
            
    m =1
        
        
        
    
# newwh = wh.reshape([l,2])    
# 
# 
# kmeans = KMeans(n_clusters=20, init='k-means++', max_iter=300, n_init=10, random_state=0)
# pred_y = kmeans.fit_predict(newwh)
# 
# m = kmeans.predict(newwh)
# plt.scatter(newwh[:,0], newwh[:,1])
# plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=300, c='red')
# plt.show()




m =1