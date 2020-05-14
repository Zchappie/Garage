import numpy as np 
import cv2
import os
import shutil

def moveFilesToAnotherFolderAccordingToName(sourceFolder, targetFolder, targetChar):
    """
    sourceFolder: source folder of files to be moved
    targetFolder: target folder to move the files to
    targetChar: string to match the file name
    """
    for fileName in os.listdir(sourceFolder):
        filePath = os.path.join(sourceFolder, fileName)
        if targetChar in filePath:
            shutil.move(filePath, targetFolder)

def normalizeRangeFiles(sourceFolder, targetFolder):
    """
    This function corresponds to falseColorConverter.cpp.
    sourceFolder: source folder of files to be moved
    targetFolder: target folder to move the files to, after the file is processed
    """
    counter = 0
    for fileName in os.listdir(sourceFolder):
        counter += 1        
        filePath = os.path.join(sourceFolder, fileName)
        rangeImg = cv2.imread(filePath)
        
        # scaling factor
        maxPxlValue = rangeImg.max()
        minPxlValue = rangeImg.min()
        if maxPxlValue == minPxlValue:
            print("Dividing zero here at ", counter, "-th image, and it has been moved to a trash, your majesty.")
            shutil.move(filePath, './ranges_without_process/')
            continue
        alpha = 255/(maxPxlValue-minPxlValue)
        
        # shifting factor
        beta = -min(minPxlValue * alpha, maxPxlValue * alpha)
        normalizedImg = np.float32(rangeImg) * alpha + beta
        normalizedImg = np.uint8(normalizedImg)
        im_color = cv2.applyColorMap(normalizedImg, cv2.COLORMAP_BONE)
        cv2.imwrite(filePath, im_color)

def moveColorImgsToAnotherFolder(sourceFolder, targetFolder):
    for fileName in os.listdir(sourceFolder):        
        filePath = os.path.join(sourceFolder, fileName)
        img = cv2.imread(filePath)

        if len(img.shape) == 3:
            shutil.move(filePath, targetFolder)


# new function to calculate the pixel value, 40% near 0, then throw away.
def findPossibleValidRangeFiles(sourceFolder, targetFolder):
    for fileName in os.listdir(sourceFolder):        
        filePath = os.path.join(sourceFolder, fileName)
        img = cv2.imread(filePath)
        if img.shape[0] == 1:
            continue
        else:
            shutil.move(filePath, targetFolder)
        # np.reshape(img, -1)


# sourceFolder = './nlr_imgs_small/'
# targetFolder = './ranges/'
# moveFilesToAnotherFolderAccordingToName(sourceFolder, targetFolder, 'range')

# sourceFolder = './ranges/'
# targetFolder = './ranges/'
# normalizeRangeFiles(sourceFolder, targetFolder)

# sourceFolder = './ranges/'
# targetFolder = './processed/'
# moveColorImgsToAnotherFolder(sourceFolder, targetFolder)

sourceFolder = './processed/'
targetFolder = './rectangleImgs/'
findPossibleValidRangeFiles(sourceFolder, targetFolder)
