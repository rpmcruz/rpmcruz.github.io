import functools
import requests
import sys
import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--disable-search-engine-choice-screen')

proceedings = {
    'Advances in Computational Intelligence': ('International Work-Conference on Artificial Neural Networks', 'IWANN'),
    'Pattern Recognition and Image Analysis': ('Iberian Conference on Pattern Recognition and Image Analysis', 'IbPRIA'),
}

#sjr_categories = {  # for purposes of SJR Quartile Rank
#  'Applied Mathematics', 'Artificial Intelligence', 'Bioengineering',
#  'Biomedical Engineering', 'Computational Mathematics',
#  'Computer Science Applications', 'Computer Science (miscellaneous)',
#  'Computer Vision and Pattern Recognition', 'Control and Optimization',
#  'Electrical and Electronic Engineering', 'Engineering (miscellaneous)',
#  'Mathematics (miscellaneous)', 'Signal Processing',
#  'Statistics and Probability', 'Statistics, Probability and Uncertainty',
#  'Software',
#}

def get_hindices():
    hindices = {}
    # scholar
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
    response = requests.get('https://scholar.google.pt/citations?user=pSFY_gQAAAAJ', headers=headers)
    response.raise_for_status()
    tree = etree.HTML(response.content)
    hindices['[Google Scholar](https://scholar.google.pt/citations?user=pSFY_gQAAAAJ)'] = int(tree.xpath('//table/tbody/tr[2]/td[2]/text()')[0])
    # scopus
    '''
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.scopus.com/authid/detail.uri?authorId=57192670388')
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//section/div/div[3]//span[@data-testid="unclickable-count"]')))
    hindices['[Scopus](https://www.scopus.com/authid/detail.uri?authorId=57192670388)'] = int(element.text)
    driver.close()
    '''
    print('Scopus is forcing human verification - https://www.scopus.com/authid/detail.uri?authorId=57192670388', file=sys.stderr)
    hindex = 5
    print(f'Setting h-index to {hindex}', file=sys.stderr)
    hindices['[Scopus](https://www.scopus.com/authid/detail.uri?authorId=57192670388)'] = hindex
    # web of science
    '''
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.webofscience.com/wos/author/record/IQV-2746-2023')
    element = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '(//div[@class="wat-author-metric"])[1]')))
    hindices['[Web of Science](https://www.webofscience.com/wos/author/record/IQV-2746-2023)'] = int(element.text)
    driver.close()
    '''
    print('WebOfScience is forcing human verification - https://www.webofscience.com/wos/author/record/IQV-2746-2023', file=sys.stderr)
    hindex = 4
    print(f'Setting h-index to {hindex}', file=sys.stderr)
    hindices['[Web of Science](https://www.webofscience.com/wos/author/record/IQV-2746-2023)'] = hindex
    return hindices

@functools.cache
def get_core_rank(acronym):
    response = requests.get(f'http://portal.core.edu.au/conf-ranks/?search={acronym}&by=acronym&source=all')
    response.raise_for_status()
    tree = etree.HTML(response.content)
    rank = tree.xpath('//table//tr[2]/td[4]/text()')
    if len(rank) == 0: return 'n/a'
    rank = rank[0].strip()
    if rank.startswith('National'): return 'n/a'
    return rank

