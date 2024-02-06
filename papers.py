import argparse
parser = argparse.ArgumentParser()
parser.add_argument('type', choices=['html', 'latex'])
args = parser.parse_args()

import functools
from tqdm import tqdm
import json, re
import time
import sys
import requests
from lxml import etree
from crossref.restful import Works
from datetime import datetime

class Latex:
    def begin(self, name):
        print(r'\documentclass[12pt]{article}')
        print(r'\usepackage[a4paper, margin=3cm]{geometry}')
        print(r'\usepackage{longtable}')
        print(r'\usepackage{graphicx}')
        print(r'\usepackage[hidelinks]{hyperref}')
        print(f'\\title{{{name}}}')
        print(r'\begin{document}')
        print(r'\maketitle')

    def end(self):
        print(r'\end{document}')

    def markdown(self, text, newline=r'\\'):
        text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1 \\href{\2}{\\includegraphics[width=0.8em]{imgs/link.pdf}}', text)  # links
        text = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', text)  # bold
        text = re.sub(r'\*(.*?)\*', r'\\textit{\1}', text)  # italic
        text = re.sub(r'\=\=(.*?)\=\=', r'\\hl{\1}', text)  # highlight
        text = text.replace('&', r'\&').replace('~', r'$\sim$')  # escape symbols
        text = text.replace('\n', newline + '\n')  # force breaklines
        text = re.sub(r'"(.*?)"', r"``\1''", text)
        return text

    def contacts(self, contacts):
        for icon, text, link in contacts:
            print(f'\\includegraphics[width=0.5cm]{{imgs/{icon}.pdf}} \\href{{{link}}}{{{text}}} ')
        print('\n')

    def section(self, icon, text):
        print(f'\\section{{\\includegraphics[width=1cm]{{imgs/{icon}.pdf}} {text}}}')

    def paragraph(self, text):
        print(self.markdown(text), end='\n\n')

    def description(self, items):
        print(r'\begin{description}')
        for label, text in items:
            print(f'\\item[{label}] {self.markdown(text)}')
        print(r'\end{description}')

    def table(self, rows, filters, columns_type, columns_sort, columns_size):
        sizes = '|'.join(f'p{{{size}}}' if size else 'l' for size in columns_size)
        print(r'\begin{longtable}{|' + sizes + '|}')
        print(r'\hline')
        print('&'.join(rows[0]) + r'\\')
        print(r'\hline\endhead')
        for row in rows:
            print('&'.join(self.markdown(str(v), r'\newline') for v in row.values()) + r'\\')
            print(r'\hline')
        print(r'\end{longtable}')

class Html:
    tables = 0
    def begin(self, name):
        print('<!DOCTYPE html>')
        print('<html lang="en">')
        print('<head>')
        print('<meta charset="UTF-8">')
        print('<meta name="viewport" content="width=device-width, initial-scale=1" />')
        print(f'<title>{name}</title>')
        print('<style>')
        print('body {text-align: justify;}')
        print('h2 {margin-top: 50px; border-bottom: solid;}')
        print('.container { max-width: 800px; margin: 0 auto; }')
        print('table { width: 100%; }')
        # description
        print('@media screen and (min-width: 1000px) {div.description {display: flex; flex-direction: column} div.item {display: flex} div.left {width: 4em; font-weight: bold} div.right {flex: 1}')
        print('@media screen and (max-width: 999px) {div.item {display: inline} div.left {display: inline; font-weight: bold} div.right {display: inline}}')
        print('</style>')
        print('<script src="mytable.js"></script>')
        print('</head>')
        print('<body>')
        print('<div class="container">')
        print(f'<h1>{name}</h1>')

    def end(self):
        print('</div>')
        print('</body>')
        print('</html>')

    def markdown(self, text):
        text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)  # links
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  # bold
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)  # italic
        text = text.replace('&', '&amp;').replace('--', '&ndash;')
        text = text.replace('\n', '<br>\n')  # force breaklines
        text = re.sub(r'\=\=(.*?)\=\=', r'<span class="hl">\1</span>', text)  # highlight
        return text

    def contacts(self, contacts):
        print('<p>')
        for icon, text, link in contacts:
            print(f'<img width="28px" src="imgs/{icon}.svg"> <a href="{link}">{text}</a> ')
        print('</p>')

    def section(self, icon, text):
        print(f'<h2><img width="45px" src="imgs/{icon}.svg"> {text}</h2>')

    def paragraph(self, text):
        print('<p>' + self.markdown(text) + '</p>')

    def description(self, items):
        print('<div class="description">')
        for label, text in items:
            print(f'<div class="item"><div class="left">{label}</div><div class="right">{self.markdown(text)}</div></div>')
        print('</div>')

    def table(self, rows, filters, columns_type, columns_sort, columns_size=None):
        print(f'<div id="filters{self.tables}"></div>')
        print('</div>')  # temporarily disable container
        print(f'<div id="table{self.tables}"></div>')
        print('<div class="container">')  # re-enable container
        print('<script>')
        rows = [{key: self.markdown(str(value)) for key, value in row.items()} for row in rows]
        print(f'table = new Table("table{self.tables}", ' + json.dumps(list(rows[0].keys())) + ', ' + json.dumps(columns_type) + ', ' + json.dumps(columns_sort) + ', ' + json.dumps(rows) + ');')
        filters = {f: list(sorted(set(r[f] for r in rows))) for f in filters}
        print(f'new Filters(table, "filters{self.tables}", ' + json.dumps(filters) + ');')
        print('</script>')
        self.tables += 1

