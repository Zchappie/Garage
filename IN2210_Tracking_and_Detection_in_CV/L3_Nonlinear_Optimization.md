# Non-linear Optimization and Robust Estimation for Tracking

1. Objective Function
    
    Previously, we are solving the pose estimation using P-nP and DLT methods, which use only small number of point. This leads to a disadvantage, the accuracy is highly depends on the chosen point pairs. Now with the optimization, we can use as much (of course limited) as possible correspondences to find the camera pose with robustness. 
    > The objective function
    > $$E(p) = \min_{R, T} \sum_i \lVert Proj_{A, R, T}(M_i) - m_i \rVert _2^2 = \min_{R, T} \sum_i \lVert f(p) - b \rVert_2^2$$ (1)

    with $p = \begin{bmatrix}\alpha & \beta & \gamma & t_x & t_y & t_z\end{bmatrix} ^T$. 

    It aims to minimize the difference between projected 3D points and corresponding 2D image points. 
    * We can also minimize the **re-projection error**. It depends on what kind of information we have.
    * A good optimization may require result from P-nP or KLT as **initialization**.

2. Numerical Optimization 
   1. Gradient Descent
      From (1), assume the function $f(p) = Ap$, the optimimal can be found with $p=(A^TA)^{-1}A^Tb$. If not, iterative optimization is needed.
      $$p_{i+1} = p_i - \lambda\nabla E(p_i) = p_i - \lambda 2J(f(p_i))$$
      with 
      $$J(p_i) = \begin{bmatrix}
          \frac{\partial E(u_i)}{\partial \alpha} & \frac{\partial E(u_i)}{\partial \beta} & \frac{\partial E(u_i)}{\partial \gamma} & \frac{\partial E(u_i)}{\partial t_x} & \frac{\partial E(u_i)}{\partial t_y} & \frac{\partial E(u_i)}{\partial t_z} \\
          \frac{\partial E(v_i)}{\partial \alpha} & \frac{\partial E(v_i)}{\partial \beta} & \frac{\partial E(v_i)}{\partial \gamma} & \frac{\partial E(v_i)}{\partial t_x} & \frac{\partial E(v_i)}{\partial t_y} & \frac{\partial E(v_i)}{\partial t_z}
      \end{bmatrix}$$
      The size of Jacobian is $2N \times 6$.
   2. Gauss-Newton and Levenberg-Marquardt

        GN and LM methods use the first order approximation.
        $$\Delta_{i, GN} = -(J^TJ)^{-1}J^T \epsilon_i$$
        $$\Delta_{i, LM} = -(J^TJ + \lambda I)^{-1}J^T \epsilon_i$$
        And the iteration for LM
        
        1. Intialize $\lambda = 0.001$
        2. While not converged, compute $\Delta_{i, LM}$ and $E(p_i + \Delta_{i, LM})$
           1. If $E(p_i + \Delta_{i, LM}) > E(p_i)$, set $\lambda = 10\lambda$
           2. If $E(p_i + \Delta_{i, LM}) < E(p_i)$, set $\lambda = 0.1\lambda$

