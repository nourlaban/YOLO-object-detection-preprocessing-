import os


path        = r'E:\1MyWork\1 my papers\paper 6\Object\darknet\transform\newsitting\setting_training_4'

myfile      =  path +  r'\val0\resultval0test.txt'
f           = open( myfile , "r")
lines       = f.readlines()
f.close()

alfbaa     = ['plane', 'ship' , 'car']    

images         = []
numbersclasses = []
imageindex = -1

image_cls     = [0,0,0]
classarr      = []
for line in lines:
    
    segments = line.split(':')
    #print (segments)
    if len(segments) == 3:
        imagepath  =  segments[1]
        imagename  =  imagepath.split('/')[3]
        if imageindex >= 0:
            classarr.append(image_cls)
        imageindex = imageindex +1   
        image_cls     = [0,0,0]
        images.append(imagename)
        
        
        

    if len(segments) == 2:
        classname =  segments[0]
        
        if classname ==  alfbaa[0]:
            image_cls[0] = image_cls[0] +1
        if classname ==  alfbaa[1]:
            image_cls[1] = image_cls[1] +1
        if classname ==  alfbaa[2]:
            image_cls[2] = image_cls[2] +1    
        mystr = segments[1]
        if  mystr != ' ':
            classprob = int(mystr.split('%')[0])
    m = 1
classarr.append(image_cls)    
    
m2 = 1    
    
    
    
    
    
    