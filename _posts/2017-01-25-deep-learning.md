---
layout: post
title: Is deep learning a buzz-word?
category: machine learning
---

What is deep learning?

Deep learning are artificial neural networks, which go as far back as 1958 with the conceptualization of a computer-programmed perceptron by Frank Rosenblatt, an American psychologist. But they were only made popular with the advent of the backpropagation algorithm in 1986 (which was the re-inventation of an algorithm from 1975).

## What are artificial neural networks?

Artificial neural networks are logistic regressions on steroids. A logistic regression is of the form $$y=f(w_0+w_1x_1+w_2+x_2)$$, where $$y$$ is the variable we want to predict and $$x$$ are the exogenous variables. $$f$$ is a non-linear function that maps a real value into a probability [0,1]. This family of functions are known as [sigmoid functions](https://en.wikipedia.org/wiki/Sigmoid_function), and usually the [logistic function](https://en.wikipedia.org/wiki/Logistic_function) is the one used.

Example of a logistic regression. Let's say we want to predict if someone will buy an house. We can write an equation of the form:

P(Will_Buy_House | Monthly_Income, Number_Rooms) = f(-10 + 0.01\*Monthly_Income + 1\*Number_Rooms)

(P(Will_Buy_House | Monthly_Income, Number_Rooms) means the probability of someone buying a house given their monthly income and the number of rooms of the house.)

Two people come into the real estate office. These are the probabilities they will buy the house:

P(Will_Buy_House | Monthly_Income=600, Number_Rooms=2) = 0.12

P(Will_Buy_House | Monthly_Income=1000, Number_Rooms=2) = 0.88

The tricky part here is finding the coefficients to multiply the variables. These are also known as weights.

We will answer that in the following section (in very broad strokes). Back to the question: neural networks are logistic regressions on steroids. Instead of $$P=f(w*x)$$, you do $$P=f(w_1*f(w_2*x))$$. The number of times you transform your data is known as layers. In the most typical case, a single hidden layer is used. Furthermore, several intermediate variables are created as well, so that in the end you have $$P=f(w_1*f(w_2*x)+w_3*f(w_4,x)+w_5*f(w_6*x))$$.

This is usually expressed in a diagram of the form:

![nnet](/img/2017-01-25/03-nnet.jpeg)

(This image is diagram that everybody copies around. It's impossible to say who created this image at this point hehe.)

## Backpropagation

How you do find the weights $$w$$?

Usually you try to minimize some error function: $$\sum |y - f(x)|$$, where $$y$$ are the values from our sample. In other words, we need to have a big real-world sample to compare our model against and fix it. Often, we use squared error because it is easy to create the derivative: $$\sum (y - f(x))^2$$.

To find weights, simply find when the derivative of the error function relative to the weights is zero. This is high school mathematics. (The derivative is the velocity of the function, and the function will reach a peak when the velocity goes from positive to negative, or vice-versa, i.e. it is zero.)

But the sigmoid function $$f$$ makes that impossible because the value of each weight will depend on the other weights. Instead, what we do is to use the derivative relative to each weight to change each weight a little bit in the direction of the zero.

## Deep learning

So, deep learning is just neural networks.

Yes and no.

Yes: well, yes.

No: the reason why the buzzword was created was because until recently backpropagation suffered from the vanishing gradient problem.

Deep learning was possible when the vanishing gradient problem was finally conquered.

What is the vanishing gradient problem?

The sigmoid function can saturate. Let's look at the logistic function (green) and its derivative (blue):

![sigmoid](/img/2017-01-25/03-sigmoid.png)

Why is this a problem? Consider the situation when $w*x=1000$. Then, $$f(1000)=0.9999999$$. The derivative? $$f'(1000)=0.00000001$$.

The process of finding the weights does not work for part of the value space. This can be mitigated by normalizing the data for single hidden-layer neural networks. But if you have multiple layers, then the derivative gets smaller and smaller as you increase your neural networks.

(Side-note: Interestingly, there is a little known algorithm called [resilient backpropagation](https://en.wikipedia.org/wiki/Rprop) which does not suffer from this problem. The reason is because it uses the sign of the gradient, not its magnitude, when changing the weights in the direction of whatever minimizes your error. This is the default algorithm for the neuralnet package in R, by the way. On the other hand, the algorithms uses if-elses instead of vector multiplications, which makes it very slow.)

This was overcome by deep learning! Well, actually, not. In the beggining of the 2010s, Google and others invested things like ReLU functions which replaced the logistic function. ReLU is of the form $$f(x)=max(0,x)$$, so its derivative is either 0 or 1. Several other approaches, combined with faster computers, have mitigated the vanishing gradient problem. It was never fixed completely.

Deep learning is the result of this revolution: very large and complex topologies of artificial neural networks.

# Where is deep learning being used

I will take one example only here: image recognition.

Traditionally, in image recognition, you'd build several variables from the image: the entropy across the image, the types of edges in the image, etc. Then, you'd build a model to predict whether your image was, say, a bird based on these features that you have manually extracted from the image.

With things like convolutional neural networks no such pre-processing is required. These neural networks have nodes spread-out across the image which are then connected to the neighbor nodes, and so on, across many layers. This system was invented by LeCun, and is inspired from the animal neural-vision system.

Many other such systems exist, though convolutional neural networks are probably the most used commercially. For instance, self-driving cars use them.