out = globals()[args.type.title()]()

#################################### START ####################################

out.begin('Ricardo Cruz, PhD')
out.contacts([
    ('profile-email', 'rpcruz@fe.up.pt', 'mailto:rpcruz@fe.up.pt'),
    ('profile-orcid', '0000-0002-5189-6228', 'https://orcid.org/0000-0002-5189-6228'),
    ('profile-github', 'github.com/rpmcruz', 'https://github.com/rpmcruz?tab=repositories'),
])
out.paragraph('Ricardo Cruz has worked on a wide range of machine learning topics, with particular emphasis on deep learning and computer vision. Since 2021, he is a researcher on autonomous driving under the THEIA research project, a partnership between the University of Porto and Bosch Car Multimedia. Prior to that, he was a researcher at INESC TEC since 2015, working towards his PhD in Computer Science. He has a BSc in computer science and a MSc in applied mathematics.')

#################################### PAPERS ####################################

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
def get_sjr_rank(journal_name):
    name2id = {'Lecture Notes in Computer Science': 25674,
        'Pattern Analysis and Applications': 24822,
        'Computers &amp; Electrical Engineering': 18159,
        'PeerJ Computer Science': 21100830173,
        'Mathematics': 21100830702, 'Sensors': 130124,
        'Intelligent Systems with Applications': 21101051831,
    }
    for name, id in name2id.items():
        if name in journal_name:
            break
    else:
        raise Exception(f'Conference "{conference}" unknown.')
    while True:
        try:
            response = requests.get(f'https://www.scimagojr.com/journalsearch.php?q={id}&tip=sid', timeout=5)
            response.raise_for_status()
            break
        except:
            print(f'Could not retrive page for {id}. Wait 1 second...', file=sys.stderr)
            time.sleep(1)
    tree = etree.HTML(response.content)
    tbody = tree.xpath('//div[@class="dashboard"]//table/tbody')[0]
    years = tbody.xpath('./tr/td[2]/text()')
    quartiles = tbody.xpath('./tr/td[3]/text()')
    max_year = max(int(y) for y in years)
    return min(quartile for year, quartile in zip(years, quartiles) if int(year) == max_year)

def get_paper_info(doi, topic):
    info = Works().doi(doi)
    authors = ', '.join('**R. Cruz**' if author.get('ORCID', '') == 'http://orcid.org/0000-0002-5189-6228' or author['given'][0] + author['family'] == 'RCruz' else f'{author["given"][0]}. {author["family"]}' for author in info['author'])
    where = info['publisher'] + ' ' + ' - '.join(info['container-title'])
    return {
        'Year': info['published']['date-parts'][0][0],
        'Paper': '[' + info['title'][0] + '](' + info['URL'] + ')\n' + authors + '\n*' + where + '*',
        'Topic': topic,
        'Type': info['type'],
        'Citations': info['is-referenced-by-count'],
        'SJR Rank': get_sjr_rank(where) if info['type'] != 'proceedings-article' else '',
        'CORE Rank': get_core_rank(conference_acronym(where)) if info['type'] != 'journal-article' else '',
    }

