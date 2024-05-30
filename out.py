import json, re
import sys

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
        print('body {text-align:justify;}')
        print('h1 {background-image:url("imgs/lecture.jpg"); background-size:cover; background-position:25%; height:180px; color:white; text-align:center; text-shadow:-2px -2px 2px black, 2px -2px 2px black, -2px 2px 2px black, 2px 2px 2px black;}')
        print('h2 {margin-top:50px; border-bottom:solid;}')
        print('.container {max-width:800px; margin:0 auto;}')
        print('table {width:100%; text-align:left;}')
        print('thead th {background-color: #ccc;}')
        # description
        print('@media screen and (min-width:1000px) {div.description {display:flex; flex-direction: column;} div.item {display:flex;} div.left {width:4em; font-weight:bold;} div.right {flex: 1;}')
        print('@media screen and (max-width:999px) {div.item {display:inline;} div.left {display:inline;font-weight:bold;} div.right{display:inline;}}')
        print('.hl {background-color:yellow;}')
        print('</style>')
        print('<script src="mytable.js"></script>')
        print('</head>')
        print('<body>')
        print(f'<h1>{name}</h1>')
        print('<div class="container">')

    def end(self):
        print('</div>')
        print('</body>')
        print('</html>')

    def markdown(self, text):
        text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)  # links
        text = re.sub(r'!\[\]\((.*?)\)', r'<img href="\1">', text)  # image
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  # bold
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)  # italic
        text = text.replace('&', '&amp;').replace('--', '&ndash;')
        text = text.replace('\n', '<br>\n')  # force breaklines
        text = re.sub(r'\=\=(.*?)\=\=', r'<span class="hl">\1</span>', text)  # highlight
        return text

    def contacts(self, contacts):
        print('<p>')
        for icon, text, link in contacts:
            print(f'<img width="28px" src="imgs/{icon}.svg">&nbsp;<a href="{link}">{text}</a> ')
        print('</p>')

    def section(self, text, icon=None):
        icon = '' if icon is None else f'<img width="45px" src="imgs/{icon}.svg"> '
        print(f'<h2>{icon}{text}</h2>')

    def text(self, text):
        print('<p>' + self.markdown(text) + '</p>')

    def description(self, items):
        print('<div class="description">')
        for label, text in items:
            print(f'<div class="item"><div class="left">{self.markdown(label)}</div><div class="right">{self.markdown(text)}</div></div>')
        print('</div>')

    def itemize(self, items):
        print('<ul>')
        for text in items:
            print(f'<li>{self.markdown(text)}</li>')
        print('</ul>')

    def table(self, rows, columns, types, sizes):
        print('</div>')  # temporarily disable container
        print(f'<div id="table{self.tables}"></div>')
        print('<div class="container">')  # re-enable container
        print('<script>')
        rows = [[self.markdown(str(value)) for value in row] for row in rows]
        print(f'table = new Table("table{self.tables}", ' + json.dumps(rows) + ', ' + json.dumps(columns) + ', ' + json.dumps(types) + ');')
        print('</script>')
        self.tables += 1

class Latex:
    def begin(self, name):
        print(r'\documentclass{article}')
        print(r'\usepackage[a4paper, margin=3cm]{geometry}')
        print(r'\setlength\parindent{0pt}  % no indent')
        print(r'\usepackage{xcolor,soul}')
        print(r'\usepackage{graphicx}')
        print(r'\usepackage[colorlinks=true, linkcolor=blue, urlcolor=blue]{hyperref}')
        print(r'\usepackage{longtable}')
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
        print(r'\titleformat{\section}{\normalfont\Large\scshape}{}{0pt}{}[{\vspace{-0.5ex}\titlerule[0.8pt]}]')
        print(r'\renewcommand{\thesection}{}  % no section numbers')
        print(r'\renewcommand{\thesubsection}{}  % no section numbers')
        print(r'\usepackage{tocloft}\renewcommand{\cftsecleader}{\cftdotfill{\cftdotsep}}\renewcommand{\cftsubsecdotsep}{\cftnodots}\setlength{\cftbeforesecskip}{-.5ex}')
        print(r'\usepackage{enumitem}')
        print(r'\newlength{\widestlabel}  % used by description')
        print(r'\begin{document}')
        print(f'{{\\Large {name}}}', end='\n\n')

    def end(self):
        print(r'\end{document}')

    def markdown(self, text, newline=r'\\'):
        text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1 \\href{\2}{\\includegraphics[width=0.8em]{imgs/link.pdf}}', text)  # links
        text = re.sub(r'!\[\]\((.*?)\)', r'\\includegraphics{\1}', text)  # image
        text = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', text)  # bold
        text = re.sub(r'\*(.*?)\*', r'\\textit{\1}', text)  # italic
        text = re.sub(r'\=\=(.*?)\=\=', r'\\hl{\1}', text)  # highlight
        text = text.replace('&', r'\&').replace('~', r'$\sim$')  # escape symbols
        text = text.replace('\n', newline + '\n')  # force breaklines
        text = re.sub(r'"(.*?)"', r"``\1''", text)
        return text

    def contacts(self, contacts):
        print(r'\noindent{\small')
        for icon, text, link in contacts:
            print(f'\\raisebox{{-0.25\\height}}{{\\includegraphics[width=0.5cm]{{imgs/{icon}.pdf}}}} \\href{{{link}}}{{{text}}} ')
        print('}\n')
        print(r'\setcounter{tocdepth}{2}\tableofcontents')
        print()

    def section(self, text, icon=None):
        icon = '' if icon is None else f'\\includegraphics[width=1cm]{{imgs/{icon}.pdf}}'
        print(f'\\section[{text}]{{{icon}{text}}}\\nopagebreak')

    def subsection(self, text):
        print(f'\\subsection[{text}]{{{text}}}\\nopagebreak')

    def text(self, text):
        print()
        print(r'\bigskip')
        print(self.markdown(text), end='\n\n')

    def description(self, items):
        largest_label = max((label for label, _ in items), key=len)
        print(f'\\settowidth{{\\widestlabel}}{{\\textbf{{{largest_label}}}}}')
        print(r'\begin{description}[style=sameline, labelwidth=\dimexpr\widestlabel+\labelsep, leftmargin=!]')
        for label, text in items:
            print(f'\\item[{self.markdown(label)}] {self.markdown(text, r'\newline')}')
        print(r'\end{description}')

    def itemize(self, items):
        print(r'\begin{itemize}')
        for text in items:
            print(f'\\item {self.markdown(text)}')
        print(r'\end{itemize}')

    def table(self, rows, columns, types, sizes):
        sizes = '|'.join(f'p{{{size}}}' if size else 'l' for size in sizes)
        print(r'{\small\begin{longtable}{|' + sizes + '|}')
        print(r'\hline')
        print('&'.join((f'\\bf {h}' for h in columns)) + r'\\')
        print(r'\hline\endhead')
        for row in rows:
            print('&'.join(self.markdown(str(v), r'\newline') for v in row) + r'\\')
            print(r'\hline')
        print(r'\end{longtable}}')
