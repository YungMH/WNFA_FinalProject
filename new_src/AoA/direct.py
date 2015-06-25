import os
import glob

path = '/Volumes/Transcend/GitHub/WNFA_FinalProject/new_src/AoA'
file_list = []

for filename in glob.glob(os.path.join(path, '*.png')):
    print filename
    file_list.push(filename)
print file_list
