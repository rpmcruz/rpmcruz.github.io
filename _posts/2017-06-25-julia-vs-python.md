---
layout: post
title: "Python vs Julia"
category: machine learning
---

As a complement to my other post on Julia, here is a quick comparison between a support vector machine implemented in Python and Julia.

Quick background: a support vector machine tries to find a hyperplane whose distance to the observations (margin) is maximized. Only the points at a distance smaller or equal to 1 are considered: this are known as the __support vectors__, hence the name.

For each support vector $i$, we maximize the distance to the hyperplane, $$y_i \omega\cdot x_i$$, where $$y_i$$ is -1 or +1 depending on its side of the hyperplane. Because we are considering only support vectors, whose distance is smaller than 1, we can turn this into a minimization problem as: $$\min_{\omega_i} \sum_i \max[0,1-y_i \omega\cdot x_i]$$. We probably also want to introduze a regularization term: $$\lambda \sum_q \omega^2_q$$.

I will not consider kernels here.

![Optimal hyperplane](/img/2017-06/svm-optimal-hyperplane.png)

To solve this, we can use gradient descent. We use the first-derivative of this function we want to minimize and give small steps to its zero.

**Python code**

```python
class SVM:
    def __init__(self, lambda_, max_iter=1000):
        self.lambda_ = lambda_
        self.max_iter = max_iter

    def fit(self, X, y):
        nobs = len(y)
        self.w = np.zeros((len(self.classes_)-1, X.shape[1]))
        self.b = np.zeros(len(self.classes_)-1)

        for it in range(self.max_iter):
            dw = np.zeros(self.w.shape)
            db = np.zeros(self.b.shape)

            _y = 2*(y > 0)-1
            A = (1/nobs)*np.sum(
                [-_y[i]*X[i] for i in range(len(X))
                 if _y[i]*np.sum(self.w*X[i]+self.b) < 1], 0)
            B = (1/nobs)*np.sum(
                [-_y[i] for i in range(len(X))
                 if _y[i]*np.sum(self.w*X[i]+self.b) < 1])

            dw = A + 2*self.lambda_*self.w[kk]
            db = B

            # update values
            eta = 1/(it+2)  # (self.lambda_*t)
            self.w -= eta*dw
            self.b -= eta*db
            self.w /= np.sum(self.w*self.w, 1)[:, None]
        return self

    def predict(self, X):
        return (np.sum(X*self.w+self.b, 1) >= 0).astype(int)
```

**Julia code**

```julia
type SVM
    lambda     ::Float64
    max_iter   ::Int64

    # internal
    biases     ::Float64
    weights    ::Array{Float64}
end

function fit(self::SVM, X::Array{Float64,2}, y::Array{Int64})
    @assert size(X, 1) == length(y)
    nobs = length(y)
    self.weights = zeros(size(X, 2))
    self.bias = 0

    for it in 1:self.max_iter
        dw = zeros(size(self.weights))
        db = 0

        _y = 2*(y .> 0)-1

        # fix support vectors
        for i in 1:size(X, 1)
            if _y[i]*sum(self.weights.*X[i,:]+self.bias) < 1
                dw += (1/nobs) * (-_y[i]*X[i,:])
                db += (1/nobs) * (-_y[i])
            end
        end

        # penalty cost (lambda)
        dw += 2*self.lambda*self.weights

        # update values
        eta = 1/(it+2)  # (self.lambda_*t)
        self.weights -= eta*dw
        self.bias -= eta*db
        self.weights ./= sum(self.weights.*self.weights,2)
    end
    self
end

function predict(self::SVM, X::Array{Float64,2})
    yp = sum(broadcast(.*, X, self.weights)+self.bias, 2) .>= 0
    Array{Int}(yp[:, 1])
end
```

Notes:

1. Julia does not work with classes: it uses something such as prototypes from Javascript.
2. I have defined the type of some of the variables in Julia, but this is optional. I am just doing that in order to more easily catch errors.

I adapted my code in a hurry, let me know if there is a problem with it. My SVM implementation is a quite different because we have changed the optimization problem of a multiclass ordinal problem.
