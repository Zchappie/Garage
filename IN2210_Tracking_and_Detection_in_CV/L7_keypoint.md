# Keypoint Recognition

Random Forest and Random Ferns can be found [here](http://vision.cse.psu.edu/seminars/talks/2009/random_tff/ForestsAndFernsTalk.pdf).

1. Random Forest
   
   1. The full dataset contains $N$ samples, the single decision tree takes $n$ samples as training dataset. $n<N$, and pick out with replacement. This step is also called **Bagging**.
   2. To train single decision tree, first pick $m$ features out of $M$ input features for every node, then only choose the best one (Gini index/Entropy/Misclassification rate) to splite.
   3. Splite the node until pure at the leave. Since the previous two precodures produce enough randomness, without proning, it will not over-fitting.
   4. Train $K$ trees with the same approach.
   5. Regression (average of the all outputs from trees) or classification (majority vote of all outputd from trees).
   
2. Random Ferns
   
   The story begins from Navie Bayesian. As we know from Machine Learning
   $$\argmax_k P(C_k|f_1, f_2, ...,f_M) = \argmax_k P(f_1, f_2, ...,f_M|C_k)*P(C_k)$$
   assume the features are independent
   $$Class(f) = \argmax_k P(C_k) \prod_i^MP(f_i|C_k)$$
   However, the independence assumption may not hold, thus, we have Semi-Naive Bayesian. First, group features into $L$ small sets of size $S = \frac{M}{L}$ 
   $$F_l = \{f_{l,1}, f_{l,2}, ...,f_{l,S}\}$$ 
   with $f_n \in \{0,1\}$, and make the assumption that the $F_n$s are independent with each other. Then the likelihood will be 
   $$P(f_1, f_2, ...,f_M|C_k) = \prod_l^LP(F_l|C_k)$$
   Finally, maximize the posterior is fomulated as 
   $$Class(f) = \argmax_k P(C_k) \prod_l^LP(F_l|C_k)$$ (1)$$
    For further improvement, we can adjust the balance by by choice of Fern size, number of Fern. It is a trade-off between complexity and performance.
    
    Now, let's have a look how single fern works during **training**.
    1. One binary test between two pixels' intensities is counted as a feature, and in total $S$ tests. Group all the tests result as a binary code. Convert to decimal, this code will be in $[0, 2^S-1]$. 
    2. For all samples from the same class, do the previous step. The result codes will be a multinomial distribution $P(F_0|C_0)$.
    3. Get all multinomial distributions $P(F_0|C_k)$ for all classes from this fern, store them. Then the training is done.

    **Prediction**:
    1. Apply the test image to a fern, get the binary code, then convert it to decimal.
    2. Extract all the probabilities from $P(F_0|C_k)$ with the same decimal.
    3. Then normalize, and we get the probability of the test image belongs to each class. ![prediction by single fern](https://lh3.googleusercontent.com/proxy/ZbO96QMIs1ZyQPYLGC5T_GI_6k-TfeLdcE5oIB9GI7MtxAWtm39klzYI4JtWbrNTZHGbzdXf5RnnctnshmlCZG8rvBKswUIC0Nx6cDnGLkuECBOT1cnHNSQ)
    4. Repeat the previous steps for all the ferns, and use (1) to get the final perdicted label. ![prediction from all ferns](https://pic4.zhimg.com/80/v2-51941fa7cdb784e41e3d2f2ec1c1bea3_hd.png)


3. Observations

    1.  (Following words come from the [paper](https://www.epfl.ch/labs/cvlab/wp-content/uploads/2018/08/OzuysalCLF10.pdf), page 10) A tree can be transformed into a Fern by performing the following steps. First, we constrain the tree to systematically perform the same test across any given hierarchy level, which results in the same feature being evaluated independently of the path taken to get to a particular node. Second, we do away with the hiearchical structure and simply store the feature values at each level. This means applying a sequence of tests to the patch, which is what Ferns do. ![transform tree to fern](https://csdl-images.computer.org/trans/tp/2010/03/figures/ttp20100304484.gif)
    2. Some comparision
   
        Random Forest | Random Ferns
        --- | --- 
        Directly learn the posterior| Learn the conditional probability 
        The tests at every node is different | Same tests for single input
        Exponentially time needed with tree depth grows | Linear time needed with ferns size grow

4. BRIEF
   
   Check [here](https://medium.com/analytics-vidhya/introduction-to-brief-binary-robust-independent-elementary-features-436f4a31a0e6).
    
    Important points:
    * Do a gaussian blur before compute the binary vectors like in ferns. Brief deals with the image at pixel level so it is very noise-sensitive. By pre-smoothing the patch, this sensitivity can be reduced, thus increasing the **stability** and **repeatability** of the descriptors.
    * Diﬀerent approaches to choosing the test locations. GII and GIV are the best, GV is the worst. ![Diﬀerent approaches to choosing the test locations](https://miro.medium.com/max/1250/0*bTfQfO4qOxk3qL78)

5. Hough Forest

    Check [the original paper](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.204.6049&rep=rep1&type=pdf).

    **Observations**:
    * The random trees in Hough forests are constructed according to a standard random forest framework.
    * The ideal binary test should split the cuboids in such a way as to minimize the uncertainty of their **class label** and **displacement vectors**.
    * At each node during training, either class or displacement uncertainty is chosen at **random** to be minimized at that given node.
    * During prediction, put all small patches from an image to the trained forest. Do the averaging inside the leaf where a patch falls into. The pointed position will be the center of the object with high probability. Do this step for all patches, then a non-maximum suppression to get the prediction of objects' position.
    * The feature descriptors of patches could be HoG, intensities comparision, etc. 
    * Hough Forest could also be used in scale-space. The steps are the same, only the test images are scaled into different sizes. After detection for each scale, summarize the result into the original image. 