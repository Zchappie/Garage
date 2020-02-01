import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image
import os

# input stored map, compute the disparity map of current image
def computeDispMap(imgL, imgR, map0x, map0y, map1x, map1y, stereo, imgId):
    img1_rect = cv2.remap(imgL, map0x, map0y, cv2.INTER_LINEAR)
    img2_rect = cv2.remap(imgR, map1x, map1y, cv2.INTER_LINEAR)

    disp0 = stereo.compute(img1_rect,img2_rect)/16.0
    disp1 = stereo.compute(img2_rect,img1_rect)/16.0
    # cv2.imwrite(os.path.join('./results/rect_0/', imgId), img1_rect)
    # cv2.imwrite(os.path.join('./results/rect_1/', imgId), img2_rect)
    # cv2.imwrite(os.path.join('./results/disparity_map_opencv_0', imgId), disparity)
    return disp0, disp1

#-----------------------------------------do rectify here
cameraMatrix0 = np.array(
    [
        [461.1581901632606, 0, 365.8972386901175],
        [0, 459.80802859479726, 249.35492318319005],
        [0, 0, 1.0]
    ]
)

cameraMatrix1 = np.array(
    [
        [459.7448068651981, 0, 379.36396149546416],
        [0, 458.35350534633889, 256.0435254270624],
        [0, 0, 1.0]
    ]
)

# ground truth coeffs
distCoeff0 = np.array([-0.28340811, 0.07395907, 0.00019359, 1.76187114e-05])
distCoeff1 = np.array([-0.28368365,  0.07451284, -0.00010473, -3.55590700e-05])

# this is not for pin-hole camera, need to check the conversion
# distCoeff0 = np.array([-0.004593052532205668, 0.027532432037029668, -0.03697767177099984, 0.01861021724557011])
# distCoeff1 = np.array([0.004549588612679905,  0.002485490491605769, -0.010601348784725634, 0.01078104114089161])

T_i_0 = np.array(
    [
        [0.0148655429818, -0.999880929698, 0.00414029679422, -0.0216401454975],
        [0.999557249008, 0.0149672133247, 0.025715529948, -0.064676986768],
        [-0.0257744366974, 0.00375618835797, 0.999660727178, 0.00981073058949],
        [0.0, 0.0, 0.0, 1.0]
    ]
)
T_i_1 = np.array(
    [
        [0.0125552670891, -0.999755099723, 0.0182237714554, -0.0198435579556],
        [0.999598781151, 0.0130119051815, 0.0251588363115, 0.0453689425024],
        [-0.0253898008918, 0.0179005838253, 0.999517347078, 0.00786212447038],
        [0.0, 0.0, 0.0, 1.0]
    ]
)
T_0_1 = np.linalg.inv(np.dot(np.linalg.inv(T_i_0), T_i_1))
# print(T_0_1)
R = T_0_1[0:3:1, 0:3:1]
T = T_0_1[0:3:1, 3:4:1].flatten()
# print(R, T)

R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(
    cameraMatrix1=cameraMatrix0,
    distCoeffs1=distCoeff0,
    cameraMatrix2=cameraMatrix1,
    distCoeffs2=distCoeff1,
    imageSize=(752, 480),
    R=R,
    T=T#, alpha = 1
    )

np.savez('cams_params_new', 
            cameraMatrix0 = P1, 
            distCoeff0 = distCoeff0, 
            newRotation0 = R1, 
            newRotation1 = R2,
            cameraMatrix1 = P2, 
            distCoeff1 = distCoeff1,
            c = R2,
            dispToDepth = Q,
            T_0_1 = T_0_1)

map0x, map0y = cv2.initUndistortRectifyMap(
    cameraMatrix=cameraMatrix0,
    distCoeffs=distCoeff0,
    R=R1,
    newCameraMatrix=P1,
    size=(752, 480),
    m1type=cv2.CV_16SC2)

map1x, map1y = cv2.initUndistortRectifyMap(
    cameraMatrix=cameraMatrix1,
    distCoeffs=distCoeff1,
    R=R2,
    newCameraMatrix=P2,
    size=(752, 480),
    m1type=cv2.CV_16SC2)

stereo = cv2.StereoSGBM_create(
        numDisparities=64,  blockSize=3, 
        minDisparity = 0,
        # SADWindowSize = 11,
        P1 = 120,
        P2 = 240,
        disp12MaxDiff = -1,
        preFilterCap = 31,
        uniquenessRatio = 0,
        speckleWindowSize = 500,
        speckleRange = 3
        )

# create right and left matcher for disparity map post-processing
left_matcher = stereo
right_matcher = cv2.ximgproc.createRightMatcher(left_matcher)

# FILTER Parameters
lmbda = 80000
sigma = 1.2
visual_multiplier = 1.0
 
wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=left_matcher)
wls_filter.setLambda(lmbda)
wls_filter.setSigmaColor(sigma)

#-----------------------------------------begin
img_path_0 = '../../data/V1_01_easy/mav0/cam0/data/'
img_path_1 = '../../data/V1_01_easy/mav0/cam1/data/'

# for loop will start from here, for every images
for imgid in os.listdir(img_path_0):
    imgL = cv2.imread(img_path_0 + imgid, -1)
    imgR = cv2.imread(img_path_1 + imgid, -1)
    disp0, disp1 = computeDispMap(imgL,imgR, map0x, map0y, map1x, map1y, left_matcher, imgid)
    disp0 = np.int16(disp0)
    disp1 = np.int16(disp1)
    filteredImg = wls_filter.filter(disp0, imgL, None, disp0)
    filteredImg = cv2.normalize(src=filteredImg, dst=filteredImg, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX)
    filteredImg = np.uint8(filteredImg)
    cv2.imwrite(os.path.join('./results/disparity_map_opencv', imgid), filteredImg)
    break