#!/usr/bin/env python3
# convert Ciência Vitae's XML to HTML and LaTeX

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('xml')
args = parser.parse_args()

import os, re, io
from datetime import datetime, timedelta
from lxml import etree
from tqdm import tqdm
from ruamel.yaml import YAML  # round-trip YAML: keeps the comments when the downloaded information is written
from ruamel.yaml.comments import CommentedMap
import scrap
xml = etree.parse(args.xml)

# hand-written information (e.g. tags) in a YAML with the same name as the XML
yaml = YAML()
yaml.width = 4096  # do not wrap long lines
info_filename = args.xml[:-3] + 'yaml'
info = CommentedMap()
if os.path.exists(info_filename):
    info = yaml.load(open(info_filename)) or CommentedMap()
normalize = lambda s: re.sub(r'\W+', '', s).lower()  # match keys ignoring case and punctuation
outputs_info = {normalize(str(k)): v for k, v in (info.get('outputs') or {}).items()}

# add more information to the XML
nsmap = {'output': 'http://www.cienciavitae.pt/ns/output',
         'service': 'http://www.cienciavitae.pt/ns/service',
         'extra': 'http://extra'}
# everything downloaded (citations, journal/conference metrics, thesis URLs) is stored in the YAML,
# with the time of the download ('downloaded'). if that was less than MAX_AGE ago, the stored values
# are used and nothing is downloaded (except for new outputs or venues). otherwise everything is
# downloaded again; if a download fails (e.g. captcha) or finds nothing (n/a), the stored value is
# kept. a scraper that fails is not tried again during this run.
MAX_AGE = timedelta(days=30)
fresh = bool(info.get('downloaded')) and datetime.now() - datetime.fromisoformat(str(info['downloaded'])) < MAX_AGE
if not fresh:
    info['downloaded'] = datetime.now().isoformat(sep=' ', timespec='seconds')
def section(key):  # a dictionary in the YAML, created if missing or empty
    if not info.get(key):
        info[key] = CommentedMap()
    return info[key]
def flow_map():  # dictionary written in one line in the YAML: {key: value, ...}
    m = CommentedMap()
    m.fa.set_flow_style()
    return m
metrics = section('metrics')  # journal or conference -> metric -> value
papers_info = section('papers')  # DOI -> citations, venue, journal or conference
theses = section('theses')  # RENATES thesis id -> URL
failed_scrapers = set()
def get_metric(venue, name, scraper):
    stored = metrics.get(venue, {}).get(name)
    if fresh and stored is not None:
        return stored
    if name not in failed_scrapers:
        try:
            value = scraper(venue)
            try: value = float(value)
            except ValueError: pass
            if value != 'n/a' or stored is None:  # n/a = not found online; it does not replace a stored value
                metrics.setdefault(venue, flow_map())[name] = value
                return value
            tqdm.write(f'warning: {name} of {venue} not found online')
        except Exception as e:
            if not isinstance(e, KeyError):  # KeyError = venue unknown to the scraper; anything else = site problem
                failed_scrapers.add(name)
            tqdm.write(f'warning: could not download {name} of {venue} ({type(e).__name__}: {str(e).splitlines()[0] if str(e) else ""})')
    if stored is not None:
        tqdm.write(f'warning: using the stored {name} of {venue}')
        return stored
    return 'n/a'

def get_paper_info(output, doi):
    # from Crossref: citations, and the journal or conference whose metrics are shown
    if fresh and doi in papers_info:
        return papers_info[doi]
    try:
        crossref = scrap.get_crossref_info(doi)
    except Exception as e:
        if doi not in papers_info:
            raise
        tqdm.write(f'warning: could not download {doi} from Crossref ({type(e).__name__}), using the stored citations')
        return papers_info[doi]
    paper = flow_map()
    paper['citations'] = crossref['is-referenced-by-count']
    output_type = output.xpath('./output:output-type/@code', namespaces=nsmap)[0]  # code, so it works in any export language
    if output_type == 'P101':  # journal article: impact factor and SJR quartile
        paper['journal'] = crossref['container-title'][0].replace('&amp;', '&')
    if output_type in ['P122', 'P103', 'P105']:  # conference paper, book, book chapter: CORE rank
        publisher = output.xpath('.//output:publisher/text()', namespaces=nsmap)
        proceedings = output.xpath('.//output:proceedings-title/text()', namespaces=nsmap)
        if publisher:
            acronym = publisher[0].split()[-1][1:-1]
        elif proceedings:
            acronym = proceedings[0].split()[0]
        elif crossref['type'] == 'book-chapter' and 'assertion' in crossref:
            d = {i['name']: i['value'] for i in crossref['assertion']}
            paper['venue'] = d['conference_name']
            acronym = d['conference_acronym']
        else:
            container = crossref['container-title'][0]
            paper['venue'] = container
            acronym = re.search(r'\(([A-Z]+)', container).group(1)
        paper['conference'] = acronym
    papers_info[doi] = paper
    return paper