papers = [
    ('10.1007/978-3-031-49018-7_40', 'applications'),
    ('10.1007/978-3-031-49018-7_39', 'others'),
    ('10.1007/978-3-031-49018-7_38', 'human-in-the-loop'),
    ('10.1007/978-3-031-36616-1_22', 'human-in-the-loop'),
    ('10.1007/978-3-031-43078-7_43', 'ordinal-losses'),
    ('10.3390/s23063092', 'spatial-resource-efficiency'),
    ('10.1117/12.2679881', 'spatial-resource-efficiency'),
    ('10.1016/j.iswa.2022.200170', 'applications'),
    ('10.3390/math10060980', 'ordinal-losses'),
    ('10.7717/peerj-cs.457', 'ordinal-losses'),
    ('10.1109/ICPR48806.2021.9413004', 'background-invariance'),
    ('10.1109/EMBC.2019.8857385', 'absolute-costs'),
    ('10.1016/j.compeleceng.2019.08.001', 'applications'),
    ('10.1007/978-3-030-30484-3_10', 'others'),
    ('10.1109/IJCNN.2018.8489696', 'iterative-inference'),
    ('10.1109/PRNI.2018.8423960', 'ranking-for-class-imbalance'),
    ('10.1007/s10044-018-0705-4', 'ranking-for-class-imbalance'),
    ('10.1007/978-3-319-59147-6_47', 'absolute-costs'),
    ('10.1007/978-3-319-59147-6_45', 'ranking-for-class-imbalance'),
    ('10.1007/978-3-319-59147-6_46', 'ranking-for-class-imbalance'),
    ('10.1007/978-3-319-58838-4_1', 'ranking-for-class-imbalance'),
    ('10.1109/IJCNN.2016.7727469', 'ranking-for-class-imbalance'),
]
papers = [get_paper_info(*p) for p in tqdm(papers)]

if args.type == 'latex':
    # split papers into types and reduce columns
    for type in sorted(set([p['Type'] for p in papers])):
        out.section('section-publications', f'{type.replace("-", " ").title()} Publications')
        keys = ['Year', 'Paper', 'Citations']
        if type in ('journal-article', 'book-chapter'):
            keys.append('SJR Rank')
        else:
            keys.append('CORE Rank')
        subpapers = [{k: p[k] for k in keys} for p in papers if p['Type'] == type]
        out.table(subpapers, [], [], [], (None, '25em', None, None))
else:  # html
    out.section('section-publications', 'Publications')
    h_index = sum(i+1 <= paper['Citations'] for i, paper in enumerate(sorted(papers, key=lambda x: x['Citations'], reverse=True)))
    out.paragraph(f'My cross-ref h-index: {h_index}')
    out.table(papers, ['Topic', 'Type'], ["int", "str", "str", "str", "int", "str", "str"], ["desc", None, None, None, "desc", "asc", "asc"])

################################## AWARDS ##################################

out.section('section-awards', 'Awards')
out.description([
    ('2022', '[Bosch for Mobility:](https://noticias.up.pt/estudantes-da-u-porto-brilham-em-concurso-de-conducao-autonoma-da-bosch/) My students won Best New Participating Team in an autonomous driving competition'),
    ('2021', '[INESC TEC Outstanding Recognition Award:](https://bip.inesctec.pt/en/especiaisdecorrida/ricardo-cruz-ctm-2/) INESC TEC internal award, reason: maintenance of the HPC infrastructure'),
    ('2021', 'Pedagogic award (voted by students): University of Porto (FEUP)'),
    ('2021', '[Best paper and presentation:](https://noticias.up.pt/investigadores-da-u-porto-dominam-premios-do-recpad-2021/) RECPAD national conference'),
    ('2018', '[INESC TEC Outstanding Recognition Award:](http://bip-archive.inesctec.pt/en/196/fora-de-serie.html) INESC TEC internal award, reason: help organizing workshops'),
    ('2017', 'Kaggle Bronze Medal (competition) and Silver (engagement)'),
])

################################ SUPERVISIONS ################################

