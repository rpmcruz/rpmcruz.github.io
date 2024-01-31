import yaml
import json
from datetime import datetime
from crossref.restful import Works

publications = yaml.load(open('publications.yaml'), Loader=yaml.SafeLoader)

print('''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Ricardo Cruz</title>
<style>
.container { max-width: 800px; margin: 0 auto; }
p.description {text-align: justify;}
table { width: 100%; }
a.filter {color: black; text-decoration: none; border: 2px solid gray; border-radius: 5px; padding: 5px; display: inline-block;}
a.filter:hover {background-color: lightgray;}
a.filter.active {background-color: lightgray;}
a.filter.active:hover {background-color: gray;}
#topic_description {background-color: lightgray;}
</style>
</head>
<body>
<div class="container">
<h1>Ricardo Cruz, PhD</h1>
<p><a href="mailto:rpcruz@fe.up.pt">rpcruz@fe.up.pt</a></p>
''')

print(f'<p class="description">{publications["description"]}</p>')

topics = set()
filters = set()
listing = []

works = Works()
for doi, topic in publications['papers'].items():
    info = works.doi(doi)
    where = info['publisher'] + ' ' + ' - '.join(info['container-title'])
    topics.add(topic)
    listing.append({
        'year': info['published']['date-parts'][0][0],
        'title': info['title'][0],
        'authors': ', '.join('<b>R. Cruz</b>' if author.get('ORCID', '') == 'http://orcid.org/0000-0002-5189-6228' or author['given'][0] + author['family'] == 'RCruz' else f'{author["given"][0]}. {author["family"]}' for author in info['author']),
        'url': info['URL'],
        'type': info['type'],
        'topic': topic,
        'citations': info['is-referenced-by-count'],
        'where': where,
        'sjr-rank': ''.join(_rank for _where, _rank in publications['sjr-ranks'].items() if _where in where),
        'core-rank': ''.join(_rank for _where, _rank in publications['core-ranks'].items() if _where in where),
    })

h_index = sum(i+1 <= paper['citations'] for i, paper in enumerate(sorted(listing, key=lambda x: x['citations'], reverse=True)))
print(f'<p>My cross-ref h-index: {h_index}</p>')

print('<p><b>Topics:</b>')
for topic in topics:
    print(f'<a class="filter" id="{topic}" href="#" onclick="toggleTopic(\'{topic}\')">{topic}</a>')
print('</p>')

print('<p class="description" id="topic_description" style="display: none"></p>')

print('''</div>
<table id="table" border="1">
<thead>
<tr><th><a href="#" onclick="sort('year', 'desc', 'int')">Year</a></th><th>Paper</th><th>Info</th><th><a href="#" onclick="sort('citations', 'desc', 'int')">Citations</a></th><th><a href="#" onclick="sort('sjr-rank', 'asc', 'str')">SJR Rank</a></th><th><a href="#" onclick="sort('core-rank', 'asc', 'str')">CORE Rank</a></th></tr>
</thead>
<tbody></tbody>
</table>
<div class="container">
''')

print('<p><b>Filters:</b>')
for filter_key in ('type', 'sjr-rank', 'core-rank'):
  for filter_value in sorted(set(item[filter_key] for item in listing)):
      if filter_value:
        print(f'<a class="filter other" id="{filter_value}" href="#" onclick="toggleFilter(\'{filter_key}\', \'{filter_value}\')">{filter_value}</a>')
print('</p>')

print(f'<p>Last update: {datetime.now().strftime("%Y-%m-%d")}</p>')

print('<script src="table.js"></script>')
print('<script>')
print('createTable(\'table\', ' + json.dumps(listing) + ', ' + json.dumps(publications['topics']) + ');')
print('''</script>
</div>
</body>
</html>
''')
