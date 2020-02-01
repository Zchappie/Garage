# get ground truth disparity map from data

import cv2
from plyfile import PlyData, PlyElement
import csv
import numpy as np
from scipy.spatial.transform import Rotation as R
import os

# ----------------------------------------------------------- Load camera poses (necessary 164), convert to 4*4 matrix
# load the use-able camera ids
f=open("../../data/euroc_V1/timestamps.txt", "r")
if f.mode == 'r':
    f1 = f.readlines()
    cam_ids = []
    for x in f1:
        cam_ids += [int(x)]
else:
    print("Can't open file timestamps.txt")

# load ground truth camera poses
csv_path = '../../data/V1_01_easy/mav0/state_groundtruth_estimate0/data.csv'
cam_poses = []
with open(csv_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    row_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            if int(row[0]) in cam_ids:
                cam_poses += [row[:8]] # whole list are strings
            line_count += 1
    # print(f'Processed {line_count} lines.')  # 28713
    print(cam_poses) # only have 59 out of 82 poses

# load camera matrix (rectified)
npzfile = np.load('cams_params_new.npz')
cam0_matrix = npzfile['cameraMatrix0']
distCoeff0 = npzfile['distCoeff0'] 

# marker to base
T_B_S = np.array(
    [
        [ 0.33638, -0.01749,  0.94156,  0.06901],
        [-0.02078, -0.99972, -0.01114, -0.02781],
        [ 0.94150, -0.01582, -0.33665, -0.12395],
        [     0.0,      0.0,      0.0,      1.0]
    ]
)

# cam0 to base
T_B_0 = np.array(
    [
        [0.0148655429818, -0.999880929698, 0.00414029679422, -0.0216401454975],
        [0.999557249008, 0.0149672133247, 0.025715529948, -0.064676986768],
        [-0.0257744366974, 0.00375618835797, 0.999660727178, 0.00981073058949],
        [0.0, 0.0, 0.0, 1.0]
    ]
)

# convert the quaternion to tranformation matrix
cam_poses_mat = np.empty((0, 4, 4))
for pose in cam_poses:
    pose[1:] = [float(x) for x in pose[1:]]
    t = np.array(pose[1:4])
    r_quaternion = pose[4:]
    qw = r_quaternion[0]
    r_quaternion[0:3] = r_quaternion[1:4]
    r_quaternion[-1] = qw
    r = R.from_quat(r_quaternion).as_dcm() # the params order is changed
    cam_pose = np.dot(np.vstack((np.hstack((r, t[:, None])), [0, 0, 0 ,1])), np.linalg.inv(T_B_0)) # base to cam0
    # cam_pose = np.vstack((np.hstack((r, t[:, None])), [0, 0, 0 ,1]))
    cam_poses_mat = np.append(cam_poses_mat, [cam_pose], axis=0)
print(cam_poses_mat)
# -----------------------------------------------------------

# ----------------------------------------------------------- Load point cloud
pcl_path = '../../data/V1_01_easy/mav0/pointcloud0/data.ply'
plydata = PlyData.read(pcl_path)  
ply_elements = plydata.elements  # totally 7 properties, xyz,i,rgb
vertice_num = len(plydata.elements[0].data['x'])
# -----------------------------------------------------------

# for every camera poses, find the point cloud expressed in current frame
def projectToImg(cam_mat, distCoeffs, p3d):
    """
    INPUTS:
    cam_mat, (3,3), camera matrix (rectified)
    distCoeffs, (1,4), radial-tangential distortion coefficients
    p3d, (1,3), expressed in camera frame

    OUTPUTS:
    p2d, (1,2) pixel coordinates
    """
    x_prime = p3d[0]/p3d[2]
    y_prime = p3d[1]/p3d[2]
    # r_2 = x_prime*x_prime + y_prime*y_prime
    # x_pp = x_prime*(1 + distCoeffs[0]*r_2 + distCoeffs[1]*r_2*r_2) + 2*distCoeffs[2]*x_prime*y_prime + distCoeffs[3]*(r_2 + 2*x_prime*x_prime)
    # y_pp = y_prime*(1 + distCoeffs[0]*r_2 + distCoeffs[1]*r_2*r_2) + 2*distCoeffs[3]*x_prime*y_prime + distCoeffs[2]*(r_2 + 2*y_prime*y_prime)
    u = int(round(cam_mat[0][0]*x_prime + cam_mat[0][2]))
    v = int(round(cam_mat[1][1]*y_prime + cam_mat[1][2]))
    p2d = [v, u]
    return p2d

# p3d_world_homo = np.array([-2.91190004, -3.40980005,  0.45410001,  1.        ])
# p3d_cam0_homo = np.dot(cam_poses_mat[0], p3d_world_homo)
# p2d_cam0, _ = cv2.projectPoints(p3d_cam0_homo[:3], np.zeros((3,3)), np.zeros((1,3)), cam0_matrix[0:3:1, 0:3:1], distCoeff0)
# p2d_cam0 = projectToImg(cam0_matrix[0:3:1, 0:3:1], distCoeff0, p3d_cam0_homo)
# print(p2d_cam0)

npzfile = np.load('cams_params_new.npz')
R1 = npzfile['newRotation0']  # rect rotation
R2 = npzfile['newRotation1']  # rect rotation
P1 = npzfile['cameraMatrix0'][0:3:1, 0:3:1]
T_0_1 = npzfile['T_0_1']
R = T_0_1[0:3:1, 0:3:1]
T = T_0_1[0:3:1, 3:4:1].flatten()
fx = P1[0][0]
width = 752
img_real_size = 4.51e-3
focal_length = fx*img_real_size/width  # in m
# T_0_1_rect = np.dot(R1, np.dot(R, np.linalg.inv(R2)) + T)
# baseline = np.linalg.norm(np.dot(R1, T)) # in m
baseline = np.linalg.norm(T)  # in m
t = np.transpose(np.array([0,0,0]))
addtional_T = np.vstack((np.hstack((R1, t[:, None])), [0, 0, 0 ,1]))

for i in range(len(cam_poses_mat)):
    img = np.zeros((480, 752))  # initialize the disp map for groud truth
    img0 = np.zeros((480, 752))  # initialize the projected img for cam0
    img1 = np.zeros((480, 752))  # initialize the projected img for cam1
    for vertex in plydata.elements[0].data:
        p3d_world_homo = np.array(list(vertex)[:3] + [1])
        p3d_cam0_homo = np.dot(addtional_T, np.dot(np.linalg.inv(cam_poses_mat[i]), p3d_world_homo))  # world to cam0, cam0 to rectified cam0
        p2d_cam0 = projectToImg(cam0_matrix[0:3:1, 0:3:1], distCoeff0, p3d_cam0_homo)

        # p3d_cam1_homo = np.dot(addtional_T, np.dot(cam_poses_mat[i], p3d_world_homo))  # world to cam1, cam1 to rectified cam0
        if p2d_cam0[0] < 480 and p2d_cam0[0] >=0 and p2d_cam0[1] <752 and p2d_cam0[1] >=0:
            # img[p2d_cam0[0]][p2d_cam0[1]] = p3d_cam0_homo[2]  # store the depth value of current pixel
            # TODO: transform the point cloud to disparity map
            print(p2d_cam0)
            disparity_value = (baseline * 1/6e-6 * focal_length) / p3d_cam0_homo[2]
            img[p2d_cam0[0]][p2d_cam0[1]] = disparity_value
            # img0[p2d_cam0[0]][p2d_cam0[1]] = vertex[3]
    
    cv2.imwrite(os.path.join('./results/disparity_map_gt', cam_poses[i][0] + '.png'), img)
    # cv2.imwrite(os.path.join('./results/rect_0_gt', cam_poses[i][0] + '.png'), img0)
    # break
    
# TODO: Load ours disparity map 