def get_extra_info(output):
    doi = output.xpath('.//output:identifier[output:identifier-type/@code="doi"]/output:identifier/text()', namespaces=nsmap)
    if not doi: return {}
    paper = get_paper_info(output, str(doi[0]))  # str: lxml's string type cannot be written to the YAML
    extra = {'citations': paper['citations']}
    if 'venue' in paper:
        extra['venue'] = paper['venue']
    if 'journal' in paper:
        extra['impact-factor'] = get_metric(paper['journal'], 'impact-factor', scrap.get_impact_factor)
        extra['sjr-rank'] = get_metric(paper['journal'], 'sjr-rank', scrap.get_quartile)
    if 'conference' in paper:
        extra['core-rank'] = get_metric(paper['conference'], 'core-rank', scrap.get_core_rank)
    return extra
def is_preprint(output, doi):
    # Ciência Vitae's preprint type, or a preprint exported as a journal article (e.g. arXiv's "CoRR", from ORCID)
    journal = output.xpath('./output:journal-article/output:journal/text()', namespaces=nsmap)
    return (output.xpath('./output:output-type/@code', namespaces=nsmap)[0] == 'P127'
            or bool(journal and re.search(r'\b(corr|\w*rxiv)\b', journal[0], re.I))  # CoRR, arXiv, bioRxiv, medRxiv...
            or bool(doi and doi[0].lower().startswith('10.48550/')))  # arXiv DOI
used_info = set()
for output in tqdm(xml.xpath('//output:output', namespaces=nsmap), desc='scrap metrics'):
    doi = output.xpath('.//output:identifier[output:identifier-type/@code="doi"]/output:identifier/text()', namespaces=nsmap)
    if is_preprint(output, doi):
        output.getparent().remove(output)  # preprints are left out of both HTML and LaTeX (the user's choice)
        continue
    title = output.xpath('./output:*/output:article-title/text() | ./output:*/output:paper-title/text() | ./output:*/output:chapter-title/text() | ./output:*/output:title/text()', namespaces=nsmap)
    key = normalize(doi[0] if doi else title[0])
    if key in outputs_info and outputs_info[key].get('hide'):
        used_info.add(key)
        output.getparent().remove(output)  # left out of both HTML and LaTeX
        continue
    extra_elem = etree.Element('{http://extra}extra', nsmap=nsmap)
    for name, value in get_extra_info(output).items():
        etree.SubElement(extra_elem, '{http://extra}' + name).text = str(value)
    if key in outputs_info:
        used_info.add(key)
        tags_elem = etree.SubElement(extra_elem, '{http://extra}tags')
        for tag in outputs_info[key].get('tags', []):
            etree.SubElement(tags_elem, '{http://extra}tag').text = tag
    elif outputs_info:
        tqdm.write(f'warning: no YAML entry for: {doi[0] if doi else title[0]}')
    output.append(extra_elem)
for key in outputs_info.keys() - used_info:
    print('warning: YAML entry matches no output:', key)
# webpage notice box ({email} is turned into a link by the XSLT)
if 'notice' in info:
    etree.SubElement(xml.getroot(), '{http://extra}notice').text = str(info['notice'])
# webpage footer: when the citations and metrics were downloaded (the data sources are written in the XSLT)
etree.SubElement(xml.getroot(), '{http://extra}updated').text = str(info['downloaded'])[:10]
for service in tqdm(xml.xpath('//service:research-based-degree-supervision', namespaces=nsmap), desc='scrap theses'):
    extra_elem = etree.Element('{http://extra}extra', nsmap=nsmap)
    tid = [str(t) for t in service.xpath('.//service:tid/text()', namespaces=nsmap)]
    if tid:
        if not (fresh and tid[0] in theses):
            try:
                theses[tid[0]] = scrap.get_thesis_url(tid[0])
            except Exception as e:
                tqdm.write(f'warning: could not download the URL of thesis {tid[0]} ({type(e).__name__})')
        url = theses.get(tid[0])
        if url:
            etree.SubElement(extra_elem, '{http://extra}url').text = url
            service.append(extra_elem)
# save the downloaded information (written to memory first, so that an error does not empty the file)
buffer = io.StringIO()
yaml.dump(info, buffer)
open(info_filename, 'w').write(buffer.getvalue())
#print(etree.tostring(xml, pretty_print=True, encoding="unicode"))

# convert the XML
for ext in ['html', 'tex']:
    out = etree.XSLT(etree.parse(f'cienciavitae_to_{ext}.xslt'))(xml)
    with open(args.xml[:-3] + ext, 'wb') as f:
        f.write(out)