# Detection of Features/Keypoints/Interest Points

Everything could be found in [the book of zeliski](http://szeliski.org/Book/drafts/SzeliskiBook_20100903_draft.pdf), chapter 4. Or the slides from Stanford CS231 [lecture 6](http://vision.stanford.edu/teaching/cs131_fall1617/lectures/lecture6_detectors_harris_cs131_2016.pdf) and [lecture 7](http://vision.stanford.edu/teaching/cs131_fall1617/lectures/lecture7_dog_sift_cs131_2016.pdf) (year 16).

First check what is Features/Keypoints/Interest Points:
* are image patterns which differ from its immediate neighborhood
* they are related to interesting locations in the image and they speed up computation
* they also serve to give a new compact representation of an image
* they can reliably describe the objects or their parts

And they should be **local**, **invariant** to illumination changes and geometric transformations, **distinctive**, **robust** to noise and some operations.

1. Harris Corner Detector
   1. Mathematics expression
        In order to find the corner, by searching in both x and y directions, we come to the $M$ matrix (**second moment matrix**):
        $$M = \sum_{x,y}w(u,v)\begin{bmatrix}
            I_x^2 & I_xI_y\\
            I_xI_y & I_y^2
        \end{bmatrix}$$
        Notice, window function is Gaussian, as it is rotation invariant (symmetric).Intuitively, a corner is a point where both the $I_x$ and $I_y$ are relatively large. In mathematical way, this means that both eigenvalues of the matrix $M$ are large. To simplify this, we have 
        $$R = \det(M) - \alpha \cdot trace(M)^2 = \lambda_1\lambda_2 - \alpha(\lambda_1+\lambda_2)^2$$
        When apply a threshold on $R$, we can get the desired corner.
   
       **Observations**:
       * Invariant to intensity shift/scale, partially invariant to affine intensity change; but not invariant to scaling.

    1. Harris-Laplace Detector
        
        Since original Harris detector can't deal with scale variations, to address this problem, we have Harris-Laplace Detector. Applies Harris corner detector at multiple scales and uses Laplacian operator for **scale selection**. The **characteristic scale** as the scale that produces peak of Laplacian response, but do remember to normalize the Laplacian.

2. FAST
   
   This is the most intuitive (easy) corner detector. It searches the surrounding pixels of the center one, and do the intensity comparisions. A point is assigned to a corner when 12 consecutive pixels have larger or smaller intensity values at the same time comparing to the center. 
3. Blob Detectors
    
    The Laplacian is introduced in Harris-Laplace Detector. Here, Blob also uses it to find the *blob*. **Difference between an edge and a blob**: after convolved with Laplace kernel, edge is at the ripple, and blob is at the superposition of two ripples. The process is also simple:
    1. Convolve image with scale-normalized Laplacian at several scales
    2. Find maxima of squared Laplacian response in scale-space
    
    Note, we can use **DoG** to approximate Laplacian to speed up the computation.

4. Hessian Corner Detector (DoH)

5. Comparision of detectors
   
Detector | Illumination | Rotation | Scale | View point
-|-|-|-|-
DoG | Yes | Yes | Yes | No
Harris corner | Yes | Yes | No | No