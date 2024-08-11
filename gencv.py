import argparse
parser = argparse.ArgumentParser()
parser.add_argument('yaml')
parser.add_argument('format', choices=['latex', 'html'])
args = parser.parse_args()

import out, papers
from papers import get_metrics
from datetime import datetime
import yaml
cv = yaml.safe_load(open(args.yaml))

out = out.Latex() if args.format == 'latex' else out.HTML()
out.begin_document(cv)
out.biography(cv['biography'])

if args.format == 'latex':
    out.section('Skills')
    out.cvitem('', '• ' + ' • '.join(cv['skills']))

out.section('Education')
for entry in cv['education']:
    out.cvitem('**' + str(entry['year']) + '**', '**' + entry['degree'] + '**')
    out.cvitem('Institution', entry['institution'])

out.section('Work Experience')
for entry in cv['employment']:
    out.cventry(entry['dates'], entry['title'], entry['employer'], '', '', entry['details'])

#out.section('Research projects')
#for project in cv['scientific_projects']:
#    out.cvitem(project['when'], project['what'])

#out.section('Participation in Scientific Events')
#for project in cv['scientific_events']:
#    out.cvitem(project['when'], project['what'])

out.section('Publications')

hindices = papers.get_hindices()
out.table_small('h-index', [[str(v) for v in hindices.values()]], hindices.keys())

out.paragraph("Sources for the following metrics: • Impact Factor (IF) as reported by the journal's webpage. • SJR rank quartiles are from Scimago and relate to the subject category closest to machine learning (not necessarily the best quartile). • CORE rank is from ICORE for whatever last year is available for that conference. " + ('• Citation counts come from Crossref. ' if args.format == 'html' else '') + 'Last update: ' + datetime.now().strftime(r'%Y-%m-%d'))

papers = cv['submitted_papers'] + \
    [papers.get_paper_info(paper) for paper in cv['published_papers']]
papers = [dict(paper, **get_metrics(paper)) for paper in papers]
if args.format == 'html':
    rows = []
    for paper in papers:
        title = '[' + paper['title'] + '](' + paper['link'] + ')' if 'link' in paper else paper['title']
        rows.append([paper['year'], paper['authors'] + ', "' + title + '", *' + paper['where'] + '*',
            paper['type'], paper.get('citations', ''), paper.get('IF', ''), paper.get('SJR', ''), paper.get('CORE', '')])
    columns = ['Year', 'Paper', 'Type', 'Citations', 'IF', 'SJR Rank', 'CORE Rank']
    types = ['sort', 'text', 'filter', 'sort', 'sort', 'sort', 'sort']
    out.table_large(rows, columns, types)
else:
    for type, title in [('journal', 'Journal Publications'), ('conference', 'International Conference Proceedings')]:
        out.subsection(title)
        for paper in papers:
            if paper['type'] == type:
                metrics = ', '.join(f'{metric}={paper[metric]}' for metric in ('IF', 'SJR', 'CORE') if metric in paper and paper[metric] != 'n/a')
                if paper.get('CORE', '').startswith('A') or paper.get('SJR') == 'Q1':
                    metrics = ', **' + metrics + '**'
                elif metrics:
                    metrics = ', ' + metrics
                text = paper['authors'] + ', "' + paper['title'] + '", *' + paper['where'] + '*' + metrics + (' [](' + paper['link'] +')' if 'link' in paper else '')
                out.cvitem(str(paper['year']), text)

out.section('Supervisions')
for type in ['MSc Dissertation', 'BSc Project', 'Internship']:
    out.subsection(type)
    for entry in cv['supervisions']:
        if entry['type'] == type:
            title = '[' + entry['title'] + '](' + entry['link'] + ')' if 'link' in entry else entry['title']
            note = ' (with co-supervisor: ' + entry['cosupervisor'] + ')' if 'cosupervisor' in entry else ''
            text = entry['student'] + ', "' + title + '", *' + entry['university'] + '*' + note
            out.cvitem(str(entry['date']), text)

out.end_document()
