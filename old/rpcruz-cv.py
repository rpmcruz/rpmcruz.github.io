import argparse
parser = argparse.ArgumentParser()
parser.add_argument('type', choices=['html', 'latex'])
parser.add_argument('--feup', action='store_true')
args = parser.parse_args()

import datetime
from tqdm import tqdm
import yaml
import papers, out

cv = yaml.safe_load(open('rpcruz-cv.yaml'))

if args.type == 'latex':
    cv['contacts'].insert(1, ('profile-website', 'rpmcruz.github.io', 'https://rpmcruz.github.io/'))
else:  # html
    cv['contacts'].append(('profile-pdf', 'PDF', 'https://rpmcruz.github.io/rpcruz-cv.pdf'))

# add citation counts
my_papers = [papers.get_paper_info(*p, frozenset(cv['categories'])) for p in tqdm(cv['papers'])]
count = {}
for p in my_papers:
    count[p[3]] = count.get(p[3], 0)+1

# add more information regarding venues
for paper in cv['manual_papers']:
    venue = ' '.join(paper[1].split('\n')[-1][:-1].split()[:-1])[1:-1]
    paper += ['']*4
    if paper[3] == 'journal':
        paper[5] = papers.get_impact_factor(venue)
        paper[6] = papers.get_sjr_rank(venue, frozenset(cv['categories']))
    else:
        paper[7] = papers.get_core_rank(venue)

h_index = sum(i+1 <= paper[4] for i, paper in enumerate(sorted(my_papers, key=lambda x: x[4], reverse=True)))
total_citations = sum(x[4] for x in my_papers)
my_papers = cv['manual_papers'] + my_papers
google_scholar_hindex = papers.get_scholar_hindex()

out = getattr(out, args.type.title())()

