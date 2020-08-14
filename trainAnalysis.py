import pandas as pd

training_file  = "newsitting/setting_training_2/resnewanchors.txt"
f = open(training_file, "r")
annolines = f.readlines()
end =  len(annolines)

recallprecsion  = []
for j in range(end):
    anno_values = annolines[j].split(',')
    linparts = len(anno_values)
    if(linparts == 4): 
        precision_values = anno_values[1].split()
        if(precision_values[0] == 'precision' ): 
            prevalue =   float(precision_values[2])  
                     
            recall_values    = anno_values[2].split() 
            recvalue         = float(recall_values[2])
            
            recallprecsion.append([recvalue,prevalue])
            print(anno_values)
    m =1
    
df = pd.DataFrame(recallprecsion,
                  columns=['recall', 'precsion'])
ax1 = df.plot.scatter(x='recall',
                      y='precsion'
                     )    
m =1     
    