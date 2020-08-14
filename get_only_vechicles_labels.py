#===============================================================================
# 
#===============================================================================
mypath = r'E:\1MyWork\1mypapers\paper6\Object\DOTA dataset compriszed\R2CNN\DOTA\val\v1\labelTxt'
newpath= 'allval/labelTxtval/'
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]



i = 0
p = 0
c = 0 
sh = 0
for a in  onlyfiles:    
    with open(join(mypath, a)) as f:
        
        print(a)
        strfile = ''
        vechiclefound = 0
        
        
        imagesource = f.readline()
        res         = f.readline()  
             
        strfile = imagesource + res
        
        
        
        for line in f:
            
            s = line.split() 
            v = s[8]  
            
            if v == 'plane' or v == 'ship' or v == 'small-vehicle':
                i = i +1     
                strfile = strfile + line  
                vechiclefound = 1       
                
                
                
            if v == 'plane':
                p =p + 1
            if v == 'ship':
                sh = sh + 1
            if v == 'small-vehicle':
                c =c + 1
    
    f.close()    
#     if vechiclefound == 1  :
#         of=open(join(newpath ,a), "wb")
#         of.writelines(strfile)
#         of.close()
         
    
print(i)  
print(c)  
print(sh)  
print(p)    