table = [
    {'Year': 'on-going', 'Degree': 'MSc', 'Student': 'Diana Teixeira Silva', 'Co-supervisor(s)': '', 'Thesis/Project': 'Quantifying How Deep Implicit Representations Promote Label Efficiency', 'University': 'FEUP'},
    {'Year': 'on-going', 'Degree': 'MSc', 'Student': 'Francisco Gonçalves Cerqueira', 'Co-supervisor(s)': '', 'Thesis/Project': 'Comparative Study on Self-Supervision Methods for Autonomous Driving', 'University': 'FEUP'},
    {'Year': 2024, 'Degree': 'MSc', 'Student': 'Airton Tiago', 'Co-supervisor(s)': 'Jaime Cardoso', 'Thesis/Project': 'Data Augmentation for Ordinal Data', 'University': 'FEUP'},
    {'Year': 2023, 'Degree': 'MSc', 'Student': 'Alankrita Asthana', 'Co-supervisor(s)': '', 'Thesis/Project': 'Iterative Inference for Point-Clouds', 'University': 'TUM'},
    {'Year': 2023, 'Degree': 'MSc', 'Student': 'Rafael Cristino', 'Co-supervisor(s)': 'Jaime Cardoso', 'Thesis/Project': '[Introducing Domain Knowledge to Scene Parsing in Autonomous Driving](https://repositorio-aberto.up.pt/handle/10216/152109)', 'University': 'FEUP'},
    {'Year': 2023, 'Degree': 'MSc', 'Student': 'José Guerra', 'Co-supervisor(s)': 'Luís Teixeira', 'Thesis/Project': '[Uncertainty-Driven Out-of-Distribution Detection in 3D LiDAR Object Detection for Autonomous Driving](https://repositorio-aberto.up.pt/handle/10216/152016) (Internship at Bosch Car Multimedia)', 'University': 'FEUP'},
    {'Year': 2022, 'Degree': 'MSc', 'Student': 'Pedro Silva', 'Co-supervisor(s)': 'Tiago Gonçalves', 'Thesis/Project': '[Human Feedback during Neural Networks Training](https://repositorio-aberto.up.pt/handle/10216/142444)', 'University': 'FEUP'},
    {'Year': 2022, 'Degree': 'MSc', 'Student': 'João Silva', 'Co-supervisor(s)': '', 'Thesis/Project': '[Environment Detection for Railway Applications based on Automotive Technology](https://repositorio-aberto.up.pt/handle/10216/142326) (Internship at Continental)', 'University': 'FEUP'},
    {'Year': 2022, 'Degree': 'MSc', 'Student': 'Ana Bezerra', 'Co-supervisor(s)': 'Joaquim Costa', 'Thesis/Project': '[Phishing Detection with a Machine Learning Net](https://repositorio-aberto.up.pt/handle/10216/147350) (Internship at E-goi)', 'University': 'FCUP'},
    {'Year': 2024, 'Degree': 'BSc', 'Student': 'Eliandro Melo', 'Co-supervisor(s)': '', 'Thesis/Project': 'Resource Efficiency using Deep Q-Learning in Autonomous Driving', 'University': 'FCUP'},
    {'Year': 2024, 'Degree': 'BSc', 'Student': 'Ivo Duarte Simões', 'Co-supervisor(s)': '', 'Thesis/Project': 'Resource Efficiency using PPO in Autonomous Driving', 'University': 'FCUP'},
    {'Year': 2023, 'Degree': 'BSc', 'Student': 'Diana Teixeira Silva', 'Co-supervisor(s)': '', 'Thesis/Project': 'Condition Invariance for Autonomous Driving by Adversarial Learning', 'University': 'FEUP'},
    {'Year': 2022, 'Degree': 'BSc', 'Student': 'Diana Teixeira Silva', 'Co-supervisor(s)': 'Tiago Gonçalves', 'Thesis/Project': 'Semantic Segmentation in Neural Networks using Iterative Visual Attention', 'University': 'FEUP'},
    {'Year': 2022, 'Degree': 'BSc', 'Student': 'Filipe Campos, Francisco Cerqueira, Vasco Alves', 'Co-supervisor(s)': '', 'Thesis/Project': '[Mobile App using Object Detection for Car Driving](https://play.google.com/store/apps/details?id=pt.up.fe.mobilecardriving)', 'University': 'FEUP'},
    {'Year': 2022, 'Degree': 'BSc', 'Student': 'Bruno Gomes, Rafael Camelo', 'Co-supervisor(s)': '', 'Thesis/Project': 'Internship at ANO', 'University': 'FEUP'},
]

if args.type == 'latex':
    # split papers into types and reduce columns
    for degree in ['MSc', 'BSc']:
        out.section('section-supervisions', f'{degree} Supervisions')
        keys = ['Year', 'Student', 'Thesis/Project']
        subtable = [{k: row[k] for k in keys} for row in table if row['Degree'] == degree]
        out.table(subtable, [], [], [], (None, '10em', '25em'))
else:  # html
    out.section('section-supervisions', 'Supervisions')
    out.table(table, ['Degree'], ["str", "str", None, None, None, "str"], ["desc", "desc", None, None, None, "asc"])

##################################### END #####################################

out.paragraph(f'Last update: {datetime.now().strftime("%Y-%m-%d")}')
out.end()
