---
layout: post
title: What is machine learning?
category: machine learning
---

This is a simple and general overview into machine learning to use as a pointer to tell people what machine learning is.

People like to put others into categories. André is an electrical engineer, Bianca is a pharmacist, et cetra. Funny enough, the very people whose job is to categorize things do not have a good category in which to put themselves. Are we computer scientists? Software engineers? Statiscians? There is a recent convergence towards "data scientist", but the term is a little odd to say. The discipline itself is known by many names: for a long time, it was known as "knowledge from databases", currently, it is mostly called either "data mining" or "machine learning".

It is not my attempt to enter this flamewar. Semantical wars are fun, but unproductive. You can easily google tons of flamewars between whether data mining is statistics, whether it is computer science, yadda, yadda, yadda. I will just say that I like the often-said expression: "a data scientist is someone who is a better programmer than a statistician, and a better statistician than a programmer."

## What problems does machine learning attack?

Usually, people categorize machine learning problems into the following:

1. regression: predict a *numerical* variable
2. classification: predict a *categorical* variable
3. clustering

**Regression** and **classification** try to find a model $f$ that describes the relationship between the target variable $y$ and the explainatory variables $x$, such that $y=f(x)$. For instance, find price\_of\_house=f(house\_topology, neighborhood\_crime, distance\_to\_metro).

There is some discussion between description and prediction. It is usually thought that there is a trade-off between model interpretability and model performance. Usually, simple models are easier to understand, but perform worse than more complex models. This will be made clear later.

**Clustering** is when you do not have a *target* variable. You just want to somehow create similar group. For instance, you want to cluster your customers into similar groups to study them.

Personally, I might also add:

