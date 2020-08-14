import matplotlib.pyplot as plt

training_file  = r"C:\Users\nour.laban\source\repos\darknet\out\build\x64-Debug\resnewanchors.txt"
f = open(training_file, "r")
annolines = f.readlines()
end =  len(annolines)

allloss = []
allavg  =  []
alliterr = []
recallprecsion  = []
i = 0
for j in range(end):
    anno_values = annolines[j].split(',')
    
    linparts = len(anno_values)
    
    if(linparts == 5 and anno_values[1].rsplit()[2] == 'loss' ): 
        
        iterrnum = int( anno_values[0].rsplit(':')[0])
        itloss   = float(anno_values[0].rsplit(':')[1])
        itavg    = float(anno_values[1].rsplit()[0])
        allloss.append(itloss)
        allavg.append(itavg)
        itres = [iterrnum,itavg]
        alliterr.append(itres)
        
        print(itres)
        
tail = .80
head = 1- tail 
        
alllens = len(allavg)  

p = int( head * alllens)     
plt.plot(allavg[p : alllens-1 ])
plt.show()
m =1        
    