if args.feup:
    out.begin(cv['name'])
    out.contacts(cv['contacts'])
    out.text(cv['biography'])

    out.section('VMC. Scientific Merit')
    out.subsection('CMC1. Scientific Production')

    out.table([['h-index', f'{google_scholar_hindex}', '6', '4']], ['', '[Google Scholar](https://scholar.google.pt/citations?user=pSFY_gQAAAAJ)', '[Scopus](https://www.scopus.com/authid/detail.uri?authorId=57192670388)', '[Web of Science](https://www.webofscience.com/wos/author/record/IQV-2746-2023)'], None, [None]*4)

    out.text('During my PhD, I have mostly published on conferences because it was a common practice in the research group I was inserted into. During my post-doc, I am trying to compensate with more journal publications, and conferences mostly for student work I am supervising.')
    out.text('With regard to authorship order, first or second author means there was a major contribution on my part. I have been using last author for supervisions, or penultimate if a co-supervision.')

    columns = ['Year', 'Paper', 'Topic', 'Type', 'Citations', 'IF', 'SJR Rank', 'CORE Rank']
    # split papers into types and reduce columns
    for type in ['journal', 'conference']:
        out.subsubsection(f'{type.title()} Publications')
        ix = [1]
        _columns = ['#'] + [columns[i] for i in ix] + ['Metrics']
        _table = []
        for row in my_papers:
            if row[3] == type:
                metrics = f'citations={row[4]}' if row[4] != '' else ''
                if type == 'journal':
                    metrics += ('\n' if row[4] != '' else '') + f'IF={row[5]}'
                    metrics += f'\nSJR==={row[6]}=='
                else:
                    metrics += f'\nCORE RANK={row[7]}'
                nbr = ('' if len(_table) < len(cv['manual_papers']) else str(len(_table)-len(cv['manual_papers'])+1)) if type == 'journal' else str(len(_table)+1)
                paper = row[1]
                paper = paper.replace('IEEE Transactions', '==IEEE Transactions==')
                _table.append([nbr, paper, metrics])
        sizes = [None, '33em', '8em']
        colors = ['lightgray']*len(cv['manual_papers']) + [None]*(len(my_papers)-len(cv['manual_papers'])) if type == 'journal' else None
        out.table(_table, _columns, None, sizes, colors)
        if type == 'journal':
            out.itemize([
                '==Highlight==: the features most valorized by the edital',
                'Journal paper #3 is an extension of conference paper #2',
                'Journal paper #8 is an extension of conference paper #15',
            ])
    out.text(f"Sources (last update: {datetime.datetime.now().strftime('%Y-%m-%d')}): • Citation counts are from Crossref. • Impact Factor (IF) comes from each journal's webpage. • SJR rank quartiles are from Scimago and relate to the subject category closest to machine learning (not necessarily the best quartile). • CORE rank is from ICORE for whatever last year is available for that conference.")

    out.subsection('CMC2. Coordination and implementation of research projects')
    out.itemize(cv['scientific_projects'])

    out.subsection('CMC3. Involvement in the scientific and professional communities')
    out.subsubsection('Participation in Scientific Events')
    out.description(cv['scientific_events'])
    out.subsubsection('Collaborations as Editor or Evaluator')
    out.description(cv['editor_or_evaluator'])
    out.subsubsection('Jury Partitions')
    out.description(cv['jury_participation'])
    out.subsubsection('Awards')
    out.description(cv['awards'])

    out.section('VEMP. Pedagogic Merit')
    out.subsection('CEMP1. Pedagogical Projects')
    out.itemize([
        'In 2018, during my PhD, I organized an activity called “Escondidos nos Dados” for Junior University together with my supervisor (Prof. Jaime Cardoso). The Junior University is an opportunity that the University of Porto gives children to get to know and do activities at the university. This activity took place for a month, with classes with different children every day, from the 8th and 9th grades. The website archives is not working, but this link describes an award I received from INESC TEC for organizing these activities, among others. [](http://bip-archive.inesctec.pt/196/fora-de-serie.html)',
        'In 2018 (and up to 2022), I collaborated with Prof João Correia Lopes in FEUP informatics first-year course “Fundamental of Programming“ (FP). This was the first time Python was taught in the course. I took a major role in guiding the best students to develop an optional project that consisted in each student developing a game [](https://www.youtube.com/@joaocorreialopes7558/playlists). Furthermore, I developed a website for the submission of weekly assignments and for the exams (Python/Flask/PostgreSQL), containing some gamification elements such as a leaderboard and likes, which was a key component of the course. The website evaluated the code using units tests. Non-graded exercises were also provided for training for which many I contributed. When CodeRunner was introduced in Moodle, I helped the transition for the course.'])
    #out.text('![](imgs/fproweb/image4.png)')
    #out.text('![](imgs/fproweb/image6.png)')
    #out.text('![](imgs/fproweb/image5.png)')

    out.text('I have also participated in the following masters dissertations and bachelors final projects:')
    ix = (0, 2, 4, 5)
    for degree in ['MSc', 'BSc']:
        out.text(f'**{degree} Supervisions**')
        columns = ['Year', 'Student', 'Dissertation' if degree == 'MSc' else 'Project', 'University']
        _table = [[row[i] for i in ix] for row in cv['supervisions'] if row[1] == degree]
        out.table(_table, columns, None, [None, '9em', '23em', None])

    out.subsection('CEMP2. Production of Teaching Materials')
    out.text('During my time as an Invited Assistant and Invited Auxiliary Professor, I contributed with exercises, especially in the FP informatics course, as discussed above.')

    out.subsection('CEMP3. Teaching Activity')
    out.description([(date, item) for date, item in cv['employment'] if 'Professor' in item or 'Teacher' in item])
    out.text("In 2021, I received the **FEUP Pedagogic Award** (voted by students) based on students' inquiries.")

    out.section('VTC. Tasks of Outreach and Economic and Social Enhancement of Knowledge Dimension')
    out.subsection('CTC1. Patents, registration and ownership of rights, development of technical standards and regulations')
    out.text('During the THEIA project, a patent was proposed that is currently being evaluated. Title: **Multi-task Learning -- Architecture Distillation**. Authors: Diogo Carneiro (Bosch), Ricardo Cruz (UP)')
    out.subsection('CTC2. Consulting and Study and Development Contracts')
    out.text('(nothing to declare)')
    out.subsection('CTC3. Dissemination of Science and Technology')
    out.text('Beyond the scientific conferences previously mentioned in CMC3, I have organized or participated on the following talks and workshops that were given for a broader public:')
    out.itemize(cv['public_workshops_talks'])

    out.section('VTC. Tasks of Outreach and Economic and Social Enhancement of Knowledge Dimension')
    out.text('Please see the files in attachment.')

    #out.subsection('CTC4. Program for the Development of the University Outreach Activity')
    #out.itemize(cv['public_outreach'])

