---
layout: post
title: Easy scraping
category: machine learning
---

I have to confess something. I am addicted. I am addicted to [stackexchange.com](stackexchange.com).

This is a family of websites of which [stackoverflow](http://stackoverflow.com/) is the most famous. From time to time, I go there to see what I can answer. I have made my fair share of questions as well!

I especially enjoy the Data Science section. You can see [my profile here.](http://datascience.stackexchange.com/users/16853/ricardo-cruz) I thought of starting to adapt some of my answers to this blog.

The first - since it was my most recent - is on *scraping.*

Scraping is to automatically extract information from a website.

Special and elaborate frameworks exist for that purpose. See e.g. [scrapy.](https://scrapy.org/)

Personally, I have find them overly-cumbersome when I tried using them. So, here is my suggestion.

Let us say we want to extract prices of cars from OLX. OLX is an international website where people post things to sell. I am going to use the Portuguese version here.

I am going to use XPath. XPath is an incredibly powerful notation of accessing XML nodes. Much more is possible than I am writing here. Take [this tutorial](http://www.w3schools.com/xml/xpath_intro.asp) to learn the full XPath syntax.

```python
from lxml import html
import urllib.request
import pandas as pd
import numpy as np

df = pd.DataFrame(columns=('car', 'price'))

for page in range(1, 10):  # keep running until no "next" pages or maximum
    url = 'https://www.olx.pt/carros-motos-e-barcos/carros/?page=%d' % page
    text = urllib.request.urlopen(url).read()
    tree = html.fromstring(text)
    table = tree.xpath('//table[@id="offers_table"]')[0]

    cars = table.xpath('//h3/following-sibling::p/small/text()')
    # remove spaces around the text
    cars = [car.strip()[9:] for car in cars]

    prices = table.xpath('//p[@class="price"]/strong/text()')
    # convert to int (remove thousand separator & etc)
    prices = [np.nan if price == 'Troca' else int(price[:-2].replace('.', ''))
              for price in prices]

    assert len(cars) == len(prices)
    df = df.append(pd.DataFrame({'car': cars, 'price': prices}))

    if not prices:
        break

df.groupby('car').mean().sort_values('price').plot(kind='bar')
```

And voila:

![Scraper result](/imgs/blog/2017-01-25/02-scraper.png)

I won't go line over line because the code is fairly straightforward. The code could be much simpler if the web design was simpler. I had to first go to the table I am interested, because OLX creates a promoted-ads table as well, and I don't want that table otherwise I would have duplicate information when going through the pages. I also have to do some gymnastics to reach the sibling of a node I was interested in because there was no way to refer to it directly.

Some web designers make your work easier or harder. Any modern browser like Chrome and Firefox can help you explore the DOM of any webpage. Just right-click and press Inspect or go to Developer Tools in the Tools menu or some such.

*Note:* some website like [scholar.google.com](https://scholar.google.pt/) disallow scrapers and are very good at detecting if that's what you're doing. You can specify an user-agent for urllib, but it might be futile. Even advanced frameworks may not be able to help you there.
