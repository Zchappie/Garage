import numpy as np 
import cv2
import os
import shutil
import csv

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
    counterZero = 0
    for fileName in os.listdir(sourceFolder):
        counter += 1        
        filePath = os.path.join(sourceFolder, fileName)
        rangeImg = cv2.imread(filePath)
        
        # scaling factor
        maxPxlValue = rangeImg.max()
        minPxlValue = rangeImg.min()
        if maxPxlValue == minPxlValue:
            counterZero += 1
            print("Dividing zero here at ", counter, "-th image, we ignored it, your majesty.")
            # shutil.move(filePath, './ranges_without_process/')
            continue
        alpha = 255/(maxPxlValue-minPxlValue)
        
        # shifting factor
        beta = -min(minPxlValue * alpha, maxPxlValue * alpha)
        normalizedImg = np.float32(rangeImg) * alpha + beta
        normalizedImg = np.uint8(normalizedImg)
        im_color = cv2.applyColorMap(normalizedImg, cv2.COLORMAP_BONE)
        cv2.imwrite(os.path.join(targetFolder, fileName), im_color)
    print("In total, we have ", counterZero, " files which are purely black, your majesty.")

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


# dig out more information from small ranges
def countSmallRangeFilesInfo(sourceFolder):
    f = open('/home/mengl/Downloads/small_ranges_info.csv', 'w')

    with f:
        writer = csv.writer(f)
        writer.writerow(['fileName', 'firstDim', 'secondDim', 'thirdDim', 'minPxlValue', 'maxPxlValue'])
        # rows = []

        for fileName in os.listdir(sourceFolder):   
            row = [fileName, 'nan', 'nan', 'nan', 'nan', 'nan']     
            filePath = os.path.join(sourceFolder, fileName)
            img = cv2.imread(filePath)
            try:
                row[1], row[2], row[3] = img.shape
                (row[4], row[5], _, _) = cv2.minMaxLoc(img)
            except:
                pass
            writer.writerow(row.copy())

        # for row in nms:
        #     writer.writerow(row)


# sourceFolder = './nlr_imgs_small/'
# targetFolder = './ranges/'
# moveFilesToAnotherFolderAccordingToName(sourceFolder, targetFolder, 'range')

# sourceFolder = './small_files/'
# targetFolder = './small_files/'
# normalizeRangeFiles(sourceFolder, targetFolder)

# sourceFolder = './ranges/'
# targetFolder = './processed/'
# moveColorImgsToAnotherFolder(sourceFolder, targetFolder)

# sourceFolder = './processed/'
# targetFolder = './rectangleImgs/'
# findPossibleValidRangeFiles(sourceFolder, targetFolder)

sourceFolder = './nlr_small_range/'
countSmallRangeFilesInfo(sourceFolder)