3. Axis Angles Parameterization
    
    Even though all parameterizations have singularities, Axis Angles is still the best choice (except Quaternions):
    $$q = \begin{bmatrix}\alpha & \beta & \gamma \end{bmatrix}$$
    Interpretation: rotation around the vector $q$, with angle of $\lVert q\rVert_2$.
    * No needs for 9 elements for 3 DoFs.
    * **Exponential map** (From axis angles to rotation matrix) **Rodrigues' Formula**
        $$R = I + (\sin\theta)K + (1-\cos\theta)K^2$$
        with $\theta = \lVert q\rVert_2$, and $K = [q]_{\times}$
    * [**Log map**](https://en.wikipedia.org/wiki/Axis–angle_representation#Log_map_from_SO(3)_to_%7F'"`UNIQ--postMath-0000000D-QINU`"'%7F(3)) (From rotation matrix to axis angles)
    * No gimbal lock compares to Euler Angles.
    * Singularity comes when $\lVert q\rVert_2 = 2n\pi$
    * From Axis Angles to Unit Quaternion
        $$q_{Quat} = (\cos\frac{\theta}{2}, \frac{q}{\theta}\sin\frac{\theta}{2})$$
        Then rotate a point $p$ to $p'$ can be written as
        $$p' = q_{Quat}\cdot p \cdot \overline{q_{Quat}}$$
        with $\overline{q_{Quat}} = (\cos\frac{\theta}{2}, -\frac{q}{\theta}\sin\frac{\theta}{2})$

4. Computing Jacobian
    
    From previous section, Jacobian matrix is the key for optimization. It can be gotten in analytical form in MATLAB, or using **Chain Rule**. First let's expand the $f$ function in (1)
    $$f_{M_i}(p) = m(\tilde{m}(M_{m_i}^{cam}(p)))$$
    and Jacobian is obtained by stacking $J_i$ for all points
    $$J_i = [\frac{\partial f_{M_i}(p)}{\partial p}] = [\frac{\partial m}{\partial \tilde{m}}]_{2\times 3}\cdot [\frac{\partial \tilde{m}}{\partial M_{m_i}^{cam}}]_{3\times 3}\cdot [\frac{\partial M_{m_i}^{cam}}{\partial p}]_{3\times 6}$$

    * $M_{m_i}^{cam}(p) = R(p)M_i + T$ represents transformation of 3D points from world frame to camera frame, thus
        $$\frac{\partial M_{m_i}^{cam}}{\partial p} = \begin{bmatrix}
            [\frac{\partial R}{\partial r_1}]M_i & [\frac{\partial R}{\partial r_2}]M_i & [\frac{\partial R}{\partial r_3}]M_i & \begin{bmatrix}
                1 & 0 & 0\\
                0 & 1 & 0\\
                0 & 0 & 1
            \end{bmatrix}
        \end{bmatrix}$$
        with
        $$\frac{\partial R}{\partial r_1} = \frac{r_i[q]_{\times} + [q \times (I-R)e_i]_{\times}}{\lVert q\rVert_2^2}R$$
        ```matlab
        I = eye(3);
        ei = I(:,i);  % [3,1]
        
        if(norm(r) < 1e-12)
            fprintf('problem: norm(r) = 0')
        end
        dRi=((r(i)*skew(r) + skew(cross(r,(I-R)*ei))) / (norm(r)^2))*R;    
        % formula from the paper
        ```
    * $\tilde{m}(M_{m_i}^{cam})$ represents the projection of 3D points in camera frame to image frame, thus
        $$\frac{\partial \tilde{m}}{\partial M_{m_i}^{cam}} = A$$
        resulting intrinsic matrix.
    * $m(\tilde{m})$ represents converting the homogeneous coordinate to 2D, thus
        $$\frac{\partial m}{\partial \tilde{m}} = \begin{bmatrix}
            1/W & 0 & -\frac{U}{W^2}\\
            0 & 1/W & -\frac{V}{W^2}
        \end{bmatrix}$$

5. Robust Estimation
    
    From Machine Learning, we know that MLE with Gauss noise is equivalent to the least square. However, this assumption may be violated. Thus, one way of handling outliers is to choose a more suitable distribution to represent the noise. Or change the least-squre estimator by a "robust estimator".
    * **Tukey estimator**: 
      * normal distribution for the inliers (small deviation)
      * uniform distribution for the outliers (large deviation)
      * Downside, as it is non-convex function, it will creates **local minima**, and gradient is close to zero when far from the global minimum. This problem is addressed by RANSAC. It's idea is to compute a set of pose from subsets of point pairs, then find the pose which majority agrees on. (I know what I meant here) 
    
    To summarize, the type of estimator which **the objective function is a sample average called M-Estimator**, check some types in the figure. 
    
    ![M-Estimators](https://www.researchgate.net/profile/Peter_Claes/publication/221810073/figure/fig2/AS:213903339462660@1428009938150/M-estimators-Different-M-estimators-left-column-and-their-outlier-influence-functions.png)

    * (a) L2
    * (c) Cauchy
    * (e) Tukey
    * (b,d,f) are corresponding outlier influence functions 

    **Observations**: Solving the objective function with M-Estimator is equivalent to solve the weighted least-square problem. Thus, the gradient can be re-written as follows (LM case)
    $$\Delta_{i, LM} = -(J^TWJ + \lambda I)^{-1}J^TW \epsilon_i$$