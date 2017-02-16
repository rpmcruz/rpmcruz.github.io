---
layout: post
title: My machine learning implementations
category: machine learning
---

I have [a github repository](https://github.com/rpmcruz/machine-learning) where I have been keeping machine learning I have implemented. These are not "inventions" of mine, but merely implementations of algorithms in the literature that are either not implemented in Python, or of which I required my own implementation so that I could build upon them.

I am still unsure about how to structure the repository, but these was how it actually looks:

- preprocessing
- classification
- ranking
- quantile

## Preprocessing

- **smote:** [SMOTE](https://www.jair.org/media/953/live-953-2037-jair.pdf) is a famous oversampling technique that generates new synthetic samples when you have too few observations of one class; I have implemented SMOTE and the MSMOTE variation
- **metacost:** this is a clever method by [Pedro Domingos](https://homes.cs.washington.edu/~pedrod/) to add costs support to a classifier by changing the classes

## Classification

I work mostly on classification, but most of these could be adapted for regression problems as well.

Here I have:

- **bagging:** a random forest implementation only
- **boosting:** a AdaBoost, and a gradient boosting implementation (with a couple of different loss functions for the latter)
- **extreme-learning:** [extreme machine learning](https://en.wikipedia.org/wiki/Extreme_learning_machine) model
- **multiclass:** one-vs-all and multiordinal ensembles, which turn binary classifiers into multiclass models
- **neuralnet:** here I have a simple neural network implemented in pure Python and in C++ with Python-bindings, implemented both with batch and online iteration

## Ranking

Ranking are models used to produce a ranking list, for instance in searches.

The models I have implemented are called "pairwise scoring rankers" which are trained in pairs, but can produce a ranking scoring for each individual observation. This ranking score is only meaningful when compared to the score of another observation.

- **GBRank:** adapation of gradient boosting for ranking
- **RankBoost:** adapation of AdaBoost for ranking
- **RankNet:** adapation of a neural network for ranking (I have also a C++ implementation in the classification folder)
- **RankSVM:** adapation of SVM with linear kernel for ranking

## Quantile

These are models which, instead of predict the average expected value, they produce the expected value for a given quantile. For instance, what the median prediction is, or what the lowest-10% value you can expect, et cetra.

I have here classification and regression models:

- **QBag:** simple bagging adapation for quantiles
- **QBC** and **QBR:** gradient boosting adapations for quantiles

And that's it!

-----------------

I meant to have some test files to unit-test the various algorithms. But I will probably never have the time to get around to do that. :) Please let me know if you use any, and whether you had problems using it.

- Also, see [my other github stuff.](https://github.com/rpmcruz?tab=repositories)
