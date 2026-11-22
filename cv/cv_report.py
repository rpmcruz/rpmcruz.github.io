import argparse
parser = argparse.ArgumentParser()
parser.add_argument('xml')
args = parser.parse_args()

from unidecode import unidecode
from lxml import etree
import yaml
import re
import helper

extras = yaml.safe_load(open(f'extras/{args.xml[:-3]}yaml'))

def convert_markdown(text, newline=r'\\'):
    text = re.sub(r'\[([^\]]*?)\]\(([^\s]*?)\)', r'\1 \\href{\2}{\\includegraphics[width=0.8em]{icons/link.pdf}}', text)  # links
    text = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', text)  # bold
    text = re.sub(r'\*(.*?)\*', r'\\textit{\1}', text)  # italic
    text = re.sub(r'__(.*?)__', r'\\underline{\1}', text)  # underline
    text = re.sub(r'\=\=(.*?)\=\=', r'\\hl{\1}', text)  # highlight
    text = text.replace('&', r'\&').replace('~', r'$\sim$').replace('#', r'\#')  # escape symbols
    text = text.replace('\n', newline + '\n')  # force breaklines
    text = re.sub(r'"(.*?)"', r"``\1''", text)  # quotes
    return text

def write_begin_document(name, contacts, resume):
    print(r'\documentclass{article}')
    print(r'\usepackage[margin=2cm]{geometry}')
    print(r'\usepackage[colorlinks=true, linkcolor=blue, urlcolor=blue]{hyperref}')
    print(r'\usepackage{graphicx}')
    print(r'\setlength\parindent{0pt}  % no indent')
    print(r'\setlength{\parskip}{4pt}  % space between paragraphs')
    print(r'\usepackage{enumitem}')
    print(r'\setlist{itemsep=0pt, parsep=0pt, topsep=0pt}')
    print(r'\usepackage{titlesec}  % change \section look')
    print(r'\titleformat{\section}{\normalfont\Large\scshape}{}{0pt}{}[{\titlerule[0.8pt]}]')
    print(r'\titleformat{\subsection}{\normalfont\large\scshape}{}{0pt}{}[\vspace{-1ex}\hbox to 15.2cm{\leaders\hbox to 5pt{\hss . \hss}\hfil}]')
    print(r'\titleformat{\subsubsection}{\normalfont\scshape}{}{0pt}{}')
    print(r'\renewcommand{\thesection}{}  % no section numbers')
    print(r'\renewcommand{\thesubsection}{}  % no section numbers')
    print(r'% header and footer')
    print(r'\usepackage{lastpage}  % defines \pageref{LastPage}')
    print(r'\usepackage{fancyhdr}')
    print(r'\pagestyle{fancy}')
    print(r'\renewcommand{\headrulewidth}{0pt}  % remove head line')
    print(r'\makeatletter\let\ps@plain\ps@fancy\makeatother  % first page equal to rest')
    print(r'\fancyhead{}')
    print(r'\fancyfoot[L]{\scriptsize Last update: \today}')
    print(r'\fancyfoot[C]{}')
    print(r'\fancyfoot[R]{\scriptsize Page \thepage\ of \pageref{LastPage}}')
    print(r'% pontos no table of contents')
    print(r'\usepackage{tocloft}\renewcommand{\cftsecleader}{\cftdotfill{\cftdotsep}}\renewcommand{\cftsubsecdotsep}{\cftnodots}\setlength{\cftbeforesecskip}{-.5ex}')
    print(r'\begin{document}')
    print(f'{{\\Large {name}}}', end='\n\n')
    print(r'\noindent{\small')
    links = {'email': 'mailto:', 'ciencia-id': 'https://www.cienciavitae.pt/portal/en/',
        'orcid-id': 'https://orcid.org/', 'google-scholar-id': 'https://scholar.google.com/citations?user='}
    for icon, value in contacts.items():
        link = links[icon] + value
        value = value.replace('_', r'\_')
        print(f'\\raisebox{{-0.25\\height}}{{\\includegraphics[width=0.5cm]{{icons/{icon}.pdf}}}} \\href{{{link}}}{{{value}}} ')
    print('}\n')
    print(r'\par\noindent\rule{\textwidth}{0.4pt}', end='\n\n')
    print(resume, end='\n\n')
    print(r'\setcounter{tocdepth}{2}\tableofcontents')
    print(r'\par\noindent\rule{\textwidth}{0.4pt}', end='\n\n')

def write_end_document():
    print(r'\end{document}')

def write_section(title):
    print(f'\\section{{{title}}}')

def write_subsection(title):
    print(f'\\subsection{{{title}}}')

def write_subsubsection(title):
    print(f'\\subsubsection{{{title}}}')

def write_item(label, item, large_label=True):
    percent = 0.1 if large_label else 0.04
    print(r'\begin{minipage}[t]{' + str(percent) + r'\linewidth}')
    print(convert_markdown(label))
    print(r'\end{minipage}%')
    print(r'\begin{minipage}[t]{' + str(1-percent) + r'\linewidth}')
    print(convert_markdown(item))
    print(r'\end{minipage}')
    print()

