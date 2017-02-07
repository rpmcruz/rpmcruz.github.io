---
layout: post
title: Deterministic random forests are stochastic?
category: machine learning
---

In the data science section of stackexchange, [J. C. Leitão asks](http://datascience.stackexchange.com/questions/16800/why-max-features-n-features-does-not-make-the-random-forest-independent-of-num),

> If I use `RandomForestClassifier(n_estimators, max_features=None, bootstrap=False)`, this should produce the same scores no matter how many `n_estimators` are used, right?

Note that `bootstrap=False` disables random forest resampling of observations, and `max_features=None` disables sampling of features for each tree.

But the poster says, according to his tests, the scores were not the same:

> predict(foo10)   # 0.906060606061
> predict(foo100)  # 0.933333333333
> predict(foo200)  # 0.915151515152

This puzzled me as well.

At first, I thought this was a precision error kind of thing. He generates his data from the same distribution. I thought what was going on was that there was some precision-casting error between the Python code and the Cython code, which sklearn uses internally for the decision trees.

I figured that some funny digit truncation was going on, and a lot of classes `y` from both classes ended up having the same values of `X`. And, I thought, the decision tree was deciding ties using randomness.

But I found no evidence of tie randomness being used. And it did not make much sense anyway. The float precision is the same, they pointed to the same memory address, and it really did not make much sense anyway.

But I had to figure this one out, especially since I have some experience in decision trees. We tried using them for some experimental models of ours, where the user specifies the number of false-negatives he wants rather than using cost matrices (I can expand on this if you want). Anyway, I lost all morning on this hehe.

What is going on is that the [`DecisionTreeClassifier`](http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html) has some stochastic behavior. For instance, the [splitter code](https://github.com/scikit-learn/scikit-learn/blob/14031f65d144e3966113d3daec836e443c6d7a5b/sklearn/tree/_splitter.pyx) iterates through the features at random:

```python
        f_j = rand_int(n_drawn_constants, f_i - n_found_constants,
                       random_state)
```

This is especially a problem on the lower branches where there is little data. The scores will be identical no matter what decision rule is used (for the training data), therefore things such as the feature iteration order are important.

If the algorithm computes the score for feature A and then computes the score for feature B and it gets score N. Or if it computes first the score for feature B and then for feature A and it gets the same score N, you can see how each decision tree will be different, and have different scores during test, even if the train score is the same.

This is a problem especially becuase the data is small and comes from the same distribution. The problem can be ameliorated, by (a) increasing the data, (b) make it more separable, or (c) use `max_depth != None`.

The solution? Pass `random_state` to `RandomForestClassifier`. It will pass along this parameter to each decision tree, and so they will all be the same, and so will the final score.

This is my code if someone wants to play with it. It includes my own implementation of a random forest.

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import numpy as np


class MyRandomForestClassifier:
    def __init__(self, n_estimators):
        self.n_estimators = n_estimators

    def fit(self, X, y):
        self.trees = [DecisionTreeClassifier(random_state=1).fit(X, y)
                      for _ in range(self.n_estimators)]
        return self

    def predict(self, X):
        yp = [tree.predict(X) for tree in self.trees]
        return ((np.sum(yp, 0) / len(self.trees)) > 0.5).astype(int)

    def score(self, X, y):
        return accuracy_score(y, self.predict(X))


for alpha in (1, 0.1, 0.01):
    np.random.seed(1)
    print('# alpha: %s' % str(alpha))
    N = 1000
    X = np.random.random((N, 10))
    y = np.r_[np.zeros(N//2, int), np.ones(N//2, int)]
    X[y == 1] = X[y == 1]*alpha
    Xtr, Xts, ytr, yts = train_test_split(X, y)

    print('## sklearn forest')
    for n_estimators in (1, 10, 100, 200, 500):
        m = RandomForestClassifier(
            n_estimators, max_features=None, bootstrap=False)
        m.fit(Xtr, ytr)
        print('%3d: %.4f' % (n_estimators, m.score(Xts, yts)))

    print('## my forest')
    for n_estimators in (1, 10, 100, 200, 500):
        m = MyRandomForestClassifier(n_estimators)
        m.fit(Xtr, ytr)
        print('%3d: %.4f' % (n_estimators, m.score(Xts, yts)))
    print()
```
