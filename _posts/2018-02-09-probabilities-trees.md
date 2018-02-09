---
layout: post
title: "Don't use decision trees for probabilities"
category: machine learning
---

Today I received an email about an answer [I posted over datascience.stackexchange](https://datascience.stackexchange.com/questions/11171/decision-tree-how-to-understand-or-calculate-the-probability-confidence-of-pred). How to compute probabilities using a Decision Tree classifier?

You cannot. Let me be even clearer: you **absolutely** cannot.

**A** decision tree is great for graphical interpretability, but it is also very misleading. The problem is that the model can be incredibly unstable. If you perturb the data a little bit, you might get a completely different tree. C4.5 decision trees were voted identified as one of the top 10 best data mining algorithms by the [IEEE International Conference on Data Mining (ICDM) from 2006](http://www.cs.umd.edu/~samir/498/10Algorithms-08.pdf), but even them remarked that:

> It is well known that the error rate of a tree on the cases from which it was constructed (the resubstitution error rate) is much lower than the error rate on unseen cases (the predictive error rate). For example, on a well-known letter recognition dataset with 20,000 cases, the resubstitution error rate for C4.5 is 4%, but the error rate from a leave-one-out (20,000-fold) cross-validation is 11.7%. As this demonstrates, leaving out a single case from 20,000 often affects the tree that is constructed!

But scikit-learn's [Decision Tree implementation](http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html) has a **predict_proba()** that generates probabilities... surely I can use it?

Well, let's give it a try to see how well it works...

First, let's use the iris dataset:

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
X, y = load_iris(True)
Xtr, Xts, ytr, yts = train_test_split(X, y, stratify=y)
```

Let's train it:
```python
from sklearn.tree import DecisionTreeClassifier
m = DecisionTreeClassifier().fit(Xtr, ytr)
```

Let's look at the probabilities it generates for class 0:

```python
print(m.predict_proba(Xts[yts == 0]))
```

```
[[ 1.  0.  0.]
 [ 1.  0.  0.]
 [ 1.  0.  0.]
 [ 1.  0.  0.]
 ...
```

Let's look at the probabilities it generates for class 1:

```python
print(m.predict_proba(Xts[yts == 1]))
```

```
[[ 0.  1.  0.]
 [ 0.  1.  0.]
 [ 0.  1.  0.]
 [ 0.  1.  0.]
 ...
```

Let's look at the probabilities it generates for class 2:

```python
print(m.predict_proba(Xts[yts == 2]))
```

```
[[ 0.  0.  1.]
 [ 0.  0.  1.]
 [ 0.  0.  1.]
 [ 0.  0.  1.]
 ...
```

As the documentation says, the way it generates probabilities is the number of samples of a given class $$k$$ on a given leaf $$\ell$$, $$n_k^{(\ell)}$$, over the number of samples in that leaf $$n^{(\ell)}$$: $$P(y=k|X)=\frac{n_k^{(\ell)}}{n^{(\ell)}}$$.

```python
from sklearn.tree import export_graphviz
import os
export_graphviz(m, 'tree-full.dot', label='none', impurity=False, rotate=True, leaves_parallel=True)
os.system('dot -Tpng tree-full.dot -o tree-full.png')
```

![Decision tree fully trained](/img/2018-02/tree-full.png)

(In blue, it's the probabilities generated written by me.) 

If you want something resembling probabilities, you have to truncate the tree. For example, limit the depth of the tree.

```python
from sklearn.tree import DecisionTreeClassifier
m = DecisionTreeClassifier(max_depth=1).fit(Xtr, ytr)
```

This will get you something like this:

```python
from sklearn.tree import export_graphviz
import os
export_graphviz(m, 'tree-full.dot', label='none', impurity=False, rotate=True, leaves_parallel=True)
os.system('dot -Tpng tree-full.dot -o tree-full.png')
```

![Truncated decision tree](/img/2018-02/tree-truncated.png)

It's still rather awful. All observations within the same node will have the same probabilities.

## Random Forest to the rescue

After all this bashing, let me you present you with the cure: Random Forest.

The idea of this model is very simple: you train a bunch of trees (the more, the merrier), and then they all vote on the final classification. Each decision tree (in the forest) is trained in resamples of the data (hence the *Random* in Random Forest) -- otherwise, all trees would look the same. I have a simple implementation of a Random Forest in my [machine learning repository](https://rpmcruz.github.io/machine%20learning/2017/02/17/my-implementations.html).

If you train a decision tree and a random forest, and the probabilities are similar, then go ahead and use the decision tree. I do think that's unlikely (if not outright impossible) because either (a) the data is easily seperable (and probabilities are uninformative: 0 or 1), or (b) the data isn't easily seperable and the decision tree will be highly unstable.

The problem with the Random Forest is that it's not easily interpretable. But the probabilities are more reliable. Even so, [scikit-learn documentations warns](http://scikit-learn.org/stable/auto_examples/calibration/plot_compare_calibration.html):

> RandomForestClassifier shows the opposite behavior: the histograms show peaks at approx. 0.2 and 0.9 probability, while probabilities close to 0 or 1 are very rare.
