# Optimization Algorithms

First check the great post from Sebatiam Ruder, [An overview of gradient descent optimization algorithms](https://ruder.io/optimizing-gradient-descent/index.html#gradientdescentvariants).

## Takeaways

1. Three variants of gradient descent, **Batch GD**, **Stochastic GD**, **Mini-batch GD**, differ in the size of data for computing gradients.
    * **Batch GD**: One calculation of gradients per whole dataset. Could be really slow.
