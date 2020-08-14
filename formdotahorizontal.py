import os
import numpy as np
import cv2
import imutils
import random 
import shutil
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
        
        width  = xmax - xmin
        height = ymax - ymin
        
        alfbaa              = ['plane', 'ship' , 'small-vehicle'] 
        
        
        category = alfbaa.index(anno_values[8])
       
        
        
        
        difficult = anno_values[9]
        rect = [xmin,ymin,width ,height,category]
        
        boxes.append(rect)
        cats.append(category)
        rects.append(rect)
        difs.append(difficult)
   
    return boxes,cats,difs,rects



datapath          = r'E:\1MyWork\1mypapers\paper6\Object\darknet\data\alpha\apcs_lables\allvallabelTxt\\'
imagepth          = r'E:\1MyWork\1mypapers\paper6\Object\DOTA dataset compriszed\R2CNN\DOTA\val\images\images\\' 
targetimage       = r"E:\1MyWork\1mypapers\paper6\Object\darknet\data\alpha\cwords\exper7\rawimages\\"

imagenewpath   = r"E:\1MyWork\1mypapers\paper6\Object\darknet\data\alpha\cwords\exper7\\" 

myimages  = os.listdir(datapath)
for i in myimages:
    name = i.split('.')
    image_file  =  imagepth + name[0]+ ".png" 
    image_target = targetimage + name[0]+ ".png"
   
    
    shutil.copyfile(image_file, image_target)
    

m =1