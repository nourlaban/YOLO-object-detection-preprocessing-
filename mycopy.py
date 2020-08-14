import os
path = 'alphabit2allval/'
files = os.listdir(path)


for f in files:
    ff = f.replace('valval', 'val_')
    os.rename(os.path.join(path, f), os.path.join(path,  ff ))