4. reinforcement learning: these are techniques used when several steps are required to reach a reward; for instance, training a computer to play board games like Go, or computer games, or some such.
5. autoencoders / adverserial neural networks / art transfer: these are techniques used to predict the following frames in a video, or for such things as to [paint a photograph using von Gogh style.](https://github.com/jcjohnson/neural-style)

... but there are many others, and all these categorization is of course very contentious. People enjoy bickering against each other. For instance, some people say that ordinal variables (like student grades 1-20) are "ordinal regression" problems, others call it "ordinal classification."

## A few examples

These are a few pratical examples using [scikit-learn.](scikit-learn.org) This is a Python package originally funded by Google for machine learning. Next to R and its ecosystem, Python+scikit-learn is the widest deployed combo for machine learning.

Let us open a dataset:

```python
data = datasets.load_boston()
X, y = data['data'], data['target']
```

(Ubuntu Installation: install the `python3-sklearn` package. Or, if you want the latest version, install the `python3-pip` package and then type `pip3 install scikit-learn`. Windows and others: use [Anaconda](https://www.continuum.io/downloads), which is a Python scientific package that comes with these things.)

The [boston housing dataset](https://archive.ics.uci.edu/ml/datasets/Housing) was compiled in 1978 and contains house prices from suburbs around Boston (target variable), and a bunch of other variables like per capita crime rate in the town, property-tax, et cetra.

Usually, we call `X` to the explanatory variable, and it is a matrix where each variable is a column, and each observation is a row. And we usually use a different variable called `y` which is of course a vector with the value for each row. This common practise in scikit-learn, but R users usually use a single matrix for everything.

Anyhow, let's apply some models to this example!

### First, things first!

Let us split the data into two. Half of the data, we will use to build the model, and the other half to see how good our model is. Obviously, it would be cheating to see how good the model was using the data used to build it. The model could just memorize the data and have perfect score. We want to make sure our models is generalizing.

This is called hold-out validation. One problem with this method of validation is that the split is incredibly random. There are more sophisticated methods of validation, known as *cross-validation.* But this is simple enough for what we want:

```python
from sklearn.model_selection import train_test_split
Xtr, Xts, ytr, yts = train_test_split(X, y, train_size=0.5)
```

`Xtr` and `ytr` are used to _train_ the model. `Xts` and `yts` are used to _test_ the model.

Note: I have decided to remove model selection from the last draft of this description on machine learning. I think it would be unfair to say one method is better or worse for this dataset, especially because the dataset is very simple, and small variations in performance are probably caused by something else, namely validation luck.

Instead, I have focused on data visualization while describing the models. We are going to try to explain average house price in the town using the number of the average rooms in that town as the explanatory variable:

```python
import matplotlib.pyplot as plt
i = 5
x = X[:, [i]]
plt.plot(x, y, '.')
plt.xlabel(data['feature_names'][i])
plt.ylabel('Price')
plt.title(data['DESCR'].splitlines()[0])
plt.show()
```

![Data visualization](/img/2017-02/data.png)

### Linear Regression

We have to start with the mandatory **linear regression.**

The model here is a simple line: $price = w_0 + w_1*crime + w_2*taxes + ...$.

The difficulty of this model is finding the weights *w* which are multiplied by the variables. The way this is done is by minimizing the sum of the differences between the true prices and the prices predicted by the model for all observations in the training set, i.e.: minimize $\sum_i |price_i - w_0 - w_1*crime_i - w_2*taxes_i|$. To make it easier, norm-L2 is used; that is, we minimize the sum of the square errors: $\sum_i (price_i - w_0 - w_1*crime_i - w_2*taxes_i)^2$.

Square error is easier because we can have a system of equations based on the derivatives of X relative to each $w$. Then, we solve for $w$, which is very easy because we have now a system of linear equations, which can be solved using matrix inversion, i.e. $AX=B$ can be solved for $A$ via $A=BX^{-1}$.

In actually, even [simpler methods](https://en.wikipedia.org/wiki/Simple_linear_regression) exist. For more complicated cases, such as logistic regressions or [artificial neural networks](/machine%20learning/2017/01/25/deep-learning.html), which involve non-linear transformations of the weights, then something like gradient descent has to be used. It is an iterative method, where we perform small steps in the direction of the derivative.

```python
from sklearn.neighbors import KNeighborsRegressor
import matplotlib.pyplot as plt
import numpy as np
X, y = data['data'], data['target']
i = 5
x = X[:, [i]]
plt.clf()
plt.plot(x, y, '.')
xx = np.arange(x.min(), x.max(), 0.01)
for k in [5, 50]:
    print(k)
    m = KNeighborsRegressor(k).fit(x, y)
    plt.plot(xx, m.predict(xx[:, np.newaxis]), label='k=%d' % k)
plt.xlabel(data['feature_names'][i])
plt.ylabel('Price')
plt.title(data['DESCR'].splitlines()[0])
plt.legend()
plt.show()
```

![Linear regression example](/img/2017-02/linear.png)

Two points:
* I have used $w$ as the coefficients, but usually beta $\beta$ is used in the literature. This is for historical reasons. Linear regressions are very old models inventented by statistician. Computer science types, however, tend to call "weights" to the coefficients.
* From the point of view of the optimization problem, the coefficients are the X variables. These are the variables that do not change. Therefore, the regression is a linear equation relative to $w$, but not relative to $X$. You can have models such as: $y=w_1*x_1^2+w_2*x_1*x_2$, etc... These transformations of variables are very important to get good results using these models, and this is where data visualization and expert knowledge comes into play.

### k Nearest Neighbors

Let us start with **k Nearest Neighbors (kNN)**. In this model, if we want to discover the price of the house for explanatory variables $X$, we compute the distance between $X$ and all training variables. Then, we output the average price of the closest $k$ neighbors.

I think kNN can be seen as a kind of [moving average](https://en.wikipedia.org/wiki/Moving_average) when used with real numbers as explanatory variables. Of course, it has the advantage that the explanatory variable could be a class: e.g.: 0, 1, 2.

This model is fast to train, but slower to evaluate. You can either do it the dumb way and store all training examples and then use a distance matrix against all new observations. Or be smart about it and use data structures such as [K-D Trees.](https://en.wikipedia.org/wiki/K-d_tree)

This is not a very interpretable model, as far as I know. But it has been shown that with infinite examples, 1-NN provably has error that is at most twice Bayes optimal error. (Whatever that means :))

This code procudes a kNN for different values of $k$. This is the number of neighbors used. The average price is computed from these closest neighbors.

```python
from sklearn.neighbors import KNeighborsRegressor
import matplotlib.pyplot as plt
import numpy as np
X, y = data['data'], data['target']
i = 5
x = X[:, [i]]
plt.clf()
plt.plot(x, y, '.')
xx = np.arange(x.min(), x.max(), 0.01)
for k in [5, 50]:
    print(k)
    m = KNeighborsRegressor(k).fit(x, y)
    plt.plot(xx, m.predict(xx[:, np.newaxis]), label='k=%d' % k)
plt.xlabel(data['feature_names'][i])
plt.ylabel('Price')
plt.title(data['DESCR'].splitlines()[0])
plt.legend()
plt.show()
```

![kNN example](/img/2017-02/knn.png)

### Decision Trees

Decision trees test all combinations of rules of the type $X_i > v$. It requires testing all these combinations. Or actually not. A trick often employed is the fact that if the metric function is monotonous, then you can employ more intelligent tactics.

They perform local one-look-ahead optimizations only. Therefore, you can improve the model performance by keeping in mind how the model works, and build interactions or simplifying variables. For instance, you might want to use "is-weekend=True/False", rather than weekday=1,2...7.

This is a decision tree build by allowing them to grow until max_depth=2 (pruned), and until each node has only one observation (unpruned).

```python
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
import numpy as np
from sklearn.tree import export_graphviz
import os
X, y = data['data'], data['target']
i = 5
x = X[:, [i]]
plt.clf()
plt.plot(x, y, '.')
xx = np.arange(x.min(), x.max(), 0.01)
for max_depth in [None, 2]:
    m = DecisionTreeRegressor(max_depth=max_depth).fit(x, y)
    max_depth_str = str(max_depth) if max_depth else 'all'
    label = 'max_depth=' + max_depth_str
    plt.plot(xx, m.predict(xx[:, np.newaxis]), label=label)
    filename = 'tree-%s.dot' % max_depth_str
    export_graphviz(
        m, filename, 3, [data['feature_names'][i]], label='none',
        impurity=False, node_ids=False)
    os.system('dot -Tpng %s -o img/tree-%s.png' % (filename, max_depth_str))
plt.xlabel(data['feature_names'][i])
plt.ylabel('Price')
plt.title(data['DESCR'].splitlines()[0])
plt.legend()
plt.show()
```

![Decision tree example](/img/2017-02/tree.png)

Small trees can be interpreted very nicely:

![Decision tree diagram depth=2](/img/2017-02/tree-2.png)


However, as they get very big, they become awful to interpret:

![Decision tree diagram with much depth](/img/2017-02/tree-all.png)

Some attempts exist at combining decision trees to build interactions between variables, and then linear regressions at the nodes. These models are known as [MARS.](https://en.wikipedia.org/wiki/Multivariate_adaptive_regression_splines)

However, they are not used much. I suspect it is because they are slow and do not perform as well as expected. They overfit easily. I also suspect it is because better models exist: random forests, which are collections of many decision trees.

Two errors exist in data mining: bias or underfitting (when the average model you build is off), and variance or overfitting (when the average model you build is correct, but each model you build is incorrect in different directions). You can fix variance using random forests: you build many decision trees and then average them out. This family of techniques are called bagging.

You can fix both bias and variance using more sophisticated ensembles such as adaboost or gradient boosting trees, where you train each decision trees by telling them to give more weight to the observations missclassified by the previous tree. This family of techniques are called bagging.

One problem often neglected is that decision trees perform only one-look-ahead optimization. Therefore, it is important to manually build feature interactions. For instance, combine weekday=monday and holiday=true into a single variable.

## Conclusion

Some models are faster to train. Some models are faster to evaluate. Some models have better performance. Some models are more interpretable. And, of course, all this is also relative to the data in question.

Here three models were presented: linear regression, k nearest neighbors, and decision trees.

Data scientists in general do not build their own models. However, a lot of programming is involved and knowing the intrinsics of each model is very helpful as well, and they do not like being called statiscians either.
