#include <iostream>
#include <sstream>
#include <stdio.h>

//#include <yaml-cpp/yaml.h>

#include "camera.h"
#include "ReadStereoCalibrationFile.h"

void camera(VideoCapture&, Mat&, Mat&, Mat&, Mat&, Mat&, Mat&);
void ReadStereoCalibrationFile(const std::string&, Mat&, Mat&, Mat&, Mat&, Mat&, Mat&, Mat&); 


int main(int argc, char** argv)
{
	//-----------------------------------------------------------Get params from .yaml-----------------------------------------------------//
	
	//######## IMPORTANT!!! always use the absolute path to refer the file, not the file name!
	std::string stereo_file = "CameraCalib\\camchain.yaml";

	Mat cam0_dist = Mat_<double>::zeros(4, 1);
	Mat cam0_intrinsics = Mat_<double>::zeros(4, 1);
	Mat cam1_dist = Mat_<double>::zeros(4, 1);
	Mat cam1_intrinsics = Mat_<double>::zeros(4, 1);
	Mat rotation01 = Mat_<double>::zeros(4, 4);
	Mat translation01 = Mat_<double>::zeros(4, 4);
	Mat image_size = Mat_<double>::zeros(2, 1);;
	/*
	std::vector<Mat> cam0_dist; 
	std::vector<Mat> cam0_intrinsics;
	std::vector<Mat> cam1_dist; 
	std::vector<Mat> cam1_intrinsics; 
	std::vector<Mat> rotation01; 
	std::vector<Mat> translation01;
	std::vector<int> image_size;
	*/
	ReadStereoCalibrationFile(stereo_file, cam0_dist, cam0_intrinsics, cam1_dist, cam1_intrinsics, rotation01, translation01, image_size);
	std::cout << "Read .yaml file. Done!" << std::endl;
	
	
	//-----------------------------------------------------------Initialize camera---------------------------------------------------------//
	VideoCapture cap(2);

	// open the camera set; 2 is the stereo set on my laptop.
	if (!cap.isOpened())  // if not success, exit program
	{
		std::cout << "Cannot open the video cam" << std::endl;
		return -1;
	}

	// the intrinsics and distortion parameters of stereo pair
	Mat left_intrinsics = (Mat1d(3, 3) << 427.32814323885566, 0., 367.1148716890002, 0., 429.48081105226316, 242.03387791215218, 0., 0., 1.);
	Mat left_distCoeffs = (Mat1d(1, 4) << -0.35292630520315216, 0.09970701156068408, -0.0003265055193558261, -0.003400767380536901);
	Mat right_intrinsics = (Mat1d(3, 3) << 425.28226969376584, 0., 342.6156277602674, 0., 427.5013362691404, 233.38645927695092, 0., 0., 1.);
	Mat right_distCoeffs = (Mat1d(1, 4) << -0.34242635946786465, 0.09353275937137827, 0.000332922660566574, -0.001440982693394223);

	// rotation and transformation between two cameras, cam0 to cam1
	Mat R = (Mat1d(3, 3) << 0.9999842188801975, 0.0051761908815188395, -0.0021838128387943914,
							-0.005183031408333682, 0.9999816430410434, -0.0031384337416914382,
							0.002167527618515751, 0.0031497029842259693, 0.9999926905708509);
	Mat T = (Mat1d(3, 1) << -0.060400809282521006, 0.00020747637203608188, 3.97878900435667e-05);

	// initial the map
	Mat first_frame;
	cap >> first_frame;

	// separate the full image to left and right eye
	Mat left_first_frame = first_frame(Rect(0, 0, 640, 480));
	Mat right_first_frame = first_frame(Rect(640, 0, 640, 480));

	// get the image size of single eye
	Size image_size_0;
	image_size_0 = left_first_frame.size();

	// get rectified maps
	Mat R1, R2, P1, P2, Q;
	stereoRectify(left_intrinsics, left_distCoeffs, right_intrinsics, right_distCoeffs, image_size_0, R, T, R1, R2, P1, P2, Q);

	// cache the map
	Mat map_left1, map_left2, map_right1, map_right2;
	initUndistortRectifyMap(left_intrinsics, left_distCoeffs, R1, P1, image_size_0, CV_16SC2, map_left1, map_left2);
	initUndistortRectifyMap(right_intrinsics, right_distCoeffs, R2, P2, image_size_0, CV_16SC2, map_right1, map_right2);

	// send rectified maps to get rectified gray images
	Mat rectified0, rectified1;
	camera(cap, rectified0, rectified1, map_left1, map_left2, map_right1, map_right2);

	cap.release();
	//-----------------------------------------------------------TEST: count FPS--------------------------------------------------------------//
	/*
	// count the fps
	double fps = cap.get(CAP_PROP_FPS);
	std::cout << "FPS is " << fps << std::endl;
	int num_frames = 100;
	time_t start, end;
	std::cout << "capturing" << num_frames << "frame" << std::endl;

	Mat frame;
	Mat grayscale;
	Mat left_gray_out, right_gray_out;
	Rect left_region(0, 0, 640, 480);  // didn't change the speed
	Rect right_region(640, 0, 640, 480);

	time(&start);
	for (int i = 0; i < num_frames; i++)
	{
		
		cap >> frame;
		cvtColor(frame, grayscale, CV_RGB2GRAY);
		Mat left_gray = grayscale(left_region);
		Mat right_gray = grayscale(right_region);
		
		remap(left_gray, left_gray_out, map_left1, map_left2, INTER_LINEAR);
		remap(right_gray, right_gray_out, map_right1, map_right2, INTER_LINEAR);
		imshow("grayscale right eye undistorted", right_gray_out);
		imshow("grayscale left eye undistorted", left_gray_out);
		//around 12 fps
	}
	time(&end);
	double seconds = difftime(end, start);
	double fps_1 = num_frames / seconds;
	std::cout << "Estimated fps is " << fps_1 << std::endl;
	*/
	//cap.release();
	return 0;
}

// 640 x 480