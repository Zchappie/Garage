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

#include <sophus/se3.hpp>

#include <visnav/common_types.h>

#include <cmath>

namespace visnav {

// Implement hat operation of a vector
template <class T>
Eigen::Matrix<T, 3, 3> hat_operator(const Eigen::Matrix<T, 3, 1>& vec) {
  Eigen::Matrix<T, 3, 3> skewMat;
  skewMat << 0, -1 * vec(2, 0), vec(1, 0), vec(2, 0), 0, -1 * vec(0, 0),
      -1 * vec(1, 0), vec(0, 0), 0;
  return skewMat;
}

// Implement exp for SO(3)
template <class T>
Eigen::Matrix<T, 3, 3> user_implemented_expmap(
    const Eigen::Matrix<T, 3, 1>& xi) {
  // TODO SHEET 1: implement

  Eigen::Matrix<T, 3, 3> expMat;   // the output matrix
  Eigen::Matrix<T, 3, 3> unitMat;  // unit matrix
  unitMat << 1, 0, 0, 0, 1, 0, 0, 0, 1;
  Eigen::Matrix<T, 3, 1> dirVec;  // the vector a

  double theta = xi.norm();
  if (theta <= 0.000001) {
    expMat = unitMat;
    return expMat;
  }
  dirVec = xi / theta;

  Eigen::Matrix<T, 3, 3> skewMat = hat_operator(dirVec);  // skew matrix of a

  expMat = cos(theta) * unitMat +
           (1 - cos(theta)) * dirVec * dirVec.transpose() +
           sin(theta) * skewMat;

  return expMat;
}

// Implement log for SO(3)
template <class T>
Eigen::Matrix<T, 3, 1> user_implemented_logmap(
    const Eigen::Matrix<T, 3, 3>& mat) {
  // TODO SHEET 1: implement

  T theta = acos((mat.trace() - 1) / 2);
  Eigen::Matrix<T, 3, 1> helpVec;
  helpVec << mat(2, 1) - mat(1, 2), mat(0, 2) - mat(2, 0),
      mat(1, 0) - mat(0, 1);

  Eigen::Matrix<T, 3, 1> vec;
  if (theta <= 0.000001) {
    vec << 0, 0, 0;
  } else {
    vec = 1 / (2 * sin(theta)) * helpVec;
    vec = vec * theta;
    return vec;
  }
}

// Implement exp for SE(3)
template <class T>
Eigen::Matrix<T, 4, 4> user_implemented_expmap(
    const Eigen::Matrix<T, 6, 1>& xi) {
  // TODO SHEET 1: implement

  Eigen::Matrix<T, 4, 4> euMat;  // output, the sepecial euclidian mtrix

  Eigen::Matrix<T, 3, 3> rotMat;   // rotation matrix of 4*4
  Eigen::Matrix<T, 3, 1> rotVec;   // rotation part from 6*1
  Eigen::Matrix<T, 3, 1> tranVec;  // translation part of 6*1
  Eigen::Matrix<T, 3, 3> unitMat;  // unit matrix
  unitMat << 1, 0, 0, 0, 1, 0, 0, 0, 1;
  Eigen::Matrix<T, 3, 1> dirVec;  // direction of rotation vector, a

  rotVec << xi(3, 0), xi(4, 0), xi(5, 0);
  tranVec << xi(0, 0), xi(1, 0), xi(2, 0);
  rotMat = user_implemented_expmap(rotVec);

  double theta = rotVec.norm();

  // avoid divide zero
  if (theta <= 0.000001) {
    dirVec << 0, 0, 0;
    tranVec << 0, 0, 0;
  } else {
    dirVec = rotVec / theta;
    tranVec = ((sin(theta) / theta) * unitMat +
               (1 - (sin(theta) / theta)) * dirVec * dirVec.transpose() +
               ((1 - (cos(theta))) / theta) * hat_operator(dirVec)) *
              tranVec;
  }

  euMat << rotMat, tranVec, 0, 0, 0, 1;
  return euMat;
}

// Implement log for SE(3)
template <class T>
Eigen::Matrix<T, 6, 1> user_implemented_logmap(
    const Eigen::Matrix<T, 4, 4>& mat) {
  // TODO SHEET 1: implement

  Eigen::Matrix<T, 6, 1> xi;
  Eigen::Matrix<T, 3, 3> rotMat;   // rotation matrix from 4*4
  Eigen::Matrix<T, 3, 1> rotVec;   // rotation part from 6*1
  Eigen::Matrix<T, 3, 1> tranVec;  // translation part from 6*1
  Eigen::Matrix<T, 3, 3> unitMat;  // unit matrix
  unitMat << 1, 0, 0, 0, 1, 0, 0, 0, 1;
  Eigen::Matrix<T, 3, 1> dirVec;  // direction of rotation vector, a

  rotMat = mat.block(0, 0, 3, 3);
  rotVec = user_implemented_logmap(rotMat);
  tranVec = mat.topRightCorner(3, 1);

  T theta = acos((rotMat.trace() - 1) / 2);
  Eigen::Matrix<T, 3, 1> helpVec;
  helpVec << rotMat(2, 1) - rotMat(1, 2), rotMat(0, 2) - rotMat(2, 0),
      rotMat(1, 0) - rotMat(0, 1);

  if (theta <= 0.000001) {
    xi << 0, 0, 0, 0, 0, 0;
  } else {
    dirVec = rotVec / theta;

    Eigen::Matrix<T, 3, 3> J;
    J = (sin(theta) / theta) * unitMat +
        (1 - (sin(theta) / theta)) * dirVec * dirVec.transpose() +
        ((1 - (cos(theta))) / theta) * hat_operator(dirVec);
    tranVec = J.inverse() * tranVec;
    xi << tranVec, rotVec;
    return xi;
  }
}

}  // namespace visnav
