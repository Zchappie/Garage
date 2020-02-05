# Optimization Algorithms

First check the great post from Sebatiam Ruder, [An overview of gradient descent optimization algorithms](https://ruder.io/optimizing-gradient-descent/index.html).

## Takeaways

1. Three variants of gradient descent, **Batch GD**, **Stochastic GD**, **Mini-batch GD**, differ in the size of data for computing gradients.
    * **Batch GD**: One calculation of gradients per whole dataset. Could be really slow.

    * **Stochastic GD**: performs a parameter update for each training example. May fluctuate heavily. When we slowly decrease the learning rate, SGD shows the same convergence behaviour as batch GD.

    * **Mini-batch GD**: update after 50-256 samples. Somebody use SGD to refer to Mini-batch GD.

2. Gradient descent optimization algorithms address the challenges of GD variants. Easy to be trapped in saddle points; unflexible update for different features with different frequencies.

    * **Momentum**: alleviate zig-zag behavior of SGD. But may rush at the minimum too fast to stop.

