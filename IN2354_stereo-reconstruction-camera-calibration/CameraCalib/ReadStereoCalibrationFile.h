#pragma once
#ifndef READSTEREOCALIBRATIONFILE_H
#define READSTEREOCALIBRATIONFILE_H

#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/calib3d/calib3d.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace cv;

/*
Read from the .yaml file, which generated from stereo calibration library 'Kalibr'
*/
void ReadStereoCalibrationFile(const std::string& stereo_file, Mat& cam0_dist, Mat& cam0_intrinsics, Mat& cam1_dist,
	Mat& cam1_intrinsics, Mat& rotation01, Mat& translation01, Mat& image_size)
{
	/*
	const std::string& stereo_file, std::vector<Mat>& cam0_dist, std::vector<Mat>& cam0_intrinsics,
		std::vector<Mat>& cam1_dist, std::vector<Mat>& cam1_intrinsics, std::vector<Mat>& rotation01, std::vector<Mat>& translation01,
		std::vector<int>& image_size
		*/
	std::string filename = stereo_file;

	FileStorage fs;
	if (!filename.empty())
	{
		fs.open(filename, FileStorage::READ);
	}

	if (!fs.isOpened())
	{
		printf("Failed to open file %s\n", filename.c_str());
	}

	FileNode cam0_node = fs["cam0"];
	FileNodeIterator it_dist0 = cam0_node["distortion_coeffs"].begin();
	for (int k = 0; k < 4; k++, ++it_dist0)
		cam0_dist |= ((int)*it_dist0) << k;
	std::cout << cam0_dist << std::endl;

	FileNodeIterator it_intrin0 = cam0_node["intrinsics"].begin();
	for (int k = 0; k < 4; k++, ++it_intrin0)
		cam0_intrinsics |= ((int)*it_intrin0) << k;
	std::cout << cam0_intrinsics << std::endl;

	FileNode cam1_node = fs["cam1"];
	cam1_node["distortion_coeffs"] >> cam1_dist;
	cam1_node["intrinsics"] >> cam1_intrinsics;
	cam1_node["resolution"] >> image_size;

	cam1_node["T_cn_cnm1"] >> rotation01;
	cam1_node["T_cn_cnm1"] >> translation01;

	//-----------------------------------------------------------Use yaml-cpp to load---------------------------------------------------------//
	/*
	// load .yaml
	YAML::Node baseNode = YAML::LoadFile(filename);
	std::cout << "Reading .yaml file" << std::endl;

	YAML::Node cam0_node = baseNode["cam0"];
	cam0_dist = cam0_node["distortion_coeffs"].as<std::vector<Mat>>();
	cam0_intrinsics = cam0_node["intrinsics"].as<std::vector<Mat>>();

	YAML::Node cam1_node = baseNode["cam1"];
	cam1_dist = cam1_node["distortion_coeffs"].as<std::vector<Mat>>();
	cam1_intrinsics = cam1_node["intrinsics"].as<std::vector<Mat>>();
	image_size = cam1_node["resolution"].as<std::vector<int>>();

	rotation01 = cam1_node["T_cn_cnm1"].as<std::vector<Mat>>();
	translation01 = cam1_node["T_cn_cnm1"].as<std::vector<Mat>>();
	*/

	fs.release();
}

#endif // READSTEREOCALIBRATIONFILE_H
