# Object detection with ConvNets

Detection task: associate object class with **probability** to the **location** of the object(s) in the image. In general, there are two ways to tackle this problem:
1. Using sliding window, generate multiple small image patches and feed them into the CNN to do the classification.
2. Region Proposal + Classification approach

Here is a [blog](https://towardsdatascience.com/r-cnn-fast-r-cnn-faster-r-cnn-yolo-object-detection-algorithms-36d53571365e) covers R-CNN, Fast R-CNN, Faster R-CNN, and YOLO; and [Lilian Weng's blog](https://lilianweng.github.io/lil-log/2017/12/31/object-recognition-for-dummies-part-3.html#r-cnn).

## Two-stage detectors

 1. [R-CNN](https://www.cv-foundation.org/openaccess/content_cvpr_2014/papers/Girshick_Rich_Feature_Hierarchies_2014_CVPR_paper.pdf) ![R-CNN](https://lilianweng.github.io/lil-log/assets/images/RCNN.png) R-CNN stands for *Regions with CNN features*. Now let's check the object detection system overview. 
    1. The system takes an input image
    2. Extracts around 2000 **bottom-up region proposals**
    3. Computes features for each proposal using a large CNN 
    4. Classifies each region using class-specific linear SVMs.
   
    Detailed information:
    * Architecture of CNN, VGG or ResNet
    * All CNN parameters are shared across all categories.
    * During training:
      * First pre-training is done by classification datasets.
      * Fine-tuning is done by SGD with only warped region proposals.
      * Train class specific SVM.
      * Train class specific Bounding-box regression. The goal of Bounding-box regression is to learn a **transformation** that maps a proposed box to a ground-truth box.
    * During detection:
      * First wrap one proposed region into CNN to get the feature vector
      * Then for each class, score the feature vector use corresponding SVM
      * Apply a greedy non-maximum suppression (for each class independently) that rejects a region if it has an intersection-over-union (IoU) overlap with a higher scoring selected region larger than a learned threshold.
    
    More information check [v5](https://arxiv.org/abs/1406.4729)

1. [SPPNet](https://arxiv.org/pdf/1406.4729.pdf) ![sppnet](https://miro.medium.com/max/1910/1*n4LE9idyGJX_efOsS-FNvw.png) ![spp](https://miro.medium.com/max/1374/1*EMhHR_g4UWEYpxsVWdpKdA.png) The main goal of **spatial pyramid pooling** layer is to remove the fixed-size constraint of the network (from fully connected layer). *In other words, it performs some information “aggregation” at a deeper stage of the network hierarchy (between convolutional layers and fully-connected layers) to avoid the need for cropping or warping at the beginning.* 

    * **Some observations:**
       * Last SPP is performed on arbitrary input sizes. Simply speaking, it divides the input features into 16/4/1 subvectors, then apply the pooling operation (normally it's max).
       * Compare to R-CNN: run the convolutional layers only once on the entire image (regardless of the number of windows), and then extract features by SPP-net on the feature maps.
   
2. [Fast-R-CNN](https://arxiv.org/pdf/1504.08083.pdf)
    
    When we look back, R-CNN and SPPNet have some drawbacks respectively (detailed information check the paper linked right above):
    * R-CNN needs several steps to train, and the training is time and space demanding. Object detection is also slow.
    * SPPNet's training is still a multi-stage pipeline, requires fine-tuning and is expensive(SVM). Fine-tuning algorithm cannot update the ConvNet layers that precede to SPP layer which limits the accuracy

    Now let's look at the Fast R-CNN. It joints the feature extractor, classifier and a regressor in a single neural network.
    
    ![fast](https://lilianweng.github.io/lil-log/assets/images/fast-RCNN.png)
    **Overview**:
    1.  An input image and multiple regions of interest (RoIs) are input into a **fully convolutional** network. 
    2.  RoI projection means record the regions which are the proposals in conv features.
    3.  The last max pooling layer is replaced by a RoI pooling layer. Each RoI is pooled into a fixed-size feature map and then mapped to a feature vector by fully connected layers (FCs).
    4.  The network has two output vectors per RoI: **softmax probabilities** and per-class **bounding-box** regression offsets. 
    5.  The architecture is trained end-to-end with a multi-task loss.

    **Important aspects:**
    * [RoI-Pooling](https://lilianweng.github.io/lil-log/2017/12/31/object-recognition-for-dummies-part-3.html#roi-pooling) This step also solve the fixed-size problem. Relate to SPPNet, Fast-RCNN is a special case of SPPNet with only one pyramid level.
    * As the result, Fast-RCNN is really fast, however, it's computation mainly dominated by the region proposals, as the region proposals are generated separately by another model and that is very expensive. And we need Faster-RCNN.

3. [Faster-RCNN](https://arxiv.org/pdf/1506.01497.pdf)

    Check the post again from [Lilian](https://lilianweng.github.io/lil-log/2017/12/31/object-recognition-for-dummies-part-3.html#faster-r-cnn). Simple equation to explain the main idea. 

    **Faster RCNN = Fast R-CNN + Region Proposal Network** 
    
    ![](https://lilianweng.github.io/lil-log/assets/images/faster-RCNN.png)

    Now look closely:
    * RPN (Region Proposal Network): Takes the feature map from last conv layer, sliding a small conv net to generate around 2400 box region proposals (anchors). Then only keep around 256 of them as anchors and stores in a big vector. One branches to do classification, and the other to do regression.

    How to train?
    * Alternating training

## One-stage Detectors

Again, check the [blog](https://lilianweng.github.io/lil-log/2018/12/27/object-detection-part-4.html). The main difference is this approach skips the region proposal stage and runs detection directly over a dense sampling of possible locations.

1. YOLO
   1. The [workflow](https://lilianweng.github.io/lil-log/2018/12/27/object-detection-part-4.html#workflow)


## Pitch - SSD6D