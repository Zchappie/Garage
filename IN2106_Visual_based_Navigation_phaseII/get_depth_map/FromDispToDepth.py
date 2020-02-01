import os
import numpy as np
import cv2
import plyfile

dirpath = os.getcwd()
img_path = str(dirpath) + '/results/disparity_map_opencv/'

# --------------------------------------------------1.setup the params
# T_i_0 = np.array(
#     [
#         [0.0148655429818, -0.999880929698, 0.00414029679422, -0.0216401454975],
#         [0.999557249008, 0.0149672133247, 0.025715529948, -0.064676986768],
#         [-0.0257744366974, 0.00375618835797, 0.999660727178, 0.00981073058949],
#         [0.0, 0.0, 0.0, 1.0]
#     ]
# )
# T_i_1 = np.array(
#     [
#         [0.0125552670891, -0.999755099723, 0.0182237714554, -0.0198435579556],
#         [0.999598781151, 0.0130119051815, 0.0251588363115, 0.0453689425024],
#         [-0.0253898008918, 0.0179005838253, 0.999517347078, 0.00786212447038],
#         [0.0, 0.0, 0.0, 1.0]
#     ]
# )
# T_0_1 = np.linalg.inv(np.dot(np.linalg.inv(T_i_0), T_i_1))
# R = T_0_1[0:3:1, 0:3:1]
# T = T_0_1[0:3:1, 3:4:1].flatten()
npzfile = np.load('cams_params_new.npz')
# R1 = npzfile['newRotation0']  # rect rotation
# R2 = npzfile['newRotation1']  # rect rotation
# P1 = npzfile['cameraMatrix0'][0:3:1, 0:3:1]
# fx = P1[0][0]
# width = 752
# img_real_size = 4.51e-3
# focal_length = fx*img_real_size/width  # in m
# T_0_1 = npzfile('T_0_1')  # load transformation between eyes instead of calculating
# T_0_1_rect = np.dot(R1, np.dot(R, np.linalg.inv(R2)) + T)
# baseline = np.linalg.norm(np.dot(R1, T))

# --------------------------------------------------1.setup the params
# load the use-able camera ids
# f=open("../../data/euroc_V1/timestamps.txt", "r")
# if f.mode == 'r':
#     f1 = f.readlines()
#     cam_ids = []
#     for x in f1:
#         cam_ids += [int(x)]
# else:
#     print("Can't open file timestamps.txt")

proj_mat = npzfile['dispToDepth']   # Directly from opencv reprojection

# for every disparity map (expressed in left eye)
for imgid in os.listdir(img_path):
    imgid_num = int(imgid[0: -4])
    # if imgid_num in cam_ids:
    img = cv2.imread(img_path + imgid, -1)
    # ----------------------------------------Using reprojection Opencv
    img_3d = cv2.reprojectImageTo3D(
        disparity = img,
        Q = proj_mat
    )
    # points = []
    # for i in range(img_3d.shape[0]):
    #     for j in range(img_3d.shape[1]):
    #         if np.isinf(img_3d[i][j].any()):
    #             continue
    #         else:
    #             points.append("%f %f %f %d %d %d\n"%(img_3d[i][j][0],img_3d[i][j][1],img_3d[i][j][2], 255, 0, 0))
    #             file = open("ply_file.ply","w")
    #             file.write('''ply
    #             format ascii 1.0
    #             element vertex %d
    #             property float x
    #             property float y
    #             property float z
    #             property uchar red
    #             property uchar green
    #             property uchar blue
    #             end_header
    #             %s 
    #             '''%(len(points),"".join(points)))
    #             file.close()
                # break
    f= open(os.path.join('./results/depth_opencv', str(imgid_num) + ".txt"),"w+")
    for i in range(img_3d.shape[0]):
        for j in range(img_3d.shape[1]):
            if np.isinf(img_3d[i][j].any()):
                continue
            else:
                # TODO: project p3d to rect 0 get 
                f.write(str(img_3d[i][j][0]*16.0) + ',' + str(img_3d[i][j][1]*16.0) + ',' + str(img_3d[i][j][2]*16.0) + '\n')
    f.close()
        # ----------------------------------------Using reprojection Opencv

        # ----------------------------------------Manually calculate depth
        # use the rect baseline, depth = baseline * focal_length/img
        # f= open(os.path.join('./results/depth_opencv', str(imgid_num) + ".txt"),"w+")
        # for i in range(img.shape[0]):
        #     for j in range(img.shape[1]):
        #         if img[i][j] == 0:
        #             continue
        #         else:
        #             # print(baseline)
        #             depth = baseline * 1/6e-6 * focal_length/img[i][j]
        #             x_y = np.dot(np.linalg.inv(P1), np.transpose(np.array([i, j, 1])))
        #             f.write(str(x_y[0]*depth) + ',' + str(x_y[1]*depth) + ',' + str(depth) + '\n')
        # f.close()
        # ----------------------------------------Manually calculate depth

        # ----------------------------------------Use point cloud library


        # ----------------------------------------Use point cloud library
        # break
    # else:
    #     continue
    # break