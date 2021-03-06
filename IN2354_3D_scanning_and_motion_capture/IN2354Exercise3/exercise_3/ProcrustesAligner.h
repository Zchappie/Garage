#pragma once
#include "SimpleMesh.h"

class ProcrustesAligner {
public:
	Matrix4f estimatePose(const std::vector<Vector3f>& sourcePoints, const std::vector<Vector3f>& targetPoints) {
		ASSERT(sourcePoints.size() == targetPoints.size() && "The number of source and target points should be the same, since every source point is matched with corresponding target point.");

		// We estimate the pose between source and target points using Procrustes algorithm.
		// Our shapes have the same scale, therefore we don't estimate scale. We estimated rotation and translation
		// from source points to target points.

		auto sourceMean = computeMean(sourcePoints);
		auto targetMean = computeMean(targetPoints);

		Matrix3f rotation = estimateRotation(sourcePoints, sourceMean, targetPoints, targetMean);
		Vector3f translation = computeTranslation(sourceMean, targetMean);

		// To apply the pose to point x on shape X in the case of Procrustes, we execute:
		// 1. Translation of a point to the shape Y: x' = x + t
		// 2. Rotation of the point around the mean of shape Y: 
		//    y = R (x' - yMean) + yMean = R (x + t - yMean) + yMean = R x + (R t - R yMean + yMean)

		Matrix4f estimatedPose = Matrix4f::Identity();
		estimatedPose.block(0, 0, 3, 3) = rotation;
		estimatedPose.block(0, 3, 3, 1) = rotation * translation - rotation * targetMean + targetMean;

		return estimatedPose;
	}

private:
	Vector3f computeMean(const std::vector<Vector3f>& points) {
		// TODO: Compute the mean of input points.
		Vector3f mean = Vector3f::Zero();
		for (int i = 0; i < points.size(); i++) {
			mean += points[i];
		}
		return mean/points.size();
	}

	Matrix3f estimateRotation(const std::vector<Vector3f>& sourcePoints, const Vector3f& sourceMean, const std::vector<Vector3f>& targetPoints, const Vector3f& targetMean) {
		// TODO: Estimate the rotation from source to target points, following the Procrustes algorithm.
		// To compute the singular value decomposition you can use JacobiSVD() from Eigen.
		// Important: The covariance matrices should contain mean-centered source/target points.

		MatrixXf x_prime = MatrixXf::Identity(sourcePoints.size(), 3);
		MatrixXf x = MatrixXf::Identity(targetPoints.size(), 3);

		Vector3f mean_diff = targetMean - sourceMean;

		for (int i = 0; i < sourcePoints.size(); i++) {
			Vector3f translated_source_point = sourcePoints[i] - targetMean;
			Vector3f target_point = targetPoints[i] - targetMean;

			x_prime(i, 0) = translated_source_point.x();
			x_prime(i, 1) = translated_source_point.y();
			x_prime(i, 2) = translated_source_point.z();

			x(i, 0) = target_point.x();
			x(i, 1) = target_point.y();
			x(i, 2) = target_point.z();
		}

		MatrixXf cross_covariance_matrix = x.transpose() * x_prime;

		JacobiSVD<MatrixXf> svd(cross_covariance_matrix, ComputeThinU | ComputeThinV);
		
		Matrix3f rotationMatrix = svd.matrixU()*svd.matrixV().transpose();
		
		return rotationMatrix;
	}

	Vector3f computeTranslation(const Vector3f& sourceMean, const Vector3f& targetMean) {
		// TODO: Compute the translation vector from source to target points.
		return targetMean - sourceMean;
	}
};