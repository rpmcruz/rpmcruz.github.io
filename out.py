import re
import json

class Latex:
    def begin_document(self, info):
        print(r'\documentclass{moderncv}')
        print(r'\moderncvstyle{classic}')
        print(r'\moderncvcolor{blue}')
        print(r'\usepackage[margin=2cm]{geometry}')
        print(r'\usepackage{soul}')
        print(r'\name{' + info['firstname'] + '}{' + info['lastname'] + '}')
        print(r'\title{' + info['title'] + '}')
        print(r'\email{' + info['email'] + '}')
        print(r'\homepage{' + info['homepage'] + '}')
        print(r'\social[github]{' + info['github'] + '}')
        print(r'\social[orcid]{' + info['orcid'] + '}')
        print(r'\photo{photo}')
        print()
        print(r'\begin{document}')
        print(r'\makecvtitle')

    def end_document(self):
        print(r'\end{document}')

    def biography(self, text):
        print(self.markdown(text))

    def section(self, name):
        print(r'\section{' + name + '}')

    def subsection(self, name):
        print(r'\subsection{' + name + '}')

    def cvitem(self, left, text):
        print(r'\cvitem{' + self.markdown(left) + '}{' + self.markdown(text) + '}')

    def cventry(self, dates, title, employer, city, grade, description):
        print(r'\cventry{' + dates + '}{' + title + '}{' + employer + '}{}{}{' + self.markdown(description) + '}')

    def paragraph(self, text):
        self.cvitem('', text)

    def table_small(self, label, rows, columns):
        print(r'\cvitem{' + label + '}{%')
        print(r'\begin{tabular}{' + '|c'*len(columns) + '|}')
        print(r'\hline')
        print(' & '.join(self.markdown(c) for c in columns) + r'\\\hline')
        for row in rows:
            print(' & '.join(row) + r'\\')
        print(r'\hline')
        print(r'\end{tabular}}')

    def markdown(self, text, newline=r'\\'):
        text = re.sub(r'!\[\]\(([^\s]*?)\)', r'\\includegraphics[width=300px]{\1}', text)  # image
        text = re.sub(r'\[([^\]]*?)\]\(([^\s]*?)\)', r'\1 \\href{\2}{\\includegraphics[width=0.8em]{imgs/link.pdf}}', text)  # links
        text = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', text)  # bold
        text = re.sub(r'\*(.*?)\*', r'\\textit{\1}', text)  # italic
        text = re.sub(r'__(.*?)__', r'\\underline{\1}', text)  # underline
        text = re.sub(r'\=\=(.*?)\=\=', r'\\hl{\1}', text)  # highlight
        text = text.replace('&', r'\&').replace('~', r'$\sim$')  # escape symbols
        text = text.replace('#', r'\#')
        text = text.replace('\n', newline + '\n')  # force breaklines
        text = re.sub(r'"(.*?)"', r"``\1''", text)
        return text

