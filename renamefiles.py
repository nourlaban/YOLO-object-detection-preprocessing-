
from os import listdir
from os.path import isfile, join
mypath = "E:\youtube-dl\Noura and Rashed\songs\New folder\\"
mmm = listdir(mypath) 
x = mmm[0]
ext_unicode = unicode(x, 'utf-8')
s = x.parse('_')

m= 1