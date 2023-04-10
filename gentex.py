import argparse
parser = argparse.ArgumentParser()
parser.add_argument('yaml')
args = parser.parse_args()

def escape(s):
    return s.replace('&', r'\&')

import yaml
cv = yaml.load(open(args.yaml), Loader=yaml.Loader)

filename = f'{args.yaml[:-5]}.tex'
f = open(filename, 'w')

print(r'\documentclass[12pt]{article}', end='\n\n', file=f)

print(r'\usepackage[a4paper, margin={2.5cm}]{geometry}', file=f)
print(r'\setlength\parindent{0pt}', file=f)
print(file=f)

print(r'\usepackage{xcolor}', file=f)
print(r'\usepackage{graphicx}', file=f)
print(r'\usepackage[colorlinks=true, linkcolor=blue, urlcolor=blue, pdfauthor={Ricardo Cruz}, pdftitle={Curriculum Vitae}]{hyperref}', file=f)
print(r'\usepackage{soul}  % \hl', file=f)
print(r'\usepackage{enumitem}', file=f)
print(r'\setlist{nosep,leftmargin=0.4cm}', file=f)
print(file=f)

print(r'% footer', file=f)
print(r'\usepackage{fancyhdr, lastpage}', file=f)
print(r'\pagestyle{fancy}', file=f)
print(r'\renewcommand{\headrulewidth}{0pt}', file=f)
print(r'\fancyfoot[L]{\scriptsize Last update: \today}', file=f)
print(r'\fancyfoot[C]{}', file=f)
print(r'\fancyfoot[R]{\scriptsize Page \thepage\ of \pageref{LastPage}}', file=f)
print(file=f)

print(r'\begin{document}', end='\n\n', file=f)

print(r'\pdfbookmark{Summary}{Summary}{\Large Ricardo Cruz, PhD}', end='\n\n', file=f)
print(r'{\footnotesize \raisebox{-0.25\height}{\includegraphics{imgs/icon-geo}} Portugal \raisebox{-0.25\height}{\includegraphics{imgs/icon-phone}} +351 934741617 \raisebox{-0.25\height}{\includegraphics{imgs/icon-mail}} \href{mailto:ricardo.pdm.cruz@gmail.com}{ricardo.pdm.cruz@gmail.com} \raisebox{-0.25\height}{\includegraphics{imgs/icon-home}} \href{http://rpmcruz.github.io}{rpmcruz.github.io}}', end='\n\n', file=f)

print(r'\bigskip', file=f)
print(cv['summary'], end='\n\n', file=f)

print(r'\textsc{Skills:}', file=f)
for i, skill in enumerate(cv['skills']):
    if i > 0:
        print(end=r' $\cdot$ ', file=f)
    print(end=skill, file=f)
print(end='\n\n', file=f)

print(r'\bigskip', file=f)
print(r'\includegraphics[width=\linewidth]{imgs/lecture}', end='\n\n', file=f)

for section in ['Education', 'Employment', 'Publications', 'Projects', 'Supervisions', 'Awards']:
    print(r'\bigskip', file=f)
    print(f'\\pdfbookmark{{{section}}}{{{section}}}\\includegraphics[width=2em]{{imgs/{section.lower()}.pdf}} \\textsc{{\large {section}}} \\hrulefill', end='\n\n', file=f)
    for item in cv[section.lower()]:
        print(r'\medskip', file=f)
        print(r'\begin{minipage}[t]{3cm}', file=f)
        if 'year' in item:
            print(escape(str(item['year'])), file=f)
        else:
            print(r'\,', file=f)
        if 'duration' in item:
            print(f"\n\\textit{{{item['duration']}}}", file=f)
        print(r'\end{minipage}%', file=f)
        print(r'\begin{minipage}[t]{13cm}', file=f)
        if 'highlight' in item:
            print(f"\\hl{{\\textbf{{{escape(item['title'])}}}}}", file=f)
        else:
            print(f"\\textbf{{{escape(item['title'])}}}", file=f)
        if 'link' in item:
            print(f"\\href{{{item['link']}}}{{\\includegraphics[width=0.8em]{{imgs/link.pdf}}}}", file=f)
        print(file=f)
        print(escape(item['subtitle']), file=f)
        if 'summary' in item:
            print(r'\begin{itemize}\color{black!80}\footnotesize', file=f)
            for subitem in item['summary']:
                print(f'\\item {escape(subitem)}', file=f)
            print(r'\end{itemize}', file=f)
        print(r'\end{minipage}%', file=f)
        print(end='\n\n', file=f)
    if section == 'Projects':
        print(r'\bigskip See my github for more projects: \href{https://github.com/rpmcruz?tab=repositories}{github.com/rpmcruz}', end='\n\n', file=f)
    if section == 'Publications':
        print(r'\bigskip My favorite publications are in \hl{\textbf{highlight}}. See my Google Scholar for more information: \href{https://scholar.google.com/citations?user=pSFY_gQAAAAJ}{scholar.google.com/citations?user=pSFY\_gQAAAAJ}', end='\n\n', file=f)

print(r'\end{document}', file=f)
f.close()

import os
if os.system(f'pdflatex -halt-on-error {filename} > /dev/null 2>&1') != 0:
    print(f'Error: pdflatex failed to compile {filename}')
    os._exit(1)
os.system(f'pdflatex -halt-on-error {filename} > /dev/null 2>&1')
for ext in ['aux', 'log', 'out', 'tex']:
    os.remove(filename[:-3] + ext)