class FEUP(Latex):
    def begin_document(self, info):
        print(r'\documentclass{article}')
        print(r'\usepackage[a4paper, margin=2cm]{geometry}')
        print(r'\setlength\parindent{0pt}  % no indent')
        print(r'\setlength{\parskip}{4pt}  % space between paragraphs')
        print(r'\usepackage{xcolor,soul}')
        print(r'\usepackage{graphicx}')
        print(r'\usepackage[colorlinks=true, linkcolor=blue, urlcolor=blue]{hyperref}')
        print(r'\usepackage{fancyhdr}')
        print(r'\usepackage{lastpage}  % defines \pageref{LastPage}')
        print(r'\pagestyle{fancy}')
        print(r'\renewcommand{\headrulewidth}{0pt}  % remove head line')
        print(r'\makeatletter\let\ps@plain\ps@fancy\makeatother  % first page equal to rest')
        print(r'\fancyhead{}')
        print(r'\fancyfoot[L]{\scriptsize Last update: \today}')
        print(r'\fancyfoot[C]{}')
        print(r'\fancyfoot[R]{\scriptsize Page \thepage\ of \pageref{LastPage}}')
        print(r'\usepackage{titlesec}  % change \section look')
        print(r'\titleformat{\section}{\normalfont\Large\scshape}{}{0pt}{}[{\titlerule[0.8pt]}]')
        print(r'\titleformat{\subsection}{\normalfont\large\scshape}{}{0pt}{}[\vspace{-1ex}\hbox to 15.2cm{\leaders\hbox to 5pt{\hss . \hss}\hfil}]')
        print(r'\titleformat{\subsubsection}{\normalfont\scshape}{}{0pt}{}')
        print(r'\renewcommand{\thesection}{}  % no section numbers')
        print(r'\renewcommand{\thesubsection}{}  % no section numbers')
        print(r'\usepackage{tocloft}\renewcommand{\cftsecleader}{\cftdotfill{\cftdotsep}}\renewcommand{\cftsubsecdotsep}{\cftnodots}\setlength{\cftbeforesecskip}{-.5ex}')
        print(r'\usepackage{enumitem}')
        print(r'\setlist{itemsep=0pt, parsep=0pt}')
        print(r'\newlength{\widestlabel}  % used by description')
        print(r'\usepackage{tikz}\usetikzlibrary{shapes}')
        print(r'\newcommand{\starnum}[2]{\tikz[baseline=(star.base)]{\node[star, star points=5, star point ratio=2.25, fill=#2, draw, minimum size=1.5em, inner sep=0pt] (star) {\textbf{#1}};}}')
        print(r'\begin{document}')
        print(f'{{\\Large {info["firstname"]} {info["lastname"]}}}', end='\n\n')
        print(r'\noindent{\small')
        for key, value in info['contact'].items():
            print(f'\\raisebox{{-0.25\\height}}{{\\includegraphics[width=0.5cm]{{imgs/{key}.pdf}}}} \\href{{{value}}}{{{value}}} ')
        print('}\n')
        print(r'\par\noindent\rule{\textwidth}{0.4pt}')
        print(r'\setcounter{tocdepth}{2}\tableofcontents')
        print(r'\par\noindent\rule{\textwidth}{0.4pt}')
        print()

    def part(self, name):
        print(r'\section{' + name + '}')

    def section(self, name):
        print(r'\subsection{' + name + '}')

    def subsection(self, name):
        print(r'\subsubsection{' + name + '}')

    def cvitem(self, left, text):
        print(r'\begin{minipage}[t]{0.12\linewidth}')
        print(self.markdown(left))
        print(r'\end{minipage}%')
        print(r'\begin{minipage}[t]{0.88\linewidth}')
        print(self.markdown(text))
        print(r'\end{minipage}')
        print()

    def cventry(self, dates, title, employer, city, grade, description):
        print(r'\begin{minipage}[t]{0.12\linewidth}')
        print(self.markdown(dates))
        print(r'\end{minipage}%')
        print(r'\begin{minipage}[t]{0.88\linewidth}')
        print(r'\textbf{' + self.markdown(title) + r'}, \textit{' + employer + r'}\\')
        print(self.markdown(description))
        print(r'\end{minipage}')
        print()

    def paragraph(self, text):
        print(self.markdown(text))
        print()

    def itemize(self, items):
        print(r'\begin{itemize}')
        for item in items:
            print(r'\item ' + self.markdown(item))
        print(r'\end{itemize}')

    def table_small(self, label, rows, columns):
        print(r'\begin{minipage}[t]{0.12\linewidth}')
        print(self.markdown(label))
        print(r'\end{minipage}%')
        print(r'\begin{minipage}[t]{0.88\linewidth}')
        print(r'\begin{tabular}{' + '|c'*len(columns) + '|}')
        print(r'\hline')
        print(' & '.join(self.markdown(c) for c in columns) + r'\\\hline')
        for row in rows:
            print(' & '.join(row) + r'\\')
        print(r'\hline')
        print(r'\end{tabular}')
        print(r'\end{minipage}%')
        print()

