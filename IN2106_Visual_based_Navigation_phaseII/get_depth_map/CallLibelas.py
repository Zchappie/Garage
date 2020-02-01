# from PIL import Image
import subprocess
import os
from pathlib import Path

dirpath = os.getcwd()
print(dirpath)

# load the use-able camera ids
f=open("../../data/euroc_V1/timestamps.txt", "r")
if f.mode == 'r':
    f1 = f.readlines()
    cam_ids = []
    for x in f1:
        cam_ids += [int(x)]
else:
    print("Can't open file timestamps.txt")

# img_path_0 = str(dirpath) + '/results/rect_0/'
# img_path_1 = str(dirpath) + '/results/rect_1/'
img_path_0_new = str(dirpath) + '/results/rect_0_pgm/'
img_path_1_new = str(dirpath) + '/results/rect_1_pgm/'

# for imgid in os.listdir(img_path_0):
#     imgid_num = int(imgid[0: -4])
#     if imgid_num in cam_ids:
#         os.rename(os.path.join(img_path_0, imgid), os.path.join(img_path_0_new, imgid))
#     else:
#         continue

# for imgid in os.listdir(img_path_1):
#     imgid_num = int(imgid[0: -4])
#     if imgid_num in cam_ids:
#         os.rename(os.path.join(img_path_1, imgid), os.path.join(img_path_1_new, imgid))
#     else:
#         continue
# for loop will start from here, for every images
for imgid in os.listdir(img_path_0_new):
    commandLine = str(dirpath) + "/libelas/elas " + img_path_0_new + imgid + " " + img_path_1_new + imgid
    os.system(commandLine)
    # commandLine = "magick convert " + img_path_1_new + imgid +" "+ img_path_1_new + imgid[:-4] + ".pgm"
    # os.system(commandLine)

    # print(imgid)
    # break