import argparse
parser = argparse.ArgumentParser()
parser.add_argument('yaml')
args = parser.parse_args()

import yaml
cv = yaml.safe_load(open(args.yaml))

proceedings = {
    'Advances in Computational Intelligence': ('International Work-Conference on Artificial Neural Networks', 'IWANN'),
    'Pattern Recognition and Image Analysis': ('Iberian Conference on Pattern Recognition and Image Analysis', 'IbPRIA'),
}

sjr_categories = {  # for purposes of SJR Quartile Rank
  'Applied Mathematics', 'Artificial Intelligence', 'Bioengineering',
  'Biomedical Engineering', 'Computational Mathematics',
  'Computer Science Applications', 'Computer Science (miscellaneous)',
  'Computer Vision and Pattern Recognition', 'Control and Optimization',
  'Electrical and Electronic Engineering', 'Engineering (miscellaneous)',
  'Mathematics (miscellaneous)', 'Signal Processing',
  'Statistics and Probability', 'Statistics, Probability and Uncertainty',
}

import functools
import requests
from lxml import etree

@functools.cache
def get_core_rank(acronym):
    response = requests.get(f'http://portal.core.edu.au/conf-ranks/?search={acronym}&by=acronym&source=all')
    response.raise_for_status()
    tree = etree.HTML(response.content)
    rank = tree.xpath('//table//tr[2]/td[4]/text()')
    if len(rank) == 0 or rank[0].startswith('National'):
        return None
    rank = rank[0].strip()

