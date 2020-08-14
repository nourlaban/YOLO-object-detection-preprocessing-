# Python program to explain cv2.rectangle() method 

# importing cv2 
import cv2 
import os

# path 
impath = r'E:\1MyWork\1mypapers\paper6\Object\darknet\data\alpha\cwords\exper7\words\\'
rectimpath = r'E:\1MyWork\1mypapers\paper6\Object\darknet\data\alpha\cwords\exper7\rectJPEGImages\\'
pathtxts = r'E:\1MyWork\1mypapers\paper6\Object\darknet\data\alpha\cwords\exper7\words\\'


window_name = 'Image'
images      = [i for i in os.listdir(impath) if 'png' in i]
imagetxt    = [i for i in os.listdir(pathtxts) if 'txt' in i]
count =  0

for j in images:
    image = cv2.imread(impath + j) 
    name = j.split('.') 
    file1 = open(pathtxts + name[0] + '.txt' , 'r') 
    a = file1.readlines() 
    for m in a: 
            parts =  m.rsplit()
           
            
            w  = int(float(parts[3])*800)  
            h =  int(float(parts[4])*800) 
            
            x1 =  int(float(parts[1])*800) - int (w/2.0)
            y1 =  int(float(parts[2])*800) - int (h/2.0)
            
            start_point = ( x1 ,y1) 
            end_point = (x1+ w , y1 +h)
            color = (255, 0, 0) 
            thickness = 2
            image = cv2.rectangle(image, start_point, end_point, color, thickness) 
    file1.close()    
    cv2.imwrite(rectimpath + j,image) 
    # Displaying the image 
#     cv2.imshow(window_name, image) 
#     cv2.waitKey()
#     cv2.destroyAllWindows() 
#     c = 1       

# Displaying the image 
cv2.imshow(window_name, image) 
cv2.waitKey()
cv2.destroyAllWindows() 
