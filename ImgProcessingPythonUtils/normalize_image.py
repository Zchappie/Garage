from tow_inspection_util import *

sourceFolder = '/Users/zeekile/Desktop/Infy/nlr_data/20200422_Morning_range/'
# sourceFolder = '/Users/zeekile/Downloads/'
# sourceFolder = '/Users/zeekile/Desktop/Infy/nlr_data/goodRange/'

for fileName in os.listdir(sourceFolder): 
    if fileName.endswith(".png"):
        print(fileName)
        filePath = os.path.join(sourceFolder, fileName)
        img = (cv2.imread(filePath, -1)).astype('int32')
        imgOriginalCopy = np.copy(img)
        imgFilled = np.copy(img)
        # printStatus(fileName, img)
        
        # fill the black holes
        for rowId in range(len(imgFilled)):
            imgFilled[rowId] = filterRow(imgFilled[rowId])
        
        # fit two selected profiles, and substract the frame with interpolation
        paramsTop = fitProfile(imgFilled[0])
        paramsMiddle = fitProfile(imgFilled[int(len(imgFilled)/2)])
        paramsBottom = fitProfile(imgFilled[-1])
        x = np.array(range(len(imgFilled[0])))
        for rowId in range(len(imgFilled)):
            if rowId <= int(len(imgFilled)/2):
                wBottom = rowId / int(len(imgFilled)/2)
                wTop = 1 - wBottom
                [a,b,c] = interpolationRows(paramsTop, paramsMiddle, wTop, wBottom)
                imgFilled[rowId] = imgFilled[rowId] - (np.square(x)*a + x*b + c)
            else:
                wBottom = (rowId - int(len(imgFilled)/2)) / (len(imgFilled) - int(len(imgFilled)/2))
                wTop = 1 - wBottom
                [a,b,c] = interpolationRows(paramsMiddle, paramsBottom, wTop, wBottom)
                imgFilled[rowId] = imgFilled[rowId] - (np.square(x)*a + x*b + c)
        minVal = np.amin(imgFilled) 
        imgFilled = imgFilled - minVal
        
        # prune some pure black images
        if ((imgFilled[np.nonzero(imgFilled)]).shape)[0] == 0:
            continue
        minval = np.min(imgFilled[np.nonzero(imgFilled)])
        normalized = (((imgFilled - minval)/(np.max(imgFilled) - minval)) * 255).astype('int')
        
        try:
            saveImg(fileName, '/Volumes/ZEEKANDISK/cv2write/normalized/20200422_Morning_range/', normalized)
        except:
            print("[0]Unexpected error from file:", fileName, sys.exc_info()[0])
            raise
        
        try:
            normalized = np.uint8(normalized)
            im_color = cv2.applyColorMap(normalized, cv2.COLORMAP_BONE)
            cv2.imwrite('/Volumes/ZEEKANDISK/cv2write/colored/20200422_Morning_range/'+fileName, im_color)
        except:
            print("[1]Unexpected error from file:", fileName, sys.exc_info()[0])
            raise

#     break