class HTML:
    tables = 0

    def begin_document(self, info):
        print('<!DOCTYPE html>')
        print('<html lang="en">')
        print('<head>')
        print('<meta charset="UTF-8">')
        print('<meta name="viewport" content="width=device-width, initial-scale=1" />')
        print('<title>' + info['firstname'] + ' ' + info['lastname'] + '</title>')
        print('<style>')
        print('body {text-align:justify;}')
        #print('h1 {background-image:url("imgs/lecture.jpg"); background-size:cover; background-position:25%; height:180px; color:white; text-align:center; text-shadow:-2px -2px 2px black, 2px -2px 2px black, -2px 2px 2px black, 2px 2px 2px black;}')
        print('h2 {margin-top:50px; border-bottom:solid;}')
        print('.container {max-width:800px; margin:0 auto;}')
        print('table.large {width:100%; text-align:left;}')
        print('thead th {background-color: #ccc;}')
        # description
        print('@media screen and (min-width:1000px) {div.description {display:flex; flex-direction: column;} div.item {display:flex;} div.left {width:8em; font-weight:bold;} div.right {flex: 1;}')
        print('@media screen and (max-width:999px) {div.item {display:inline;} div.left {display:inline;font-weight:bold;} div.right{display:inline;}}')
        print('.hl {background-color:yellow;}')
        print('</style>')
        print('<script src="mytable.js"></script>')
        print('</head>')
        print('<body>')
        print('<div class="container">')
        print('<h1><img width="120px" src="photo.jpg"> ' + info['firstname'] + ' ' + info['lastname'] + '</h1>')
        print('<p>')
        for contact in ['email', 'github', 'orcid']:
            print('<img width="22px" src="imgs/' + contact + '.svg">&nbsp;<a href="' + info[contact] + '">' + info[contact] + '</a> ')
        print('<img width="22px" src="imgs/pdf.svg">&nbsp;<a href="rpcruz-cv.pdf">PDF</a>')
        print('</p>')

    def end_document(self):
        print('</div>')
        print('</body>')
        print('</html>')

    def biography(self, text):
        print('<p>' + self.markdown(text) + '</p>')

    def section(self, name):
        print(f'<h2>' + name + '</h2>')

    def subsection(self, name):
        print(f'<h3>' + name + '</h3>')

    def cvitem(self, left, text):
        print('<div class="description">')
        print(f'<div class="item"><div class="left">{self.markdown(left)}</div><div class="right">{self.markdown(text)}</div></div>')
        print('</div>')

    def cventry(self, dates, title, employer, city, grade, description):
        text = f'**{title}** *{employer}*\n{description}'
        self.cvitem(dates, text)

    def paragraph(self, text):
        print('<p>' + text + '</p>')

    def table_small(self, label, rows, columns):
        print(label + ':')
        print('<table border="1">')
        print('<tr>')
        print(''.join('<th>' + self.markdown(c) + '</th>' for c in columns))
        print('</tr>')
        for row in rows:
            print('<tr>')
            print(''.join('<td>' + r + '</td>' for r in row))
            print('</tr>')
        print('</table>')

    def table_large(self, rows, columns, types):
        print('</div>')  # temporarily disable container
        print(f'<div id="table{self.tables}"></div>')
        print('<div class="container">')  # re-enable container
        print('<script>')
        rows = [[self.markdown(str(value)) for value in row] for row in rows]
        print(f'table = new Table("table{self.tables}", ' + json.dumps(rows) + ', ' + json.dumps(columns) + ', ' + json.dumps(types) + ');')
        print('</script>')
        self.tables += 1

    def markdown(self, text):
        text = re.sub(r'\[([^\]*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)  # links
        text = re.sub(r'!\[\]\((.*?)\)', r'<img href="\1">', text)  # image
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  # bold
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)  # italic
        text = re.sub(r'__(.*?)__', r'<u>\1</u>', text)  # underline
        text = text.replace('&', '&amp;').replace('--', '&ndash;')
        text = text.replace('\n', '<br>\n')  # force breaklines
        text = re.sub(r'\=\=(.*?)\=\=', r'<span class="hl">\1</span>', text)  # highlight
        return text