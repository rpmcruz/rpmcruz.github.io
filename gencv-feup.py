import argparse
parser = argparse.ArgumentParser()
parser.add_argument('yaml')
args = parser.parse_args()

import out, papers
from papers import get_metrics
from datetime import datetime
import yaml
cv = yaml.safe_load(open(args.yaml))

out = out.FEUP()
out.begin_document(cv)
out.biography(cv['biography'])

# https://sigarra.up.pt/spup/pt/noticias_geral.ver_noticia?p_nr=76889
# https://sigarra.up.pt/spup/pt/noticias_geral.ver_noticia?p_nr=76909

out.part('VMC. Scientific Merit')

out.section('CMC1. Scientific Production')

out.subsection('Publications')

hindices = papers.get_hindices()
out.table_small('h-index', [[str(v) for v in hindices.values()]], hindices.keys())

out.paragraph('During my PhD, I have mostly published on conferences because it was a common practice in the research group I was inserted into. During my post-doc, I am trying to compensate with more journal publications, and conferences mostly for student work I am supervising.')
out.paragraph('With regard to authorship order, first or second author means there was a major contribution on my part. I have been using last author for supervisions, or penultimate if a co-supervision.')

papers = cv['submitted_papers'] + \
    [papers.get_paper_info(paper) for paper in cv['published_papers']]
papers = [dict(paper, **get_metrics(paper)) for paper in papers]
for type, title in [('journal', 'Journal Publications'), ('conference', 'International Conference Proceedings')]:
    out.subsection(title)
    i = 0
    for paper in papers:
        if paper['type'] == type:
            metrics = ', '.join(f'{metric}={paper[metric]}' for metric in ('IF', 'SJR', 'CORE') if metric in paper and paper[metric] != 'n/a')
            if paper.get('CORE', '').startswith('A') or paper.get('SJR') == 'Q1':
                metrics = ', ==' + metrics + '=='
            elif metrics:
                metrics = ', ' + metrics
            if 'citations' in paper and paper['citations'] > 0:
                metrics += ' (cited ' + str(paper['citations']) + ' times)'
            where = paper['where']
            if 'IEEE Transactions' in where:
                where = where.replace('IEEE Transactions', '==IEEE Transactions==')
            text = paper['authors'] + ', "' + paper['title'] + '", *' + where + '*' + metrics + (' [](' + paper['link'] +')' if 'link' in paper else '')
            if 'doi' in paper:
                if paper['doi'].lower() in cv['best_last_5_years'] and paper['doi'].lower() in cv['best_overall']:
                    text = r'\starnum{5}{red} ' + text
                elif paper['doi'].lower() in cv['best_last_5_years']:
                    text = r'\starnum{5}{yellow} ' + text
                elif paper['doi'].lower() in cv['best_overall']:
                    text = r'\starnum{\phantom{5}}{red} ' + text
            if 'citations' in paper:
                out.cvitem('**' + str(i+1) + r'.** ' + str(paper['year']), text)
                i += 1
            else:
                out.cvitem('[submitted]', text)
out.itemize([
    'In ==highlight== features valued by the notice',
    r'\starnum{5}{red} = best 5 years and overall; \starnum{5}{yellow} = best 5 years; \starnum{\phantom{5}}{red} = best overall (justification for these choices in attachment)',
    r'Journal paper #3 is an extension of conference paper #2',
    r'Journal paper #8 is an extension of conference paper #15',
])
out.paragraph("Sources for the above metrics: • Impact Factor (IF) as reported by the journal's webpage. • SJR rank quartiles are from Scimago and relate to the subject category closest to machine learning (not necessarily the best quartile). • CORE rank is from ICORE for whatever last year is available for that conference. • Citation counts come from Crossref. Last update: " + datetime.now().strftime(r'%Y-%m-%d'))

out.section('CMC2. Coordination and implementation of research projects')
for project in cv['scientific_projects']:
    out.cvitem(project['when'], project['what'])

