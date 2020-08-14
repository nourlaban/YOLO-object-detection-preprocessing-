import imutils
import cv2
import os


mypath = r'E:\1MyWork\1mypapers\paper6\Object\DOTA dataset compriszed\R2CNN\DOTA\val\images\images\\'
imgstr = 'P1415_1'
rotatepath = imgpath+imgstr
if(not(  os.path.isdir(rotatepath)) ): 
        os.mkdir(rotatepath)

img = cv2.imread(imgpath + imgstr + '.png' ,1) 
for ang in range(0,181,15):
    
    rimg = imutils.rotate_bound(img, ang)
    cv2.imwrite( rotatepath + "/" + imgstr + '_'+ str(ang)+ '.jpg', rimg)