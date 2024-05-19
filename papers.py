import functools
import sys
import time
import requests
from lxml import etree
from crossref.restful import Works

def conference_from_book(conference):
    if conference == 'Advances in Computational Intelligence':
        return 'International Work-Conference on Artificial Neural Networks', 'IWANN'
    if conference == 'Pattern Recognition and Image Analysis':
        return 'Iberian Conference on Pattern Recognition and Image Analysis', 'IbPRIA'
    raise Exception(f'Book "{conference}" unknown.')

def get_scholar_hindex():
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
    response = requests.get('https://scholar.google.pt/citations?user=pSFY_gQAAAAJ', headers=headers)
    response.raise_for_status()
    tree = etree.HTML(response.content)
    return int(tree.xpath('//table/tbody/tr[2]/td[2]/text()')[0])

@functools.cache
def get_core_rank(acronym):
    response = requests.get(f'http://portal.core.edu.au/conf-ranks/?search={acronym}&by=acronym&source=all')
    response.raise_for_status()
    tree = etree.HTML(response.content)
    rank = tree.xpath('//table//tr[2]/td[4]/text()')
    rank = rank[0].strip() if len(rank) else 'n/a'
    if rank == 'n/a':
        print(f'Warning: could not find CORE rank for "{acronym}"', file=sys.stderr)
    return rank

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
        'Computers &amp; Electrical Engineering': ('elsevier', 'computers-and-electrical-engineering'),
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
        'Computers &amp; Electrical Engineering': 18159,
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
    paper = Works().doi(doi)
    authors = ', '.join('**R. Cruz**' if author.get('ORCID', '') == 'http://orcid.org/0000-0002-5189-6228' or author['given'][0] + author['family'] == 'RCruz' else f'{author["given"][0]}. {author["family"]}' for author in paper['author'])
    if paper['type'] == 'journal-article':
        where = f"{' - '.join(paper['container-title'])}, {paper['publisher']}"
    elif paper['type'] == 'proceedings-article':
        if 'event' in paper:
            conference_acronym = paper['event']['name']
            conference_acronym = conference_acronym[conference_acronym.rfind('(')+1:conference_acronym.rfind(')')].split()[0]
            where = f"{paper['event']['name']}, {paper['publisher']}"
    else:
        # my book chapters are all in conferences. fetch the conference name, not
        # the book name
        if 'assertion' in paper:  # some book chapters have conference info here
            conference = {i['name']: i['value'] for i in paper['assertion']}
            where = f"{conference['conference_name']} {conference['conference_year']} ({conference['conference_acronym']}), {paper['publisher']}"
            conference_acronym = conference['conference_acronym']
        else:
            name, conference_acronym = conference_from_book(paper['container-title'][0])
            year = paper['published']['date-parts'][0][0]
            where = f"{name} {year} ({conference_acronym}), {paper['publisher']}"
    where = where.replace('&amp;', '&')
    return (
        paper['published']['date-parts'][0][0],
        '[' + paper['title'][0] + '](' + paper['URL'] + ')\n' + authors + '\n*' + where + '*',
        topic,
        'journal' if paper['type'] == 'journal-article' else 'conference',
        paper['is-referenced-by-count'],
        get_impact_factor(' '.join(paper['container-title'])) if paper['type'] == 'journal-article' else '',
        get_sjr_rank(' '.join(paper['container-title']), my_categories) if paper['type'] != 'proceedings-article' else '',
        get_core_rank(conference_acronym) if paper['type'] != 'journal-article' else '',
    )
