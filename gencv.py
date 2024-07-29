import argparse
parser = argparse.ArgumentParser()
parser.add_argument('yaml')
parser.add_argument('format', choices=['latex', 'html'])
args = parser.parse_args()

import out, papers
from papers import get_metrics
import yaml
cv = yaml.safe_load(open(args.yaml))

out = out.Latex() if args.format == 'latex' else out.HTML()
out.begin_document(cv)
out.biography(cv['biography'])

# add Research Interests (itemize)?

out.section('Education')
for entry in cv['education']:
    out.cvitem('**' + str(entry['year']) + '**', '**' + entry['degree'] + '**')
    out.cvitem('Institution', entry['institution'])

out.section('Work Experience')
for entry in cv['employment']:
    out.cventry(entry['dates'], entry['title'], entry['employer'], '', '', entry['details'])

out.section('Publications')
papers = cv['submitted_papers'] + \
    [papers.get_paper_info(paper) for paper in cv['published_papers']]
papers = [dict(paper, **get_metrics(paper)) for paper in papers]

if args.format == 'html':
    rows = [[paper['year'], paper['authors'] + ', "' + paper['title'] + '", *' + paper['where'] + '*',
        paper['type'], paper.get('citations', ''), paper.get('IF', ''), paper.get('SJR', ''), paper.get('CORE', '')] for paper in papers]
    columns = ['Year', 'Paper', 'Type', 'Citations', 'IF', 'SJR Rank', 'CORE Rank']
    types = ['sort', 'text', 'filter', 'sort', 'sort', 'sort', 'sort']
    out.table(rows, columns, types)
else:
    for type, title in [('conference', 'International Conference Proceedings'), ('journal', 'Journal Publications')]:
        out.subsection(title)
        for paper in papers:
            if paper['type'] == type:
                metrics = ', '.join(f'{metric}={paper[metric]}' for metric in ('IF', 'SJR', 'CORE') if metric in paper and paper[metric] != 'n/a')
                if metrics:
                    metrics = ', **' + metrics + '**'
                text = paper['authors'] + ', "' + paper['title'] + '", *' + paper['where'] + '*' + metrics
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