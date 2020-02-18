# Camera Model and Pose Estimation

## Parametriztion
1. Why we use homogeneous coodinates?  
    1. To capture the concept of **infinity**, with `z=0` (last component of the coordinate). This is extremely useful when some tedious geometric calculate is involved.
    2. **Projective geometry** relies heavily on homogeneous coordinates as well. Side notes, projective geometry doesn't presever lots of properties, such as length, angle and etc.
    3. Compactly formulate the coordinate transformation in a single matrix operation.

2. Camera Intrinsics
    $$\begin{bmatrix}
    k_uf & 0 & u_0\\
    0 & k_vf & v_0\\
    0 & 0 & 1
    \end{bmatrix}$$ 
    * $k_u$ and $k_v$ are set according to the shape of the pixel.
    * $u_0$ and $v_0$ are principle point coordinates, usually set as image center. 
    * Camera distortion has two cases in general: radial (important) + tangential. And the image is undistorted through a look-up table.

3. The Full Homogeneous Transformation, from world coordinate to image 
    $$p_{hom} = PX = KP_0TX = \begin{bmatrix}
    k_uf & 0 & u_0\\
    0 & k_vf & v_0\\
    0 & 0 & 1
    \end{bmatrix} \begin{bmatrix}
    1 & 0 & 0 & 0\\
    0 & 1 & 0 & 0\\
    0 & 0 & 1 & 0
    \end{bmatrix} \begin{bmatrix}
    r_{11} & r_{12} & r_{13} & t_1\\
    r_{21} & r_{22} & r_{23} & t_2\\
    r_{31} & r_{32} & r_{33} & t_3
    \end{bmatrix} \begin{bmatrix}
        x \\ y \\ z \\ 1 
    \end{bmatrix}$$ (1)

4. Inverse of Transformation
   $$R_{inv} = R^T$$ 
   $$T_{inv} = -RT$$

5. Camera Optical Ray

    For a camera center $C$, any point which results as the same projection on the image as point $M$ has the property 
    $$PX(\lambda) = (1 - \lambda)PM$$ 
    as $PC = 0$
    $$X(\lambda) = M + \lambda(C - M)$$
    $$0 = PC = A[R|t]C_{hom} = ARC + At$$
    leads to 
    $$C = -(AR)^{-1}At = -Q^{-1}q$$
    For any image point $m$, the optical ray $X$ through it has the property
    $$X = C + Q^{-1}m$$

## Extract Camera Pose
1. DLT (Direct Linear Transformation) algorithm
   
   The goal of DLT algorithm is estimating the position and orientation of camera from 2D/3D point pairs when the camera intrinsics are unknown.
   From (1) (note, here uses non-homogenous version, it's kind of abuse of notation, but understandable), given a 3D point $M_i$ in the world frame and corresponding 2D coordinate $m_i$ on the image, we can get the equation
   $$m_i = PM_i$$(3)
   Reformulate the equation, stack all unknowns from $P$ at the right side, and rests at left side, we get
   $$BP_{stack} = 0$$ (2)
   In order to solve this 12-unknow (essentially 11, defined up to a scale) equation system, we need at least 6 correspondences. More for robustness. Then
   $$P = (P_{3\times3}|p_{3\times1})$$
   and 
   $$P_{3\times3}P_{3\times3}^T = AR(AR)^T = AA^T$$
   $A$ could be found through Choleski factorization, as $A$ is upper-triangular matrix. And $AA^T$ is called **image of the absolute conic**. With $P_{3\times3}=AR$, $R = A^{-1}P_{3\times3}$. Note, no guarantee that it is a orthonormal rotation matrix. The real rotation matrix can be gotten from SVD of $A^{-1}P_{3\times3} = USV^T$, and $R= UV^T$.


2. P3P algorithm

    In previous method, the camera intrinsics are also unknowns. Now suppose that we know $A$, then only 6 unkowns are left (3 for rotation and 3 for translation). Thus, at least 3 correspondences are needed to recover the parameters, that's why it is called P3P (Perspective 3 Points).

    The detailed procedure can be seen [here](https://www.wikiwand.com/en/Perspective-n-Point#/P3P). For three points, let $X$, $Y$, $Z$ as the depths to the camera center, $\alpha$, $\beta$, $\gamma$ as the angles between every two optical rays, $a$, $b$, $c$ as distances between two points, then the equation system holds
    $$Y^2 + Z^2 - 2\cos\alpha YZ - X^2 = 0$$
    $$X^2 + Z^2 - 2\cos\beta XZ - Y^2 = 0$$
    $$Y^2 + X^2 - 2\cos\gamma XY - Z^2 = 0$$

    When $X$, $Y$, $Z$ are computed, let $\overline{M}^w$ is the center point of 3D points in world coordinate, $N^w_i = M^w_i - \overline{M}^w$, and correspondingly, $\overline{M}^c$ and $N^c_i$. The rotation matrix is found through 
    $$R = \argmax_R \sum_i (N^c_i)^T(RN^w_i)$$
    This optimization problem forces the $RN^w_i$ to be as close as possible to $N^c_i$, and translation can also be found
    $$T = \overline{M}^c - R\overline{M}^w$$

    **Observations:**
    
    * Minimally, 3 correspondences is sufficient, but it is not uniquely defined, thus, we need the fourth.
    * In practical, the more point pairs used the better.
    * The four solutions can be interpreted as intersections of three toroids.
    * The chosen point correspondences **cannot be colinear**.

3. (Special case) Pose Estimation from a Plane
   
    From (3), we have equation for a planer case
    $$x = A\begin{bmatrix}R_{3\times1}&R_{3\times1}&R_{3\times1}& T\end{bmatrix}\begin{bmatrix}X\\Y\\0\\1\end{bmatrix} = 
    \begin{bmatrix}R_{3\times1}&R_{3\times1}& T\end{bmatrix}\begin{bmatrix}X\\Y\\1\end{bmatrix} 
    = H\begin{bmatrix}X\\Y\\1\end{bmatrix}$$