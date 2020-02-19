# Filtering and Edge Detection

> **Image function:**
> $$I : \Omega \subset \R \rightarrow \R_+; (x,y) \rightarrow I(x,y)$$  
> with discretization
> $$\Omega = [1, width]\times[1, height] \subset \Z^2, \R_+=[0,255]\subset\Z_+$$
> or in general:
> $$I = I(x,y) = \{I_R(x,y),I_G(x,y),I_B(x,y)\}$$

Sum up this chapter with Canny Edge Detector.

1. Image Smoothing
    
    Image smoothing uses filters, and filters are operations based on neighborhood. Let's check first two simple filters, correlation and Convolution. They both are
    1. **Shift invariant** (operation independent from the location)
    2. **Linear** (result is linear combination of neighbors of central pixel)
    
    The mathematical expression of **Correlation** and **Convolution** (as a discret $3\times3$ kernel):
    $$J(x,y) = H \circ I = \sum_{i=-1}^1\sum_{j=-1}^1H(i,j)I(x+i,y+j)$$
    $$J(x,y) = H \ast I = \sum_{i=-1}^1\sum_{j=-1}^1H(i,j)I(x-i,y-j) = \sum_{i=-1}^1\sum_{j=-1}^1H(x-i,y-j)I(i,j)$$

    To interpret, applying a convolution on an image is equivalent to first rotating the conv kernel $180\degree$, then do a weighted sum of local region (as gifs in Deep Learning). Normally, the rotation is omitted as the kernel is center symmetric.
    E.g.
    $$H\ast I = \begin{bmatrix}1 & -1\end{bmatrix} \quad \Leftrightarrow \quad H\cdot I =\begin{bmatrix}-1 & 1\end{bmatrix}\cdot \begin{bmatrix}I(x_0) & I(x_0+\Delta x)\end{bmatrix}^T$$

    For image smoothing, the most common one is Gaussian smoothing.
    $$G(u,v) = e^{-\frac{1}{2} \frac{u^2 + v^2}{\sigma^2}} \Rightarrow G(u,v) =e^{-\frac{1}{2}(\frac{u}{\sigma})^2} e^{-\frac{1}{2}(\frac{v}{\sigma})^2}$$(1)
    Here, the expression doesn't use the standard normalization with $\pi$, but it is similar. From (1), the 2D gauss kernel can be replaced by two 1D kernels, this will result a less and fast smoothing operation on an image.

    Note, the higher $\sigma$, the smoother the image becomes.
2. Image Derivatives

    1. Image first derivatives are computed by using the first order approximation of its Taylor expansion, as images are descretized. 
        $$I(x_0 + \Delta x) \approx I(x_0) + \frac{\partial I(x_0)}{\partial x}\Delta x \Rightarrow \frac{\partial I(x_0)}{\partial x} \approx I(x_0 + \Delta x) - I(x_0)$$
        This is also equivalent to apply a filter $\begin{bmatrix}1 & -1\end{bmatrix}$ or $\begin{bmatrix}1 & 0 & -1\end{bmatrix}$.
    2. Second derivative
        $$\frac{\partial^2 I(x_0)}{\partial x^2} \approx I(x_0 + 2\Delta x) - 2I(x_0 + \Delta x) + I(x_0)$$
        Similar to first order, the kernel is  $\begin{bmatrix}1 & -2 & 1\end{bmatrix}$. For 2D 
        $$\nabla^2I(x,y) = \frac{\partial^2 I}{\partial x^2} + \frac{\partial^2 I}{\partial y^2}$$
    
    **Observations:**
       
    * First order derivative is used to find the **magnitude and orientation** of the gradient. Second derivative simply determins whether the evaluated location is an edge by searching the **zero-crossing**.
    * Since convolution has the property **associativety**, applying a derivative on a gauss smoothed image is the same as taking the derivative on the gauss kernel first, and then apply it on the image. This has an advantage that the kernel can be pre-computed. 
    $$I_x = (D_x \ast G) \ast I = G_x \ast I$$
3. Non-maximal Suppression

    After computing the image gradient, we can quantize it into four bins to simplify the searching neighbors ($0\degree$, $45\degree$, $90\degree$, $135\degree$). Then non-maxima suppression is applied to thin the edges. For every edge pixel, find a limit range of neighboring pixels in the direction of its gradient. Take the one with the largest gradient magnitude, while others are set to zero.

4. Hysteresis Thresholding

    Edges gradients above some low threshold are considered to be above the threshold if they are also connected to edges above a higher. They can thus be seen as continuations of these high-confidence areas.

In the previous sections, we only talked about the linear filters. Now, let's check the **non-linear filters**. This tpye of filter takes into account input pixel values before deciding how to use them in the output.

1. Median Filtering

    Median filters preserve the sharp edge, and it is particularly effictive when the noise pattern consists of strong spike-like components. However, for high levels of noise, its performance not that much better than Gaussian blur.
2. Bilateral Filtering

    It replaces the intensity of each pixel with a weighted average of intensity values from nearby pixels. This weight can be based on a Gaussian distribution (simply distance).