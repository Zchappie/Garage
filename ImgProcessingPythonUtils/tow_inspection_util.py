import numpy as np
import cv2
import os
import sys
from PIL import Image
# import png
from matplotlib import pyplot as plt
import matplotlib.lines as mlines
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter

def plotImage(img, edges = None):
    # plot the image with edges or only image
    if not edges:
        fig=plt.figure(figsize=(18, 16), dpi= 80, facecolor='w', edgecolor='k')
        plt.gray()
        plt.imshow(img)
    else:
        fig=plt.figure(figsize=(18, 16), dpi= 80, facecolor='w', edgecolor='k')
        plt.gray()
        plt.imshow(img)
        # plt.plot()
        # l = mlines.Line2D([xmin,xmax], [ymin,ymax])

def plotProfile(profile):
    fig=plt.figure(figsize=(18, 16), dpi= 80, facecolor='w', edgecolor='k')
    plt.plot(range(len(profile)), profile)

def smooth(x, window_len=11, window='hanning'):
    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y

def removeCloseGrad(gradients):
    # after thresholding the gradient of the profile, same large edge may create some consecutive large gradients
    nonConsecutiveEdges = [gradients[0]]
    counter = 1
    for gradient in gradients:
        if gradient - nonConsecutiveEdges[-1] == 0:
            pass
        elif gradient - nonConsecutiveEdges[-1] == counter:
            counter += 1
        else:
            nonConsecutiveEdges.append(gradient)
            counter = 1
    # the first one is fake edge created by color filling
    return nonConsecutiveEdges[1:]

def filterAccordingToWidth(gradients):
    # WARNING!!
    # this is a cheating trick, manually measured the tow width -> around 140 pxls
    towWidth = 140
    tows = [gradients[0]]
    for gradient in gradients:
        if (gradient - tows[0])%towWidth < 20 or (gradient - tows[0])%towWidth > 120:
            tows.append(gradient)
    return tows[1:]

# find consecutive zeros
def zero_runs(a):
    # Create an array that is 1 where a is 0, and pad each end with an extra 0.
    iszero = np.concatenate(([0], np.equal(a, 0).view(np.int8), [0]))
    absdiff = np.abs(np.diff(iszero))
    # Runs start and end where absdiff is 1.
    ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
    return ranges

# processing steps from Profactor, first interpolate the black dots
def filterRow(row):
    zeroRanges = zero_runs(row)
    if zeroRanges.size != 0:
        for zeroRange in zeroRanges:
            if zeroRange[0] == 0 and zeroRange[1] != len(row):
                row[zeroRange[0] : zeroRange[1]].fill(row[zeroRange[1]])
            elif zeroRange[0] != 0 and zeroRange[1] == len(row):
                row[zeroRange[0] : zeroRange[1]].fill(row[zeroRange[0]-1])
            elif zeroRange[0] != 0 and zeroRange[1] != len(row):
                x = [zeroRange[0] - 1, zeroRange[1]]
                y = [row[zeroRange[0] - 1], row[zeroRange[1]]]
                row[zeroRange[0] : zeroRange[1]] = np.interp(range(zeroRange[0], zeroRange[1]), x, y)
    else:
        return row
    return row

def printStatus(fileName, img):
    # print('The file name is', fileName, \
    #          '\nThe image size', img.shape, \
    #          '\nThe whole image mean value:', np.mean(img), \
    #          '\nThe maximum value:', np.amax(img), \
    #          '\nThe minimum value:', np.amin(img), \
    #          '\n\nThe image left part, mean value:', np.mean(img[:, :1000]), \
    #          '\nThe image left part, max value:', np.amax(img[:, :1000]), \
    #          '\nThe image left part, min value:', np.amin(img[:, :1000]), \
    #          '\n\nThe image right part, mean value:', np.mean(img[:, 1000:]), \
    #          '\nThe image right part, max value:', np.amax(img[:, 1000:]), \
    #          '\nThe image right part, min value:', np.amin(img[:, 1000:]), \
    #          '\n-------------------------------------------------------\n')
    print('The file name is', fileName, \
             '\nThe image size', img.shape, \
             '\nThe whole image mean value:', np.mean(img), \
             '\nThe maximum value:', np.amax(img), \
             '\nThe minimum value:', np.amin(img), \
             '\n-------------------------------------------------------\n')

def normalizeImg(img):
    """
    Normalize the image to [0, 255], may not be necessary
    """
    normalizedImg = img - np.amin(img)
    normalizedImg = np.multiply((255.0/normalizedImg.max()), normalizedImg)
    normalizedImg = normalizedImg.astype(int)
    return normalizedImg

def saveImg(fileName, targetDir, img):
    nameDir = targetDir + fileName
    
    # Use pypng to write img as a grayscale PNG.
    # with open(nameDir, 'wb') as f:
    #     writer = png.Writer(width=img.shape[1], height=img.shape[0], bitdepth=16, greyscale=True)
    #     gray2list = img.tolist()
    #     writer.write(f, gray2list)
        
    cv2.imwrite(nameDir, img)

def fitProfileAndPlot(profile):
    # define a function to be fitted
    def func(x, a, b, c):
        return np.square(x)*a + x*b + c 
    
    # plot the fitted function on the profile
    plotProfile(profile)
    popt, pcov = curve_fit(func, range(len(profile)), profile)
    plt.plot(range(len(profile)), func(range(len(profile)), *popt), \
             'g--', label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))

def fitProfileAndNormalize(profile):
    # define a function to be fitted
    def func(x, a, b, c):
        return np.square(x)*a + x*b + c 
    
    # normalize the profile and avoid negative value
    popt, pcov = curve_fit(func, range(len(profile)), profile)
    [a, b, c] = popt
    minVal = np.amin(profile - func(range(len(profile)), a, b, c)) 
    return profile - func(range(len(profile)), a, b, c) - minVal

def fitProfile(profile):
    # define a function to be fitted
    def func(x, a, b, c):
        return np.square(x)*a + x*b + c 
    
    # normalize the profile and avoid negative value
    popt, pcov = curve_fit(func, range(len(profile)), profile)
    return popt

def interpolationRows(paramsTop, paramsBottom, wTop, wBottom):
    """
    Interpolation of two fixed fitting curves to get a fitting curve at any row in a frame.
    Return the interpolated parameters of a curve.
    """
    return paramsTop*wTop + paramsBottom*wBottom

def colorNormalize(img):
    # scaling factor
    maxPxlValue = img.max()
    minPxlValue = img.min()
    if maxPxlValue == minPxlValue:
        return None
    
    alpha = 255/(maxPxlValue-minPxlValue)

    # shifting factor
    beta = -min(minPxlValue * alpha, maxPxlValue * alpha)
    normalizedImg = np.float32(img) * alpha + beta
    normalizedImg = np.uint8(normalizedImg)
    im_color = cv2.applyColorMap(normalizedImg, cv2.COLORMAP_BONE)
    return im_color