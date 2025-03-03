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
if args.format == 'html':
    # for the public, show my work email
    cv['contact']['email'] = 'rpcruz@fe.up.pt'
out.begin_document(cv)
out.paragraph(cv['biography'])

if args.format == 'html':
    print('<div style="border:1px solid;padding:2px;background-color:yellow">If you are a student that would like to do research for a project, masters dissertation or PhD, drop me <a href="mailto:rpcruz@fe.up.pt">an email</a>.</div>')
if args.format == 'latex':
    out.section('Skills')
    out.cvitem('', '• ' + ' • '.join(cv['skills']))

    out.section('Education')
    for entry in cv['education']:
        out.cvitem('**' + str(entry['year']) + '**', '**' + entry['degree'] + '**')
        out.cvitem('', entry['institution'])

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

if args.format != 'html':
    hindices = papers.get_hindices()
    out.table_small('h-index', [[str(v) for v in hindices.values()]], hindices.keys())

out.paragraph("Sources for the following metrics: • Impact Factor (IF) as reported by the journal's webpage. • SJR rank quartiles are from Scimago and best quartile is chosen when multiple categories exist. • CORE rank is from ICORE for whatever last year is available for that conference. " + ('• Citation counts come from Crossref. ' if args.format == 'html' else '') + 'Last update: ' + datetime.now().strftime(r'%Y-%m-%d'))

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
            note = ' (main supervisor: ' + entry['supervisor'] + ', co-supervisor: R. Cruz)' if 'supervisor' in entry else ''
            text = entry['student'] + ', "' + title + '", *' + entry['institution'] + '*' + note
            out.cvitem(str(entry['date']), text)

out.end_document()