def write_item_with_bullets(label, item, bullets, large_label=True):
    percent = 0.1 if large_label else 0.04
    print(r'\begin{minipage}[t]{' + str(percent) + r'\linewidth}')
    print(convert_markdown(label))
    print(r'\end{minipage}%')
    print(r'\begin{minipage}[t]{' + str(1-percent) + r'\linewidth}')
    print(convert_markdown(item))
    write_bullets(bullets)
    print(r'\end{minipage}')
    print()

def write_bullets(items):
    print(r'\begin{itemize}')
    for item in items:
        print(r'\item ' + item)
    print(r'\end{itemize}')

def write_table(headers, rows):
    print(r'\begin{tabular}{|l|' + ('r|'*(len(headers)-1)) + '}')
    print(r'\hline')
    print(' & '.join(headers) + r' \\')
    print(r'\hline')
    for row in rows:
        print(' & '.join(row) + r' \\')
    print(r'\hline')
    print(r'\end{tabular}')

def write_markdown(markdown):
    print(convert_markdown(markdown))
    print()

tree = etree.parse(args.xml)
root = helper.strip_namespaces(tree.getroot())
scholar_refs = helper.get_scholar_refs()

#print(etree.tostring(root, pretty_print=True, encoding='unicode'))

name = root.xpath('//person-info/full-name/text()')[0]
resume = root.xpath('//resume/text()')[0]

email = root.xpath('//email/email-address/text()')[0]
identifiers = root.xpath('//author-identifiers')[0]
identifiers = {unidecode(type.text.lower().replace(' ', '-')): value.text for type, value in identifiers}
identifiers = {'email': email, **identifiers}

write_begin_document(name, identifiers, resume)

write_section(r'Research (120)')


write_section(r'Teaching (130)')
write_section(r'Knowledge Transfer (100)')


# [nix-shell:~/projs/website/gencv]$ xmlstarlet el -u 3915-392E-21D4.xml | awk -F/ 'NF<=2'
# curriculum:curriculum/degree:degrees
# curriculum:curriculum/distinction:distinctions
# curriculum:curriculum/employment:employments
# curriculum:curriculum/funding:fundings
# curriculum:curriculum/groups:groups
# curriculum:curriculum/identifying-info:identifying-info
# curriculum:curriculum/output:outputs
# curriculum:curriculum/service:services

print(r'\begin{enumerate}')
for distinction in root.find('distinctions'):
    print(r'\item '
        + distinction.xpath('.//effective-date/text()')[0] + ' '
        + distinction.xpath('.//distinction-type/text()')[0] + ' '
        + distinction.xpath('.//distinction-name/text()')[0] + ' '
        + '(' + ', '.join(distinction.xpath('.//institution-name/text()')) + r')\newline '
        + distinction.xpath('.//description/text()')[0]
    )
print(r'\end{enumerate}')

print(r'\begin{enumerate}')
for output in root.find('outputs'):
    type = output.xpath('.//output-type/text()')[0]
    if type == 'Artigo em conferência':
        date = output.xpath('.//presentation-date/@year')[0] + '/' + output.xpath('.//presentation-date/@month')[0]
        title = output.xpath('.//paper-title/text()')[0]
        url = output.xpath('.//url/text()')[0]
        where = output.xpath('.//proceedings-title/text()')[0]
        desc = ', '.join(output.xpath('.//author/text()'))
    if type == 'Artigo em revista':
        date = output.xpath('.//publication-date/@year')[0]
        title = output.xpath('.//article-title/text()')[0]
        url = output.xpath('.//url/text()')[0]
        where = output.xpath('.//journal/text()')[0]
        desc = ', '.join(output.xpath('.//author/text()'))
    if type == 'Capítulo de livro':
        date = output.xpath('.//publication-year/text()')[0]
        title = output.xpath('.//chapter-title/text()')[0]
        url = output.xpath('.//url/text()')[0]
        where = None
        desc = ', '.join(output.xpath('.//author/text()'))
    if type == 'Livro':
        date = output.xpath('.//publication-year/text()')[0]
        title = output.xpath('.//title/text()')[0]
        url = output.xpath('.//url/text()')[0]
        where = output.xpath('.//volume/text()')[0]
        desc = ', '.join(output.xpath('.//author/text()'))
    if type == 'Poster em conferência':
        date = output.xpath('.//conference-date/@year')[0] + '/' + output.xpath('.//conference-date/@month')[0]
        title = output.xpath('.//title/text()')[0]
        url = output.xpath('.//url/text()')[0]
        where = output.xpath('.//conference-name/text()')[0]
        desc = ', '.join(output.xpath('.//author/text()'))
    if type == 'Resumo em conferência':
        date = output.xpath('.//conference-date/@year')[0] + '/' + output.xpath('.//conference-date/@month')[0]
        title = output.xpath('.//article-title/text()')[0]
        url = output.xpath('.//url/text()')[0]
        where = output.xpath('.//conference-name/text()')[0]
        desc = ', '.join(output.xpath('.//author/text()'))
    print(r'\item '
        + date + ' '
        + type + ' '
        + title + ' '
        + ('[](' + url + ') ' if url != None else '')
        + ('(' + where + ')' if where != None else '') + r'\newline '
        + desc
    )
