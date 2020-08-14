from shutil import copyfile
mypath = 'labelTxtvalpcs/'
from os import listdir
from os.path import isfile, join,splitext


onlyfiles = [splitext(f)[0] for f in listdir(mypath) if isfile(join(mypath, f))]


for a in onlyfiles:  
    copyfile('imagesthird220/'+ a + ".png" , "imagesthird220sub/"+a+".png" )