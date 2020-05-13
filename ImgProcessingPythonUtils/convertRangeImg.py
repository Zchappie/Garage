import numpy as np 
import cv2
import os
import shutil

subFolder = '../../source/ranges/'
for img in os.listdir('../../source/nlr_imgs_converted/'):
    if img.endswith(".png"):
        # print(os.path.join('../../source/nlr_imgs/', img))
        rangeFileName = os.path.join('../../source/nlr_imgs_converted/', img)
        if 'range' in rangeFileName:
            # print(rangeFileName)
            shutil.move(rangeFileName, subFolder)
            # break
        # rangeImg = cv2.imread(rangeFileName)

        # # scaling factor
        # maxPxlValue = rangeImg.max()
        # minPxlValue = rangeImg.min()
        # # print('The max pixel value is ', maxPxlValue, '\nThe min pixel value is ', minPxlValue)
        # alpha = 255/(maxPxlValue-minPxlValue)
        # # shifting factor
        # beta = -min(minPxlValue * alpha, maxPxlValue * alpha)
        # normalizedImg = np.float32(rangeImg) * alpha + beta
        # normalizedImg = np.uint8(normalizedImg)
        # im_color = cv2.applyColorMap(normalizedImg, cv2.COLORMAP_BONE)
        # cv2.imwrite(os.path.join('../../source/nlr_imgs_converted/', img), im_color)

