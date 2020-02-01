/**
BSD 3-Clause License

Copyright (c) 2018, Vladyslav Usenko and Nikolaus Demmel.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

#pragma once

#include <bitset>
#include <set>

#include <Eigen/Dense>
#include <sophus/se3.hpp>

#include <opengv/relative_pose/CentralRelativeAdapter.hpp>
#include <opengv/relative_pose/methods.hpp>
#include <opengv/sac/Ransac.hpp>
#include <opengv/sac_problems/relative_pose/CentralRelativePoseSacProblem.hpp>

#include <visnav/camera_models.h>
#include <visnav/common_types.h>

namespace visnav {

void computeEssential(const Sophus::SE3d& T_0_1, Eigen::Matrix3d& E) {
  const Eigen::Vector3d t_0_1 = T_0_1.translation();
  const Eigen::Matrix3d R_0_1 = T_0_1.rotationMatrix();

  // TODO SHEET 3: compute essential matrix
  Eigen::Matrix3d t_h;
  Eigen::Vector3d t;
  t = t_0_1.normalized();
  t_h << 0, -t(2), t(1), t(2), 0, -t(0), -t(1), t(0), 0;
  E = t_h * R_0_1;
  // E = R_0_1.transpose() * t_h;
}

void findInliersEssential(const KeypointsData& kd1, const KeypointsData& kd2,
                          const std::shared_ptr<AbstractCamera<double>>& cam1,
                          const std::shared_ptr<AbstractCamera<double>>& cam2,
                          const Eigen::Matrix3d& E,
                          double epipolar_error_threshold, MatchData& md) {
  md.inliers.clear();

  for (size_t j = 0; j < md.matches.size(); j++) {
    const Eigen::Vector2d p0_2d = kd1.corners[md.matches[j].first];
    const Eigen::Vector2d p1_2d = kd2.corners[md.matches[j].second];

    // TODO SHEET 3: determine inliers and store in md.inliers
    Eigen::Vector3d x_o_l = cam1->unproject(p0_2d);
    Eigen::Vector3d x_o_r = cam2->unproject(p1_2d);
    if (std::abs(x_o_l.transpose() * E * x_o_r) < epipolar_error_threshold) {
      md.inliers.emplace_back(md.matches[j]);
    }
  }
}

void findInliersRansac(const KeypointsData& kd1, const KeypointsData& kd2,
                       const std::shared_ptr<AbstractCamera<double>>& cam1,
                       const std::shared_ptr<AbstractCamera<double>>& cam2,
                       const double ransac_thresh, const int ransac_min_inliers,
                       MatchData& md) {
  md.inliers.clear();

  // TODO SHEET 3: run RANSAC with using opengv's CentralRelativePose and store
  // in md.inliers. If the number if inliers is smaller than ransac_min_inliers,
  // leave md.inliers empty.

  // create the central relative adapter
  Eigen::Vector2d p0_2d, p1_2d;
  opengv::bearingVector_t x_o_l, x_o_r;
  opengv::bearingVectors_t bvs1, bvs2;
  for (size_t j = 0; j < md.matches.size(); j++) {
    p0_2d = kd1.corners[md.matches[j].first];
    p1_2d = kd2.corners[md.matches[j].second];
    x_o_l = (cam1->unproject(p0_2d)).normalized();
    x_o_r = (cam2->unproject(p1_2d)).normalized();
    bvs1.push_back(x_o_l);  // bearing vectors for left eye frame
    bvs2.push_back(x_o_r);  // bearing vectors for right eye frame
  }
  opengv::relative_pose::CentralRelativeAdapter adapter(bvs1, bvs2);
  opengv::essentials_t fivept_nister_essentials =
      opengv::relative_pose::fivept_nister(adapter);

  // create a RANSAC object
  opengv::sac::Ransac<
      opengv::sac_problems::relative_pose::CentralRelativePoseSacProblem>
      ransac;
  // create a CentralRelativePoseSacProblem
  std::shared_ptr<
      opengv::sac_problems::relative_pose::CentralRelativePoseSacProblem>
      relposeproblem_ptr(
          new opengv::sac_problems::relative_pose::
              CentralRelativePoseSacProblem(
                  adapter, opengv::sac_problems::relative_pose::
                               CentralRelativePoseSacProblem::NISTER));
  // run ransac
  ransac.sac_model_ = relposeproblem_ptr;
  ransac.threshold_ = ransac_thresh;
  ransac.max_iterations_ = 1000;
  ransac.computeModel();

  // optimize the result before store into md
  // non-linear optimization (using all available correspondences)
  //  opengv::transformation_t nonlinear_transformation =
  //      opengv::relative_pose::optimize_nonlinear(adapter, ransac.inliers_);
  ransac.sac_model_->optimizeModelCoefficients(
      ransac.inliers_, ransac.model_coefficients_, ransac.model_coefficients_);
  ransac.sac_model_->selectWithinDistance(ransac.model_coefficients_,
                                          ransac.threshold_, ransac.inliers_);

  if (ransac.inliers_.size() >= ransac_min_inliers) {
    // store the result
    for (auto i : ransac.inliers_) {
      md.inliers.emplace_back(md.matches[i]);
    }
    Eigen::Matrix3d R = ransac.model_coefficients_.topLeftCorner(3, 3);
    Eigen::Vector3d t = ransac.model_coefficients_.topRightCorner(3, 1);
    Sophus::SE3d transformation(R, t);
    md.T_i_j = transformation;
  }
}
}  // namespace visnav
