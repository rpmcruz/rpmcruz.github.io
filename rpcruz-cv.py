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
    venue = ' '.join(paper[1].split('\n')[-1][:-1].split()[:-1])[:-1]
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

    out.text(f'**Impact and Citations**')
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
            out.text(f'**{type.title()} Publications**')
            ix = (0, 1, 4, 5) if type == 'journal' else (0, 1, 4, 7)
            _columns = [columns[i] for i in ix]
            _table = [[row[i] for i in ix] for row in my_papers if row[3] == type]
            sizes = [None, '32em', None, None] if type == 'journal' else [None, '30em', None, '3.5em']
            out.table(_table, _columns, None, sizes)
            out.text(f'Total {count[type]} {type} publications.')
    out.text(f'**{type.title()} Awards**')
    out.description(cv['awards'])

    ix = (0, 2, 4, 5)
    for degree in ['MSc', 'BSc']:
        out.text(f'**{degree} Supervisions**')
        columns = ['Year', 'Student', 'Dissertation' if degree == 'MSc' else 'Project', 'University']
        _table = [[row[i] for i in ix] for row in cv['supervisions'] if row[1] == degree]
        out.table(_table, columns, None, [None, '9em', '23em', None])

    out.text(f'**Jury Partitions**')
    out.description(cv['jury_participation'])

    out.subsection('CMC2. Coordination and implementation of research projects')
    out.text('**Participation in Scientific Projects**')
    out.itemize(cv['scientific_projects'])

    out.subsection('CMC3. Involvement in the scientific and professional communities')
    out.text('**Participation in Scientific Events**')
    out.itemize(cv['scientific_events'])
    out.text('**Collaborations as Editor or Evaluator**')
    out.description(cv['editor_or_evaluator'])

    out.subsection('CMC4. Program for the development of scientific activity')
    out.text('(see the attached program)')

    out.section('VEMP. Pedagogic Merit')
    out.subsection('CEMP1. Pedagogical Projects')
    out.text('As detailed below (CTC4), during my PhD, I organized with my supervisor (Prof. Jaime Cardoso) an activity for the Junior University entitled ``Escondidos nos Dados'' that took place at FEUP. This activity took place for a month, with classes with different children every day, from the 8th and 9th grades.')
    out.subsection('CEMP2. Production of Teaching Materials')
    out.text('For the Fundamentals of Programming UC (under the supervision of Prof João Correia Lopes), beyond helping create many of the exercises, I also developed a website for the submission of weekly assignments and for the exams (the backend is Python/Flask with the database initially in MongoDB and later in PostgreSQL). The website evaluated the code using units tests (some unit tests were public, others were hidden). For the non-graded exercises, after correctly solving the coding exercise, the students could compare their answers with those of the other students and do “likes”. There is also a leaderboard to help gamify the website a little bit.')
    out.text('![](imgs/fproweb/image4.png)')
    out.text('![](imgs/fproweb/image6.png)')
    out.text('![](imgs/fproweb/image5.png)')
    out.text('Beyond that, I was responsible for introducing CodeRunner (a plugin for Moodle that does something similar to my website) in the UC of Algorithms and Data Structures (2021/2022) and participated in the introduction meetings of CodeRunner in the UC of Fundamentals of Programming despite no longer being part of it (in 2022/2023).')
    out.text('Furthermore, I took a lead role in the optional project. This optional project was available for students with excellent grades that were interested in developing small games in PyGame. In exchange, these students were not required to do the weekly assignments. See some of the projects developed by the students here: [](https://www.youtube.com/@joaocorreialopes7558/playlists)')
    out.subsection('CEMP3. Teaching Activity')
    out.text('**Teaching**')
    out.text('The teaching consisted of the pratical lessons (2h-4h per week) and helping with the materials. These courses took place during my PhD (as an Invited Teacher Assistant) and then as a Post-Doc (as an Invited Auxiliary Professor).')
    out.description([(date, item) for date, item in cv['employment'] if 'Professor' in item])
    out.text("In 2021, I received the Pedagogic award (voted by students) from FEUP based on students' inquiries.")
    out.subsection('CEMP4. Program for the development of pedagogical activity')
    out.text('(see the attached program)')

    out.section('VTC. Tasks of Outreach and Economic and Social Enhancement of Knowledge Dimension')
    out.subsection('CTC1. Patents, registration and ownership of rights, development of technical standards and regulations')
    out.text('(nothing to declare)')
    out.subsection('CTC2. Consulting and Study and Development Contracts')
    out.text('(nothing to declare)')
    out.subsection('CTC3. Dissemination of Science and Technology')
    out.text('Public workshops and talks I have organized or participated on:')
    out.itemize(cv['public_workshops_talks'])
    out.subsection('CTC4. Program for the Development of the University Outreach Activity')
    out.itemize(cv['public_outreach'])

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
