#pragma once
#ifndef CAMERA_H
#define CAMERA_H

#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/calib3d/calib3d.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace cv;
/*
VideoCapture& cap, API, to get new frame
Mat& rectified0, output rectified frame 0
Mat& rectified1, output rectified frame 1
Mat& map_left1, input map of cam0 before convert
Mat& map_left2, input map of cam0 after convert
Mat& map_right1, input map of cam1 before convert
Mat& map_right2, input map of cam1 after convert
*/
void camera(VideoCapture& cap, Mat& rectified0, Mat& rectified1, Mat& map_left1, Mat& map_left2, Mat& map_right1, Mat& map_right2)
{
	Mat frame, grayscale;

	cap >> frame;

	cvtColor(frame, grayscale, CV_RGB2GRAY); // convert to gray image

	Mat left_gray = grayscale(Rect(0, 0, 640, 480)); //separate left and right eye from single frame of stereo
	Mat right_gray = grayscale(Rect(640, 0, 640, 480));

	remap(left_gray, rectified0, map_left1, map_left2, INTER_LINEAR);
	remap(right_gray, rectified1, map_right1, map_right2, INTER_LINEAR);
}

#endif