@functools.cache
def get_impact_factor(journal_name):
    # impact factor is from Clarivate's Web of Science
    # impact score is from Elsevier's Scopus (same formula, different data)
    # Clarivate makes impact factor different to find. some websites that
    # publish it are: bioxbio.com, scijournal.org, wikipedia.org.
    # just to be safe, we are getting these values directly from each journal.
    journal_id = {
        'Springer Pattern Analysis and Applications': ('springer', 10044),
        'Elsevier Computers & Electrical Engineering': ('elsevier', 'computers-and-electrical-engineering'),
        'PeerJ Computer Science': ('peerj', 'computer-science'),
        'MDPI Mathematics': ('mdpi', 'mathematics'), 'MDPI Sensors': ('mdpi', 'sensors'),
        'Springer International Journal of Data Science and Analytics': ('springer', 41060),
        'Elsevier Pattern Recognition': ('elsevier', 'pattern-recognition'),
        'Elsevier Neurocomputing': ('elsevier', 'neurocomputing'),
        'Elsevier Computer Vision and Image Understanding': ('elsevier', 'computer-vision-and-image-understanding'),
        'IEEE Transactions on Intelligent Vehicles': ('ieee', 7274857),
        'IEEE Transactions on Neural Networks and Learning Systems': ('ieee', 5962385),
        'IEEE Transactions on Cybernetics': ('ieee', 6221036),
        'IEEE Access': ('ieee', 6287639),
        # without impact factor
        'Springer Lecture Notes in Computer Science': None,
        'Elsevier Intelligent Systems with Applications': None,
        'IEEE Transactions on Artificial Intelligence': None,
    }
    methods = {
        'springer': (False, 'https://link.springer.com/journal/', '//dd[@data-test="impact-factor-value"]/b/text()', lambda s: s.split()[0]),
        'elsevier': (True, 'https://www.sciencedirect.com/journal/', '//div[contains(@class, "js-impact-factor")]//span[contains(@class, "text-l")]', None),
        'peerj': (False, 'https://peerj.com/', '//a[@id="cta_home_statsbar_impact_factor"]/b/text()', None),
        'mdpi': (False, 'https://www.mdpi.com/journal/', '//div[@class="journal__description"]/div[2]/text()', lambda s: s.split()[0]),
        'ieee': (True, 'https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=', '//a[@class="stats-jhp_metric_impact_factor"]/span[1]', None),
    }
    id = journal_id[journal_name]
    if id == None:
        return 'n/a'
    use_selenium, url, xpath, postprocess = methods[id[0]]
    url = url + str(id[1])
    if use_selenium:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(1)
        element = WebDriverWait(driver, 60).until(
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
def get_sjr_rank(journal_name):
    # as per DEI criterion, we use best quartile, independent of category
    journals_id = {
        'Springer Lecture Notes in Computer Science': 25674,
        'Springer Pattern Analysis and Applications': 24822,
        'Springer International Journal of Data Science and Analytics': 21101017225,
        'PeerJ Computer Science': 21100830173,
        'MDPI Mathematics': 21100830702, 'MDPI Sensors': 130124,
        'Elsevier Computers & Electrical Engineering': 18159,
        'Elsevier Intelligent Systems with Applications': 21101051831,
        'Elsevier Pattern Recognition': 24823,
        'Elsevier Neurocomputing': 24807,
        'Elsevier Computer Vision and Image Understanding': 24161,
        'IEEE Transactions on Artificial Intelligence': 21101093601,
        'IEEE Transactions on Intelligent Vehicles': 21100976127,
        'IEEE Transactions on Neural Networks and Learning Systems': 21100235616,
        'IEEE Transactions on Cybernetics': 21100274221,
        'IEEE Access': 21100374601,
    }
    id = journals_id[journal_name]
    response = requests.get(f'https://www.scimagojr.com/journalsearch.php?q={id}&tip=sid', timeout=5)
    response.raise_for_status()
    tree = etree.HTML(response.content)
    tbody = tree.xpath('//div[@class="dashboard"]//table/tbody')[0]
    categories = tbody.xpath('./tr/td[1]/text()')
    years = tbody.xpath('./tr/td[2]/text()')
    quartiles = tbody.xpath('./tr/td[3]/text()')
    max_year = max(int(y) for y in years)
    return min(quartile for category, year, quartile in zip(categories, years, quartiles) if int(year) == max_year)  # and category in sjr_categories)

def get_paper_info(query):
    paper = requests.get(f'https://api.crossref.org/works/{query["doi"]}').json()['message']
    year = paper['published']['date-parts'][0][0]
    title = paper['title'][0]
    authors = ', '.join('__**R. Cruz**__' if author.get('ORCID', '') == 'http://orcid.org/0000-0002-5189-6228' or author['given'][0] + author['family'] == 'RCruz' else author['given'][0] + '. ' + author['family'] for author in paper['author'])
    where = paper['container-title'][0].replace('&amp;', '&')
    citations = paper['is-referenced-by-count']
    type = 'journal' if paper['type'] == 'journal-article' else 'conference'
    conference = None
    if 'journal' in query:
        type = 'journal'
        where = query['journal']
    elif 'conference' in query:
        type = 'conference'
        where = query['conference']
        conference = query['conference'].split()[-1][1:-1]
    elif type == 'journal':
        publisher = paper['publisher'].split()
        if publisher[-1].startswith('(') and publisher[-1].endswith(')'):
            publisher = publisher[-1][1:-1]
        else:
            publisher = publisher[0]
        if not where.startswith(publisher):
            where = publisher + ' ' + where
    elif paper['type'] == 'book-chapter' and 'assertion' in paper:
        d = {i['name']: i['value'] for i in paper['assertion']}
        where = d['conference_name'] + ' ' + d['conference_year'] + ' (' + d['conference_acronym'] + ')'
        conference = d['conference_acronym']
    elif type == 'conference':
        conferences = {'ICMV', 'ICPR', 'EMBC', 'IJCNN', 'PRNI'}
        for conf in conferences:
            if conf in where:
                conference = conf
        assert conference is not None, 'fix conference for ' + where
    return {'type': type, 'year': year, 'authors': authors, 'title': title,
        'where': where, 'citations': citations, 'conference': conference,
        'link': paper['URL'], 'doi': query['doi']}

def get_metrics(paper):
    metrics = {}
    if paper['type'] == 'journal':
        metrics['IF'] = get_impact_factor(paper['where'])
        metrics['SJR'] = get_sjr_rank(paper['where'])
    if paper['type'] == 'conference':
        metrics['CORE'] = get_core_rank(paper['conference'])
    return metrics
