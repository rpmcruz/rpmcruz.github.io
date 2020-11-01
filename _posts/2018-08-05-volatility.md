---
layout: post
title: Statisticians fooled by statistics
category: machine learning
---

Statistics are [known to lie](http://www.tylervigen.com/spurious-correlations). Even experts can be misled by statistics. For example, it is well-known that early diagnosis increases cancer survival rate, right? Actually, [a medical study](https://www.ncbi.nlm.nih.gov/pubmed/10865276) has found that the numbers have been inflated by not thinking carefully about statistics.

Usually, doctors use the percentage of people who have survived after 5-years since the time of the diagnosis. Therefore, early diagnosis looks good even if a cancer kills 100% of the patients because the early diagnosis patients are more likely to be alive after 5-years than those that were diagnosed later, whether the treatment was effective or not, simply because of statistics. This does not mean that early diagnosis is not important. Just to say that the effectiveness numbers have been highly overinflated because people did not think carefully about statistics.

Now, these people were doctors. What about statisticians? Can statisticians be fooled by statistics?

One very common error I see my colleagues making all the time is the following. I have seen people making this error even when they have a statistics background.

Consider these two graphics:

![Figure 1](/imgs/blog/2018-08/y1.png)

![Figure 2](/imgs/blog/2018-08/y2.png)

The first one is more volatile than the second, right?

Actually, the same series is represented in both graphics:

```python
import numpy as np
y = np.random.randn(n)
```

I just added a little trend to the second plot:

```python
trend = np.arange(n)
y += trend
```

I think the term *volatility* should be excised from statistics because of how subjective it is. It is very dependent on how you frame things.

For example, the stock market is *very* volatile if you want to buy a stock today and sell tomorrow, because the trend is not well defined.

But if you buy a stock to sell in five years, then the stock markets all the sudden looks pretty well behaved, because there is a trend. For example, consider the [S&P 500 index](https://www.google.com/search?tbm=fin&q=INDEXCBOE:+.INX&stick=H4sIAAAAAAAAAONgecRowi3w8sc9YSntSWtOXmNU5eIKzsgvd80rySypFBLnYoOyeKW4uTj1c_UNDM0qi4t5AEZhN345AAAA&sa=X&ved=0ahUKEwiA6tHpg9bcAhVIzoUKHSOeCxsQ0uIBCGgwBA&biw=1865&bih=990#scso=uid_XP1mW4rfEOmNlwT-nI-ADg_5:0):

![Stock market](/imgs/blog/2018-08/stock.png)

I think before looking at the data, we should define the range we use for the graphics. Otherwise, we are very prone to being fooled by data, especially when the series is stationary.
