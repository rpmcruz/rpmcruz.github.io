---
layout: post
title: "Regression + data augmentation = makes sense?"
category: machine learning
---

Data augmentation is a popular technique when working with images. Since the number of images is limited, we often create new images by slightly rotating, deforming, changing color, etc of existing images.

<img src="/img/2018-05/cat.jpg"> <img src="/img/2018-05/cat.jpg" style="transform: scaleX(-1)">

For example: A cat is still a cat if you flip the photo.

This is considered a regularization technique because it avoids the neural network to find patterns that are not there, such as thinking that cats are not symmetric in this case.

Does something like this make sense for classical classification, multi-label or regression problems?

## Experiment

Here we will explore two techniques:

* **[SMOTE](https://stats.stackexchange.com/questions/215938/generate-synthetic-data-to-match-sample-data)** which is a common technique to increase data for classification problems. Data is augmented by creating new observations for one class, based on the nearest neighbors. The motivation for this algorithm is to fix *class imbalance*, not to improve performance like I am querying here. (Class imbalance is when you have too many observations of one class, and too little of another class. One common technique is to oversample from the minority class so that it is not domintated by the majority class.)
* Dumb **Gaussian noise**: I am going to do something like this: `_X = X.copy(); for i in range(10): _X = np.r_[_X, X + np.random.randn(*X.shape)*0.5]`.

This is the summary of my experiment:

* The dataset I used was the [Boston dataset](http://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_boston.html), with **506 observations**.
* Furthermore, I did **25-75 train-test** partitions of the data. In other words, I reduced the training set to less than 130 observations. I really wanted my neural network to overfit (memorize) the data!
* I did **50 repetitions** and averaged the results (using MAE as the metric). I did this to avoid having the results contaminated by the train-test partition or by the stochastic nature of gradient descent.
* My neural network has an architecture **13-60-60-60-1**.

## Results

[SMOTE](https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume16/chawla02a-html/node6.html) was used to artificially increasing data by **0, 100, 500, 1000 and 5000 and 10,000 observations**. I have used [kNN](http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsRegressor.html) with k=10 and (i) knn without no weights (first column), (ii) knn weighted by inverse distance (second column).

| Extra data (absolute)    | Without weights | inverse distance weights |
| ------------- | --------------- | ------------------------ |
| 0 (no SMOTE)  | 3.31            | 3.31 |
| 100           | 3.48            | 3.20 |
| 500           | 3.72            | 3.23 |
| 1,000         | 3.88            | 3.24 |
| 5,000         | 4.14            | 3.25 |
| 10,000        | 4.17            | 3.30 |

I also tried data augmentation by increasing data by **200%**, where this extra data had random **Gaussian noise** with differing *sigma* values. As I increased this noise, the more the error was reduced. This was really odd, I cannot explain it.

| Sigma         | MAE             |
| ------------- | --------------- |
| 0 (original)  | 3.15            |
| 1             | 3.19            |
| 2             | 3.19            |
| 4             | 3.08            |
| 8             | 2.96            |
| 50            | 2.84            |
| 500           | 2.90            |

I also added **L2 regularization** just to check what the impact was, because what I think is going on is that all of these are just adding regularization, forcing the neural network to produce a more smooth output. Unsurprisingly, regularization helps, and it helps quite a bit.

| L2            | MAE             |
| ------------- | --------------- |
| 0 (none)      | 3.33            |
| 1e-06         | 3.32            |
| 1e-05         | 3.27            |
| 0.0001        | 3.33            |
| 0.001         | 3.29            |
| 0.01          | 3.22            |
| 0.1           | 3.18            |
| 1.0           | 2.98            |
| 10.0          | 3.74            |

## Summary

I am not completely sure what to think of these results. SMOTE seems to have helped very slightly (when knn was used with inverse distance weighting). Weirdly enough, Gaussian noise seems to have helped a lot, and was very insensitive to sigma.

Surely someone has already looked into this, but I have never seen this discussed.

## Appendix

This is the code I have used:

```python
# allow GPU memory growth
import tensorflow as tf
import keras.backend as K
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
K.set_session(tf.Session(config=config))

from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from keras import models, layers, regularizers
import numpy as np
import sys

MODE = sys.argv[1]
SMOTE_K = 10
EPOCHS = 1000
REPS = 50

def smote(X, y, n, k):
    if n == 0:
        return X, y
    knn = KNeighborsRegressor(k, 'distance').fit(X, y)

    # choose random neighbors of random points
    ix = np.random.choice(len(X), n)
    nn = knn.kneighbors(X[ix], return_distance=False)
    newY = knn.predict(X[ix])
    nni = np.random.choice(k, n)
    ix2 = np.array([n[i] for n, i in zip(nn, nni)])

    # synthetically generate mid-point between each point and a neighbor
    dif = X[ix] - X[ix2]
    gap = np.random.rand(n, 1)
    newX = X[ix] + dif*gap
    return np.r_[X, newX], np.r_[y, newY]

def noise(X, y, n, sigma):
    _X = X.copy()
    _y = y.copy()
    for _ in range(n):
        X = np.r_[X, _X + np.random.randn(*_X.shape)*sigma]
        y = np.r_[y, _y]
    return X, y

def create_model(l2):
    reg = regularizers.l2(l2)
    x = input_layer = layers.Input([13])
    x = layers.Dense(60, activation='relu', kernel_regularizer=reg)(x)
    x = layers.Dense(60, activation='relu', kernel_regularizer=reg)(x)
    x = layers.Dense(60, activation='relu', kernel_regularizer=reg)(x)
    x = layers.Dense(1)(x)
    model = models.Model(input_layer, x)
    model.compile('adadelta', 'mean_squared_error', ['mean_absolute_error'])
    return model

print('=============', MODE, '=============')
X, y = load_boston(True)
X = (X - X.mean(0)) / X.std(0)
print('data:', X.shape)

if MODE == 'smote':
    params = [0, 100, 500, 1000, 5000, 10000]
elif MODE == 'noise':
    params = [0, 1, 2, 4, 8, 50, 500]
elif MODE == 'l2':
    params = [0, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.1, 1., 10.]

results = {}
for param in params:
    results[param] = 0

for rep in range(REPS):
    print('* Repetition:', rep)
    Xtr, Xts, ytr, yts = train_test_split(X, y, test_size=0.75)
    for param in params:
        print('** param:', param)
        if MODE == 'smote':
            _Xtr, _ytr = smote(Xtr, ytr, param, SMOTE_K)
            m = create_model(0)
        elif MODE == 'noise':
            _Xtr, _ytr = noise(Xtr, ytr, 2, param)
            m = create_model(0)
        else:
            _Xtr, _ytr = Xtr, ytr
            m = create_model(param)
        m.fit(_Xtr, _ytr, 256, EPOCHS, 0)
        _, mae = m.evaluate(Xts, yts)
        print(param, mae)
        results[param] += mae / REPS

print('Average Results (%d repetitions):' % REPS)
print(results)
```
