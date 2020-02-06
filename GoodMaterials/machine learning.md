# Optimization Algorithms

First check the great post from Sebatiam Ruder, [An overview of gradient descent optimization algorithms](https://ruder.io/optimizing-gradient-descent/index.html).

## Takeaways

1. Three variants of gradient descent, **Batch GD**, **Stochastic GD**, **Mini-batch GD**, differ in the size of data for computing gradients.
    * **Batch GD**: One calculation of gradients per whole dataset. Could be really slow.

    * **Stochastic GD**: performs a parameter update for each training example. May fluctuate heavily. When we slowly decrease the learning rate, SGD shows the same convergence behaviour as batch GD.

    * **Mini-batch GD**: update after 50-256 samples. Somebody use SGD to refer to Mini-batch GD.

2. Gradient descent optimization algorithms address the challenges of GD variants. Easy to be trapped in saddle points; unflexible update for different features with different frequencies.

    * **Momentum**: alleviates zig-zag behavior of SGD. But may rush at the minimum too fast to stop (overshot).

    * **Adagrad**: adapts the learning rate to the parameters, performing smaller updates for parameters associated with frequently occurring features, and larger updates for parameters associated with infrequent features. It is well-suited for dealing with **sparse** data.

    * **RMSprop and Adadelta**: take fixed number of previous momentums into gradient update. They address the problem of Adagrad, which is aggressive, monotonically decreasing learning rate.

    * **Adam**: kind of combination of Momentum and RMSprop.

3. [How to choose the optimizer?](https://ruder.io/optimizing-gradient-descent/#whichoptimizertouse)

# Mistakes in Deep Learning project

1. Check closely the existed functions before using them in the loss function, such as `MSE`.

2. Think about image augmentation if the data is not enough.

3. If data augmentation is not feasible, try to come up ways get more data, e.g. different ways of constructing triplets.

4. [TQDM](https://tqdm.github.io) is a nice tool to show the progress by bar (percent).