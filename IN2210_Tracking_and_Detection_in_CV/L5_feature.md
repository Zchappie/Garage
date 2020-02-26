# Detection of Features/Keypoints/Interest Points

Everything could be found in [the book of zeliski](http://szeliski.org/Book/drafts/SzeliskiBook_20100903_draft.pdf), chapter 4. Or the slides from Stanford CS231 [lecture 6](http://vision.stanford.edu/teaching/cs131_fall1617/lectures/lecture6_detectors_harris_cs131_2016.pdf) and [lecture 7](http://vision.stanford.edu/teaching/cs131_fall1617/lectures/lecture7_dog_sift_cs131_2016.pdf) (year 16).

(Here goes the general idea, 4 criteria)

1. Harris Detector
   1. Mathematics expression

        Window function is Gaussian, as it is rotation invariant (symmetric).
   
    **Observations**:
    
    * Invariant to intensity shift/scale, partially invariant to affine intensity change; but not invariant to scaling.

    2. Harris-Laplace Detector

2. Blob Detectors
    
    **Difference between an edge and a blob**: after convolved with Laplace kernel, edge is at the ripple, and blob is at the superposition of two ripples.

    1. DoG to approximate Laplacian

3. Hessian Corner Detector