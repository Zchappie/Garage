	
import shutil
import subprocess
import os
from pathlib import Path

dirpath = os.getcwd()
# load the use-able camera ids
f=open("../../data/euroc_V1/timestamps.txt", "r")
if f.mode == 'r':
    f1 = f.readlines()
    cam_ids = []
    for x in f1:
        cam_ids += [int(x)]
else:
    print("Can't open file timestamps.txt")

img_path_0 = str(dirpath) + '/results/rect_0/'
img_path_1 = str(dirpath) + '/results/rect_1/'
img_path_0_new = str(dirpath) + '/results/rect_0_min/'
img_path_1_new = str(dirpath) + '/results/rect_1_min/'

for imgid in os.listdir(img_path_0):
    imgid_num = int(imgid[0: -4])
    if imgid_num in cam_ids:
        newPath = shutil.copy(os.path.join(img_path_0, imgid), os.path.join(img_path_0_new, imgid))
    else:
        continue

for imgid in os.listdir(img_path_1):
    imgid_num = int(imgid[0: -4])
    if imgid_num in cam_ids:
        newPath = shutil.copy(os.path.join(img_path_1, imgid), os.path.join(img_path_1_new, imgid))
    else:
        continue