@functools.cache
def get_impact_factor(journal_name):
    # impact factor is from Clarivate's Web of Science
    # impact score is from Elsevier's Scopus (same formula, different data)
    # Clarivate makes impact factor different to find. some websites that
    # publish it are: bioxbio.com, scijournal.org, wikipedia.org.
    # just to be safe, we are getting these values directly from each journal.
    journal_id = {
        'Pattern Analysis and Applications': ('springer', 10044),
        'Computers &amp; Electrical Engineering': ('elsevier', 'computers-and-electrical-engineering'),
        'PeerJ Computer Science': ('peerj', 'computer-science'),
        'Mathematics': ('mdpi', 'mathematics'), 'Sensors': ('mdpi', 'sensors'),
        'International Journal of Data Science and Analytics': ('springer', 41060),
        'Pattern Recognition': ('elsevier', 'pattern-recognition'),
        'IEEE Transactions on Intelligent Vehicles': ('ieee', 7274857),
        'IEEE Access': ('ieee', 6287639),
        'Neurocomputing': ('elsevier', 'neurocomputing'),
        # without impact factor
        'Lecture Notes in Computer Science': None,
        'Intelligent Systems with Applications': None,
        'Transactions on Artificial Intelligence': None,
    }
    methods = {
        'springer': (False, 'https://link.springer.com/journal/', '//dd[@data-test="impact-factor-value"]/b/text()', lambda s: s.split()[0]),
        'elsevier': (True, 'https://www.sciencedirect.com/journal/', '//div[contains(@class, "js-impact-factor")]//span[contains(@class, "text-l")]', None),
        'peerj': (False, 'https://peerj.com/', '//a[@id="cta_home_statsbar_impact_factor"]/b/text()', None),
        'mdpi': (False, 'https://www.mdpi.com/journal/', '//div[@class="journal__description"]/div[2]/text()', lambda s: s.split()[0]),
        'ieee': (True, 'https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=', '//a[@class="stats-jhp-impact-factor"]/span[1]', None),
    }
    id = journal_id[journal_name]
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
def get_sjr_rank(journal_name):
    journals_id = {
        'Lecture Notes in Computer Science': 25674,
        'Pattern Analysis and Applications': 24822,
        'Computers &amp; Electrical Engineering': 18159,
        'PeerJ Computer Science': 21100830173,
        'Mathematics': 21100830702, 'Sensors': 130124,
        'Intelligent Systems with Applications': 21101051831,
        'International Journal of Data Science and Analytics': 21101017225,
        'Pattern Recognition': 24823,
        'Transactions on Artificial Intelligence': 21101093601,
        'IEEE Transactions on Intelligent Vehicles': 21100976127,
        'Neurocomputing': 24807,
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
    return min(quartile for category, year, quartile in zip(categories, years, quartiles) if int(year) == max_year and category in sjr_categories)

def get_paper_info(doi):
    paper = requests.get(f'https://api.crossref.org/works/{doi}').json()['message']
    year = paper['published']['date-parts'][0][0]
    title = paper['title'][0]
    authors = ', '.join('**R. Cruz**' if author.get('ORCID', '') == 'http://orcid.org/0000-0002-5189-6228' or author['given'][0] + author['family'] == 'RCruz' else author['given'][0] + '. ' + author['family'] for author in paper['author'])
    where = paper['container-title'][0].replace('&amp;', '&')
    if paper['type'] == 'journal-article':
        type = 'journal'
        IF = get_impact_factor(where)
        SJR = get_sjr_rank(where)
        metrics = f'**SJR={SJR}**, **IF={IF}**'
    elif paper['type'] == 'book-chapter' and 'assertion' in paper:
        type = 'conference'
        d = {i['name']: i['value'] for i in paper['assertion']}
        where = d['conference_name'] + ' ' + d['conference_year'] + ' (' + d['conference_acronym'] + ')'
        CORE = get_core_rank(d['conference_acronym'])
        metrics = f'**CORE={CORE}**' if CORE else ''
    else:
        type = 'conference'
        CORE = get_core_rank(where)
        metrics = f'**CORE={CORE}**' if CORE else ''
    if metrics:
        metrics = ', ' + metrics
    return {'type': type, 'year': year, 'entry': f'{authors}, "{title}", *{where}*{metrics}'}

import re

def markdown(text, newline=r'\\'):
    text = re.sub(r'!\[\]\((.*?)\)', r'\\includegraphics[width=300px]{\1}', text)  # image
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1 \\href{\2}{\\includegraphics[width=0.8em]{imgs/link.pdf}}', text)  # links
    text = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', text)  # bold
    text = re.sub(r'\*(.*?)\*', r'\\textit{\1}', text)  # italic
    text = re.sub(r'\=\=([^=]*?)\=\=', r'\\hl{\1}', text)  # highlight
    text = text.replace('&', r'\&').replace('~', r'$\sim$')  # escape symbols
    text = text.replace('#', r'\#')
    text = text.replace('\n', newline + '\n')  # force breaklines
    text = re.sub(r'"(.*?)"', r"``\1''", text)
    return text

print(r'\documentclass{moderncv}')
print(r'\moderncvstyle{classic}')
print(r'\moderncvcolor{blue}')
print(r'\usepackage[margin=2cm]{geometry}')
print(r'\usepackage{soul}')
print(r'\name{' + cv['firstname'] + '}{' + cv['lastname'] + '}')
print(r'\title{' + cv['title'] + '}')
print(r'\email{' + cv['email'] + '}')
print(r'\homepage{' + cv['homepage'] + '}')
print(r'\social[github]{' + cv['github'] + '}')
print(r'\social[orcid]{' + cv['orcid'] + '}')
print(r'\photo{photo}')
print()

print(r'\begin{document}')
print(r'\makecvtitle')

print(markdown(cv['biography']))

# add Research Interests (itemize)?

print(r'\section{Education}')
for entry in cv['education']:
    print(r'\cvitem{\textbf{' + str(entry['year']) + r'}}{\textbf{' + entry['degree'] + '}}')
    print(r'\cvitem{Institution}{' + entry['institution'] + '}')

print(r'\section{Work Experience}')
for entry in cv['employment']:
    print(r'\cventry{' + entry['dates'] + '}{' + entry['title'] + '}{' + entry['employer'] + '}{}{}{' + markdown(entry['details']) + '}')

print(r'\section{Publications}')
papers = cv['submitted_papers'] + \
    [get_paper_info(paper) for paper in cv['published_papers']]

for type, title in [('conference', 'International Conference Proceedings'), ('journal', 'Journal Publications')]:
    print(r'\subsection{' + title + '}')
    for paper in papers:
        if paper['type'] == type:
            print(r'\cvitem{' + str(paper['year']) + '}{' + markdown(paper['entry']) + '}')

print(r'\section{Supervisions}')
for type in ['MSc Dissertation', 'BSc Project', 'Internship']:
    print(r'\subsection{' + type + 's}')
    for entry in cv['supervisions']:
        if entry['type'] == type:
            title = markdown('[' + entry['title'] + '](' + entry['link'] + ')') if 'link' in entry else entry['title']
            note = ' (with co-supervisor: ' + entry['cosupervisor'] + ')' if 'cosupervisor' in entry else ''
            print(r'\cvitem{' + str(entry['date']) + '}{' + entry['student'] + ', "' + title + '", *' + entry['university'] + '*' + note + '}')

print(r'\end{document}')
