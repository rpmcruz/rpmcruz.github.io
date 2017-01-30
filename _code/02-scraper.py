from lxml import html
import urllib.request
import pandas as pd
import numpy as np

df = pd.DataFrame(columns=('car', 'price'))

for page in range(1, 10+1):  # keep running until no "next" pages or maximum
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

ax = df.groupby('car').mean().sort_values('price').plot(kind='bar', color='white')
fig = ax.get_figure()
fig.savefig('plot.png')