print(r'\end{enumerate}')

print(r'\begin{enumerate}')
for output in root.find('services'):
    type = output.xpath('.//service-category/text()')[0]
    if type == 'Orientação':
        date = output.xpath('.//start-date/@year')[0] + '/' + output.xpath('.//start-date/@month')[0] + '--' \
            + output.xpath('.//end-date/@year')[0] + '/' + output.xpath('.//end-date/@month')[0]
        title = output.xpath('.//thesis-title/text()')[0]
        where = output.xpath('.//degree-subject/text()')[0]
        desc = output.xpath('.//student-name/text()')[0]
        role = output.xpath('.//supervisory-type/text()')[0]
    if type == 'Organização de evento':
        date = output.xpath('.//event-start-date/@year')[0] + '/' + output.xpath('.//event-start-date/@month')[0] + '--' \
            + output.xpath('.//event-end-date/@year')[0] + '/' + output.xpath('.//event-end-date/@month')[0]
        title = output.xpath('.//administrative-role/text()')[0]
        where = output.xpath('.//event-description/text()')[0]
        desc = None
        role = None
    if type == 'Participação em evento':
        date = output.xpath('.//event-start-date/@year')[0] + '/' + output.xpath('.//event-start-date/@month')[0] + '--' \
            + output.xpath('.//event-end-date/@year')[0] + '/' + output.xpath('.//event-end-date/@month')[0]
        title = output.xpath('.//event-description/text()')[0]
        where = output.xpath('.//event-name/text()')[0]
        desc = None
        role = None
    if type == 'Júri de grau académico':
        date = output.xpath('.//date/@year')[0] + '/' + output.xpath('.//date/@month')[0]
        title = output.xpath('.//theme/text()')[0]
        where = output.xpath('.//institution-name/text()')[0]
        desc = output.xpath('.//student-name/text()')[0]
        role = output.xpath('.//examination-role/text()')[0]
    if type == 'Comissão de avaliação':
        date = output.xpath('.//start-date/@year')[0] + '/' + output.xpath('.//start-date/@month')[0] + '--' \
            + output.xpath('.//end-date/@year')[0] + '/' + output.xpath('.//end-date/@month')[0]
        title = output.xpath('.//assessment-type/text()')[0]
        where = output.xpath('.//institution-name/text()')[0]
        desc = output.xpath('.//description-of-grant-scholarship/text()')[0]
        role = None
    if type == 'Curso / Disciplina lecionado':
        date = output.xpath('.//start-date/@year')[0] + '/' + output.xpath('.//start-date/@month')[0] + '--' \
            + output.xpath('.//end-date/@year')[0] + '/' + output.xpath('.//end-date/@month')[0]
        title = output.xpath('.//academic-session/text()')[0]
        where = output.xpath('.//institution-name/text()')[0]
        desc = None
        role = None
    if type == 'Outro júri / avaliação':
        date = output.xpath('.//start-date/@year')[0] + '/' + output.xpath('.//start-date/@month')[0]
        if output.xpath('.//end-date') != None:
            date += '--' + output.xpath('.//end-date/@year')[0] + '/' + output.xpath('.//end-date/@month')[0]
        title = output.xpath('.//description/text()')[0]
        where = output.xpath('.//institution-name/text()')[0]
        desc = None
        role = None
    if type == 'Tutoria':
        date = output.xpath('.//start-date/@year')[0] + '/' + output.xpath('.//start-date/@month')[0] + '--' \
            + output.xpath('.//end-date/@year')[0] + '/' + output.xpath('.//end-date/@month')[0]
        title = output.xpath('.//topic-of-mentor-ship/text()')[0]
        where = output.xpath('.//description/text()')[0]
        desc = output.xpath('.//name-of-protege/text()')[0]
        role = None
    print(r'\item '
        + date + ' '
        + type + ' '
        + title + ' '
        + ('(' + role + ') ' if role != None else '') +
        + '(' + where + r')\newline '
        + (desc if desc != None else '')
    )
print(r'\end{enumerate}')

print(r'\begin{enumerate}')
for output in root.find('distinctions'):
    type = output.xpath('.//distinction-type/text()')[0]
    if type in ('Prémio', 'Outra distinção'):
        date = output.xpath('.//effective-date/text()')[0]
        title = output.path('.//distinction-name/text()')[0]
        where = output.xpath('.//institution-name/text()')[0]
        desc = output.xpath('.//description/text()')[0]
    print(r'\item '
        + date + ' '
        + title
        + '(' + where + r')'
        + desc
    )

write_end_document()
