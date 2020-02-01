# evaluate the disparity map(computed) with ground truth

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

gt_path = './results/disparity_map_gt/'
computed_path = './results/disparity_map_opencv/'

def computeDiff(gt_img, computed_img):
    """
    INPUTS:
    gt_img, ground truth disparity image
    computed_img, our computed disparity image
    OUTPUTS:
    err_img, difference expressed on every pixel
    total_err, total difference between gt_img and computed_img
    """
    err_img = np.zeros((len(gt_img), len(gt_img[0])))
    for row in range(len(gt_img)):
        for col in range(len(gt_img[row])):
            if gt_img[row][col] == 0 or computed_img[row][col] ==0:
                continue
            else:
                err_img[row][col] = abs(gt_img[row][col] - computed_img[row][col])
    total_err = np.sum(err_img)
    return err_img, total_err

# for every ground truth disparity map (expressed in left eye)
# as only 59 out of 82 exsist 
for imgid in os.listdir(gt_path):
    imgid_num = int(imgid[0: -4])  # drop the .png
    gt_img = cv2.imread(gt_path + imgid, -1)
    computed_img = cv2.imread(computed_path + imgid, -1)
    err_img, total_err = computeDiff(gt_img, computed_img)
    print(total_err)
    plt.imshow(err_img)
    plt.show()
    break