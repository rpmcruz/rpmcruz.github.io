import argparse
parser = argparse.ArgumentParser()
parser.add_argument('type', choices=['html', 'latex'])
args = parser.parse_args()

import functools
import sys
import time
import requests
from lxml import etree
from crossref.restful import Works

def conference_acronym(conference):
    known_conferences = {'IJCNN': None, 'Pattern Recognition and Image Analysis': 'IBPRIA',
        'Advances in Computational Intelligence': 'IWANN', 'PRNI': None, 'EMBC': None,
        'ICANN': None, 'ICPR': None, 'ICMV': None,
        'Progress in Pattern Recognition, Image Analysis, Computer Vision, and Applications': 'CIARP',
    }
    for name, acronym in known_conferences.items():
        if name in conference:
            return acronym if acronym else name
    raise Exception(f'Conference "{conference}" unknown.')

@functools.cache
def get_core_rank(acronym):
    response = requests.get(f'http://portal.core.edu.au/conf-ranks/?search={acronym}&by=acronym&source=all')
    response.raise_for_status()
    tree = etree.HTML(response.content)
    rank = tree.xpath('//table//tr[2]/td[4]/text()')
    return rank[0].strip() if len(rank) else ''

@functools.cache
def get_sjr_rank(journal_name, my_categories):
    # notice that since we are using functools.cache, then my_categories needs
    # to be an hashable type (such as a frozenset)
    name2id = {'Lecture Notes in Computer Science': 25674,
        'Pattern Analysis and Applications': 24822,
        'Computers & Electrical Engineering': 18159,
        'PeerJ Computer Science': 21100830173,
        'Mathematics': 21100830702, 'Sensors': 130124,
        'Intelligent Systems with Applications': 21101051831,
    }
    for name, id in name2id.items():
        if name in journal_name:
            break
    else:
        raise Exception(f'Journal "{journal_name}" unknown.')
    while True:
        try:
            response = requests.get(f'https://www.scimagojr.com/journalsearch.php?q={id}&tip=sid', timeout=5)
            response.raise_for_status()
            break
        except:
            print(f'Could not retrieve SJR page for journal {id}. Wait 1 second...', file=sys.stderr)
            time.sleep(1)
    tree = etree.HTML(response.content)
    tbody = tree.xpath('//div[@class="dashboard"]//table/tbody')[0]
    categories = tbody.xpath('./tr/td[1]/text()')
    years = tbody.xpath('./tr/td[2]/text()')
    quartiles = tbody.xpath('./tr/td[3]/text()')
    max_year = max(int(y) for y in years)
    return min(quartile for category, year, quartile in zip(categories, years, quartiles) if int(year) == max_year and category in my_categories)

def get_paper_info(doi, topic, my_categories):
    info = Works().doi(doi)
    authors = ', '.join('**R. Cruz**' if author.get('ORCID', '') == 'http://orcid.org/0000-0002-5189-6228' or author['given'][0] + author['family'] == 'RCruz' else f'{author["given"][0]}. {author["family"]}' for author in info['author'])
    where = info['publisher'] + ' ' + ' - '.join(info['container-title'])
    where = where.replace('&amp;', '&')
    my_categories = frozenset(my_categories)
    return {
        'Year': info['published']['date-parts'][0][0],
        'Paper': '[' + info['title'][0] + '](' + info['URL'] + ')\n' + authors + '\n*' + where + '*',
        'Topic': topic,
        'Type': info['type'],
        'Citations': info['is-referenced-by-count'],
        'SJR Rank': get_sjr_rank(where, my_categories) if info['type'] != 'proceedings-article' else '',
        'CORE Rank': get_core_rank(conference_acronym(where)) if info['type'] != 'journal-article' else '',
    }
