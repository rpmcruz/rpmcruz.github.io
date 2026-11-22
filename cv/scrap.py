import requests
from lxml import etree
import functools, re, sys, csv, os
from random import random
from playwright.sync_api import sync_playwright
page = None

def browser():
    # like a person's browser, it keeps its cookies between runs (in browser-profile/), so websites
    # remember it; e.g. Cloudflare remembers that the "I am human" check was passed
    global page
    if page is None:
        pw = sync_playwright().start()
        profile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'browser-profile')
        context = pw.chromium.launch_persistent_context(profile, headless=False)
        page = context.pages[0] if context.pages else context.new_page()
    return page

def pause():  # wait a few seconds before clicking, as a person reading the page would
    browser().wait_for_timeout(2000 + 3000 * random())

def get_scholar_hindex():
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
    response = requests.get('https://scholar.google.com/citations?user=8hwqwn4AAAAJ', headers=headers)
    response.raise_for_status()
    tree = etree.HTML(response.content)
    return int(tree.xpath('//table[@id="gsc_rsb_st"]/tbody/tr[2]/td[2]/text()'))

def get_scholar_refs():
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
    response = requests.get('https://scholar.google.com/citations?user=8hwqwn4AAAAJ', headers=headers)
    response.raise_for_status()
    tree = etree.HTML(response.content)
    papers = tree.xpath('//tr[@class="gsc_a_tr"]')
    refs = {paper.xpath('./td[@class="gsc_a_t"]/a/text()')[0]: paper.xpath('./td[@class="gsc_a_c"]/a/text()') for paper in papers}
    refs = {k.lower().replace(' ', ''): 0 if len(v) == 0 else int(v[0]) for k, v in refs.items()}
    return refs

@functools.cache
def get_crossref_info(doi):
    return requests.get(f'https://api.crossref.org/works/{doi}').json()['message']

@functools.cache
def get_impact_factor(journal):
    # impact factor is from Clarivate's Web of Science
    # impact score is from Elsevier's Scopus (same formula, different data)
    # Clarivate makes impact factor different to find. some websites that
    # publish it are: bioxbio.com, scijournal.org, wikipedia.org.
    # just to be safe, we are getting these values directly from each journal.
    journal_id = {
        'Pattern Analysis and Applications': ('springer', 10044),
        'Computers & Electrical Engineering': ('elsevier', 'computers-and-electrical-engineering'),
        'PeerJ Computer Science': ('peerj', 'computer-science'),
        'Mathematics': ('mdpi', 'mathematics'),
        'Sensors': ('mdpi', 'sensors'),
        'International Journal of Data Science and Analytics': ('springer', 41060),
        'Pattern Recognition': ('elsevier', 'pattern-recognition'),
        'Neurocomputing': ('elsevier', 'neurocomputing'),
        'Computer Vision and Image Understanding': ('elsevier', 'computer-vision-and-image-understanding'),
        'Intelligent Systems with Applications': ('elsevier', 'intelligent-systems-with-applications'),
        'IEEE Transactions on Intelligent Vehicles': ('ieee', 7274857),
        'IEEE Transactions on Neural Networks and Learning Systems': ('ieee', 5962385),
        'IEEE Transactions on Cybernetics': ('ieee', 6221036),
        'IEEE Transactions on Knowledge and Data Engineering': ('ieee', 69),
        'IEEE Transactions on Image Processing': ('ieee', 83),
        'IEEE Access': ('ieee', 6287639),
        'IEEE Transactions on Sustainable Energy': ('ieee', 5165391),
        'IEEE Transactions on Artificial Intelligence': ('ieee', 9078688),
    }
    methods = {
        'springer': (False, 'https://link.springer.com/journal/', '//dd[@data-test="impact-factor-value"]/span/text()', lambda s: s.split()[0]),
        'elsevier': (True, 'https://www.sciencedirect.com/journal/', '//div[contains(@class, "js-impact-factor")]//span[contains(@class, "text-l")]', None),
        'peerj': (True, 'https://peerj.com/journals/', '//button[contains(normalize-space(.), "Journal impact factor")]/ancestor::div[2]/div[1]', lambda s: s.split()[0]),
        'mdpi': (True, 'https://www.mdpi.com/journal/', '//span[normalize-space(.)="Impact Factor"]/../preceding-sibling::span[1]', None),
        'peerj': (True, 'https://peerj.com/journals/', '//button[contains(normalize-space(.), "Journal impact factor")]/ancestor::div[2]/div[1]', lambda s: s.split()[0]),
        'mdpi': (True, 'https://www.mdpi.com/journal/', '//span[normalize-space(.)="Impact Factor"]/../preceding-sibling::span[1]', None),
        'ieee': (True, 'https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=', '//a[@class="stats-jhp_metric_impact_factor"]/span[1]', None),
    }
    id = journal_id[journal]
    if id == None:
        return 'n/a'
    use_selenium, url, xpath, postprocess = methods[id[0]]
    url = url + str(id[1])
    if use_selenium:
        browser().goto(url)
        if id[0] == 'ieee':  # HACK: some journals don't yet have impact factor
            browser().locator('div.metrics-container-wrapper').wait_for(state='visible')
        locator = browser().locator(f'xpath={xpath}')
        r = locator.text_content() if locator.count() else None
    else:
        response = requests.get(url)
        response.raise_for_status()
        tree = etree.HTML(response.content)
        r = tree.xpath(xpath)[-1]
    if r is None:
        return 'n/a'
    if postprocess:
        r = postprocess(r)
    return r

