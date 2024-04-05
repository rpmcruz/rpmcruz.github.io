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

def get_id(journal_name, name2id):
    for name, id in name2id.items():
        if name in journal_name:
            return id
    raise Exception(f'Journal "{journal_name}" unknown.')

@functools.cache
def get_impact_factor(journal_name):
    # impact factor is from Clarivate's Web of Science
    # impact score is from Elsevier's Scopus (same formula, different data)
    # Clarivate makes impact factor different to find. some websites that
    # publish it are: bioxbio.com, scijournal.org, wikipedia.org.
    # just to be safe, we are getting these values directly from each journal.
    name2id = {
        'Lecture Notes in Computer Science': None,
        'Pattern Analysis and Applications': ('springer', 10044),
        'Computers & Electrical Engineering': ('elsevier', 'computers-and-electrical-engineering'),
        'PeerJ Computer Science': ('peerj', 'computer-science'),
        'Mathematics': ('mdpi', 'mathematics'), 'Sensors': ('mdpi', 'sensors'),
        'Intelligent Systems with Applications': None,
        'International Journal of Data Science and Analytics': ('springer', 41060),
        'Pattern Recognition': ('elsevier', 'pattern-recognition'),
        'Transactions on Artificial Intelligence': None,
        'Transactions on Intelligent Vehicles': ('ieee', 7274857),
    }
    methods = {
        'springer': (False, 'https://link.springer.com/journal/', '//dd[@data-test="impact-factor-value"]/b/text()', lambda s: s.split()[0]),
        'elsevier': (True, 'https://www.sciencedirect.com/journal/', '//div[contains(@class, "js-impact-factor")]//span[contains(@class, "text-l")]', None),
        'peerj': (False, 'https://peerj.com/', '//a[@id="cta_home_statsbar_impact_factor"]/b/text()', None),
        'mdpi': (False, 'https://www.mdpi.com/journal/', '//div[@class="journal__description"]/div[2]/text()', lambda s: s.split()[0]),
        'ieee': (True, 'https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=', '//a[@class="stats-jhp-impact-factor"]/span[1]', None),
    }
    id = get_id(journal_name, name2id)
    if id == None:
        return 'n/a'
    use_selenium, url, xpath, postprocess = methods[id[0]]
    url = url + str(id[1])
    if use_selenium:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.wait import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        driver = webdriver.Chrome()
        driver.get(url)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        r = element.text
        driver.close()
    else:
        response = requests.get(url)
        response.raise_for_status()
        tree = etree.HTML(response.content)
        r = tree.xpath(xpath)[-1]
    if postprocess:
        r = postprocess(r)
    return r

@functools.cache
def get_sjr_rank(journal_name, my_categories):
    # 'my_categories' must be hashable (such as frozenset) since we are using
    # functools.cache
    name2id = {
        'Lecture Notes in Computer Science': 25674,
        'Pattern Analysis and Applications': 24822,
        'Computers & Electrical Engineering': 18159,
        'PeerJ Computer Science': 21100830173,
        'Mathematics': 21100830702, 'Sensors': 130124,
        'Intelligent Systems with Applications': 21101051831,
        'International Journal of Data Science and Analytics': 21101017225,
        'Pattern Recognition': 24823,
        'Transactions on Artificial Intelligence': 21101093601,
        'Transactions on Intelligent Vehicles': 21100976127,
    }
    id = get_id(journal_name, name2id)
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
    return {
        'Year': info['published']['date-parts'][0][0],
        'Paper': '[' + info['title'][0] + '](' + info['URL'] + ')\n' + authors + '\n*' + where + '*',
        'Topic': topic,
        'Type': info['type'],
        'Citations': info['is-referenced-by-count'],
        'IF': get_impact_factor(where) if info['type'] == 'journal-article' else '',
        'SJR Rank': get_sjr_rank(where, my_categories) if info['type'] != 'proceedings-article' else '',
        'CORE Rank': get_core_rank(conference_acronym(where)) if info['type'] != 'journal-article' else '',
    }
