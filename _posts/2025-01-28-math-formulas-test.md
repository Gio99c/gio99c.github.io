---
layout: post
title: "Testing LaTeX Math Formulas"
date: 2025-01-28
author: Giuseppe Concialdi
comments: true
math: true
---

This is a test post to demonstrate how to use LaTeX math formulas in your Jekyll blog posts.

## Inline Math

You can write inline math using single dollar signs: $E = mc^2$ is Einstein's famous equation.

Here's another example: The quadratic formula is $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$.

## Block Math

For larger equations, use double dollar signs for display math:

$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$

Here's a more complex example with matrices:

$$
\begin{bmatrix}
a & b \\
c & d
\end{bmatrix}
\begin{bmatrix}
x \\
y
\end{bmatrix} = 
\begin{bmatrix}
ax + by \\
cx + dy
\end{bmatrix}
$$

## Machine Learning Examples

### Linear Regression

The linear regression model is defined as:

$$
y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \cdots + \beta_n x_n + \epsilon
$$

### Gradient Descent

The gradient descent update rule:

$$
\theta_{t+1} = \theta_t - \alpha \nabla J(\theta_t)
$$

### Neural Network Forward Pass

For a neural network with one hidden layer:

$$
h = \sigma(W_1 x + b_1) \\
y = W_2 h + b_2
$$

Where $\sigma$ is the activation function.

## Probability and Statistics

### Bayes' Theorem

$$
P(A|B) = \frac{P(B|A) P(A)}{P(B)}
$$

### Normal Distribution

$$
f(x) = \frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}
$$

## Code with Math

You can combine code and math. For example, in Python:

```python
import numpy as np

# Calculate the mean: μ = (1/n) * Σ(x_i)
def calculate_mean(data):
    return np.mean(data)

# Calculate variance: σ² = (1/n) * Σ(x_i - μ)²
def calculate_variance(data):
    return np.var(data)
```

The mathematical formulas above correspond to the code implementations.

## Conclusion

Now you can write beautiful mathematical expressions in your blog posts! The KaTeX library will automatically render all the LaTeX math formulas.

### Supported Delimiters

- Inline math: `$...$` or `\(...\)`
- Display math: `$$...$$` or `\[...\]`

Try creating a new post and including some mathematical formulas to test it out! 