@functools.cache
def get_quartile(journal):
    # as per FEUP criterion, we use best quartile, independent of category
    journals_id = {
        'Lecture Notes in Computer Science': 25674,
        'Pattern Analysis and Applications': 24822,
        'International Journal of Data Science and Analytics': 21101017225,
        'PeerJ Computer Science': 21100830173,
        'Mathematics': 21100830702,
        'Sensors': 130124,
        'Computers & Electrical Engineering': 18159,
        'Intelligent Systems with Applications': 21101051831,
        'Pattern Recognition': 24823,
        'Neurocomputing': 24807,
        'Computer Vision and Image Understanding': 24161,
        'IEEE Transactions on Artificial Intelligence': 21101093601,
        'IEEE Transactions on Intelligent Vehicles': 21100976127,
        'IEEE Transactions on Neural Networks and Learning Systems': 21100235616,
        'IEEE Transactions on Cybernetics': 21100274221,
        'IEEE Transactions on Knowledge and Data Engineering': 17362,
        'IEEE Transactions on Image Processing': 25534,
        'IEEE Access': 21100374601,
    }
    id = journals_id[journal]
    return get_scimago_table().get(id, 'n/a')

@functools.cache
def get_scimago_table():
    # Scimago is behind Cloudflare, which blocked the old scraper: it opened one journal page after
    # another, typing their URLs, in a browser without cookies. so browse like a person instead: open
    # the home page, click "Journal Rankings", then "Download data" (a table with every journal, so
    # this is done once): Sourceid -> best quartile across subject categories.
    page = browser()
    page.goto('https://www.scimagojr.com/')
    link = page.locator('a[href$="journalrank.php"]:visible').first  # "Journal Rankings"
    link.wait_for(timeout=120_000)  # time to press the "I am human" check, if it appears
    pause()
    link.click()
    link = page.locator('a[href*="out=xls"]:visible').first  # "Download data"
    link.wait_for(timeout=120_000)
    pause()
    with page.expect_download(timeout=120_000) as download:
        link.click()
    with open(download.value.path(), encoding='utf-8-sig', errors='replace') as f:
        rows = csv.DictReader(f, delimiter=';')
        if not {'Sourceid', 'SJR Best Quartile'} <= set(rows.fieldnames or []):
            raise RuntimeError(f'unexpected Scimago columns: {rows.fieldnames}')
        return {int(r['Sourceid']): r['SJR Best Quartile'] for r in rows if r['SJR Best Quartile'] not in ('', '-')}

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

def get_thesis_url(tid):
    url = f'https://renates2.dgeec.mec.pt/ppsq.asp?I=0&U=0&N=&G=3,&T=&A=&Ar=&Tt=&Es=1,&Dc=1&Lc=1&Tc={tid}&Cc=0&Lc2=0&Tc2=&Cc2=0&Lc3=0&Tc3=&Cc3=0&Or=0&Pf='
    response = requests.get(url)
    response.raise_for_status()
    tree = etree.HTML(response.content)
    url = tree.xpath(r'//td[@class="txtLista"]/a[@target="_blank"]/@href')
    return url[0] if url else None