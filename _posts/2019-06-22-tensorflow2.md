---
layout: post
title: Deep learning frameworks
category: machine learning
---

{% raw  %}
A breath of fresh as TensorFlow is about to debut its 2.0 version. I take the opportunity to do a small comparison between TensorFlow v1, PyTorch and TensorFlow v2.

Let us say we want to calculate the derivative of $$f(x)=x^2$$ when $$x=5$$.

**TensorFlow v1**

Like Theano before it, TensorFlow separated the symbolic algebraic part from the numerical part:

```python
# symbolic part
x = tf.placeholder((), tf.float32)
f = x**2
df = tf.gradients(f, x)[0]

# numerical part
session = tf.Session()
session.run(tf.initializers.global_variables())
result = session.run(df, {x: 5})
```

Many people complained because if you wanted control flow operators (say you want to define a function by parts), you would need to define it symbolically using functions such as `tf.cond` and `tf.greater`. Since functions were not "defined-by-run", but rather "define-and-run", you could not use Python control flow operators like "while" and "if" in things like loss functions.

**PyTorch**

PyTorch uses a more paradigm-like way of programming which most people are better familar with. It is a defined-by-run package where things are executed as you type them. It makes it nicer to do control flow and for debugging problems with the code.

```python
x = torch.tensor(5., requires_grad=True)
f = x**2  # forward-pass
f.backward()
result = x.grad
```

Defining neural networks in PyTorch can be done by sub-classing the `nn.module` and defining layers as variables within the instances of the class:

```python
class MyModel(nn.Module):
    def __init__(self):
        self.camada1 = nn.Dense(50)
        self.camada1 = nn.Dense(10)

    def fpass(self, x):
        x = self.camada1(x)
        x = self.camada2(x)
        return x
```

**TensorFlow v2.0**

While TensorFlow already allowed the executation of defined-by-run code (also known as its "eager executation" mode), it was only in 2.0 that it has been enabled by default.

The previous operation can now be run by doing:

```
x = tf.convert_to_tensor(5.)
with tf.GradientTape() as tape:
    tape.watch(x)
    f = x**2
result = tape.gradient(f, x)
```

I think where TensorFlow 2.0 shines is in creating models, where it has integrated the user-friendly Keras library:

```python
x = input_layer = tf.keras.layers.Input((100,))
x = tf.keras.layers.Dense(50)(x) 
x = tf.keras.layers.Dense(10)(x) 
model = tf.keras.models.Model(input_layer, x)
```

A `model` can then be instantiated by giving it a tensor. For example, to make predictions, I just need to do `Y_hat = model(X)` and I got my predictions `Y_hat`. I can then do a backward pass by saving its gradients:

```python
with tf.GradientTape() as tape:
    Y_hat = model(X, training=True)  # forward-pass
    loss = mean_squared_error(Y, Y_hat)
g = tape.gradient(loss, model.trainable_weights)  # backward-pass
```

Then an optimizer could be used to updated the model's trainable weights.

It would be a good idea to place this inside a function and use the new decorator `tf.function`. This automagically translates the operations into a graph that is fast to run. In my experience, I have not suffered a speed decrease when porting code to 2.0 if I use this decorator for the training step.

{% endraw  %}