else:  # normal CV
    out.begin(cv['name'])
    out.contacts(cv['contacts'])
    out.text(cv['biography'])

    if args.type == 'latex':
        out.section('Education', 'section-education')
        out.description(cv['education'])
        out.section('Employment', 'section-employment')
        out.description(cv['employment'])

    if args.type == 'latex':
        out.section('Impact and Citations', 'section-scientific-impact')
    else:
        out.section('Publications', 'section-publications')
    out.itemize([
        f'Google Scholar h-index: **{google_scholar_hindex}** ({datetime.datetime.now().strftime("%Y-%m-%d")})',
        f'Crossref h-index: **{h_index}** with **{total_citations}** total citations ({datetime.datetime.now().strftime("%Y-%m-%d")})',
        'Best oral paper: [2021 RECPAD conference](https://noticias.up.pt/investigadores-da-u-porto-dominam-premios-do-recpad-2021/)',
    ])
    out.text(f"Sources (last update: {datetime.datetime.now().strftime('%Y-%m-%d')}): • Citation counts are from Crossref. • Impact Factor (IF) comes from each journal's webpage. • SJR rank quartiles are from Scimago and relate to the subject category closest to machine learning (not necessarily the best quartile). • CORE rank is from ICORE for whatever last year is available for that conference.")

    columns = ['Year', 'Paper', 'Topic', 'Type', 'Citations', 'IF', 'SJR Rank', 'CORE Rank']
    if args.type == 'latex':
        # split papers into types and reduce columns
        for type in ['journal', 'conference']:
            out.section(f'{type.title()} Publications', 'section-publications')
            ix = (0, 1, 4, 5) if type == 'journal' else (0, 1, 4, 7)
            _columns = [columns[i] for i in ix]
            _table = [[row[i] for i in ix] for row in my_papers if row[3] == type]
            sizes = [None, '32em', None, None] if type == 'journal' else [None, '30em', None, '3.5em']
            out.table(_table, _columns, None, sizes)
            out.text(f'Total {count[type]} {type} publications.')
    else:  # html
        out.table(my_papers, columns, ['sort', 'text', 'filter', 'filter', 'sort', 'sort', 'sort', 'sort'], None)

    if args.type == 'latex':
        # split supervisions into types and reduce columns
        ix = (0, 2, 4, 5)
        for degree in ['MSc', 'BSc']:
            out.section(f'{degree} Supervisions', 'section-supervisions')
            columns = ['Year', 'Student', 'Dissertation' if degree == 'MSc' else 'Project', 'University']
            _table = [[row[i] for i in ix] for row in cv['supervisions'] if row[1] == degree]
            out.table(_table, columns, None, [None, '9em', '23em', None])
    else:  # html
        columns = ['Year', 'Degree', 'Student', 'Co-supervisor(s)', 'Dissertation/Project', 'University']
        out.section('Supervisions', 'section-supervisions')
        out.table(cv['supervisions'], columns, ['sort', 'filter', 'text', 'text', 'text', 'sort'], None)

    if args.type == 'latex':
        out.section(f'Jury Participation', 'section-jury-participation')
        out.description(cv['jury_participation'])

    if args.type == 'html':
        out.section('Education', 'section-education')
        out.description(cv['education'])
        out.section('Employment', 'section-employment')
        out.description(cv['employment'])

    out.section('Awards', 'section-awards')
    out.description(cv['awards'])

if args.type == 'html':
    out.text(f'Last update: {datetime.datetime.now().strftime("%Y-%m-%d")}')
out.end()