out.section('CMC3. Involvement in the scientific and professional communities')
out.subsection('Participation in Scientific Events')
for project in cv['scientific_events']:
    out.cvitem(project['when'], project['what'])
out.subsection('Collaborations as Editor or Evaluator')
for project in cv['editor_or_evaluator']:
    out.cvitem(project['when'], project['what'])
out.subsection('Jury Participations')
for project in cv['jury_participation']:
    out.cvitem(project['when'], project['what'])
out.subsection('Awards')
for project in cv['awards']:
    out.cvitem(project['when'], project['what'])

################################################################################

out.part('VEMP. Pedagogical Experience and Merit')

out.section('CEMP1. Pedagogical projects')
out.itemize([
    'In 2018, during my PhD, I organized an activity called “Escondidos nos Dados” for Junior University together with my supervisor (Prof. Jaime Cardoso). The Junior University is an opportunity that the University of Porto gives children to get to know and do activities at the university. This activity took place for a month, with classes with different children every day, from the 8th and 9th grades. The website archives is not working, but this link describes an award I received from INESC TEC for organizing these activities, among others. [](http://bip-archive.inesctec.pt/196/fora-de-serie.html)',
    'In 2018 (and up to 2022), I collaborated with Prof João Correia Lopes in FEUP informatics first-year course “Fundamental of Programming“ (FP). This was the first time Python was taught in the course. I took a major role in guiding the best students to develop an optional project that consisted in each student developing a game [](https://www.youtube.com/@joaocorreialopes7558/playlists). Furthermore, I developed a website for the submission of weekly assignments and for the exams (Python/Flask/PostgreSQL), containing some gamification elements such as a leaderboard and likes, which was a key component of the course. The website evaluated the code using units tests. Non-graded exercises were also provided for training for which many I contributed. When CodeRunner was introduced in Moodle, I helped the transition for the course.'
])
out.paragraph('I have also participated in the following masters dissertations and bachelors final projects:')
for type in ['MSc Dissertation', 'BSc Project', 'Internship']:
    out.subsection(type)
    for entry in cv['supervisions']:
        if entry['type'] == type:
            title = '[' + entry['title'] + '](' + entry['link'] + ')' if 'link' in entry else entry['title']
            note = ' (with co-supervisor: ' + entry['cosupervisor'] + ')' if 'cosupervisor' in entry else ''
            text = entry['student'] + ', "' + title + '", *' + entry['university'] + '*' + note
            out.cvitem(str(entry['date']), text)

out.section('CEMP2. Production of pedagogical material')
out.paragraph('During my time as an Invited Assistant and Invited Auxiliary Professor, I contributed with exercises, especially in the FP informatics course, as discussed above.')

out.section('CEMP3. Teaching activity')
for entry in cv['employment']:
    if 'Professor' in entry['title'] or 'Teacher' in entry['title']:
        out.cventry(entry['dates'], entry['title'], entry['employer'], '', '', entry['details'])
out.paragraph("In 2021, I received the **FEUP Pedagogic Award** (voted by students) based on students' inquiries.")

################################################################################

out.part('VTC. Economic and Social Valorisation of Knowledge')

out.section('CTC1. Patents, registration, and ownership of rights, development of technical standards and legislation')
out.paragraph('Recently, during the THEIA project, a patent was proposed that is currently being evaluated. Title: **Multi-task Learning -- Architecture Distillation**. Authors: Diogo Carneiro (Bosch), Ricardo Cruz (UP)')
out.section('CTC2. Consulting services and study and development contracts')
out.paragraph('(nothing to declare)')
out.section('CTC3. Dissemination of science and technology ')
out.paragraph('Beyond the scientific conferences previously mentioned in CMC3, I have organized or participated on the following talks and workshops that were given for a broader public:')
for entry in cv['public_workshops_talks']:
    out.cvitem(entry['when'], entry['what'])

################################################################################

out.part('PCP. Scientific/Pedagogical and Extension Programme')
out.paragraph('Please see the files in attachment.')

out.end_document()