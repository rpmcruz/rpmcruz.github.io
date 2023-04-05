import argparse
parser = argparse.ArgumentParser()
parser.add_argument('yaml')
args = parser.parse_args()

import yaml
cv = yaml.load(open(args.yaml), Loader=yaml.Loader)

def escape(x):
    return x.replace('&', r'\&').replace('~', r'$\sim$')

f = open(f'{args.yaml[:-4]}tex', 'w')

print(r'''\documentclass[11pt]{article}

\usepackage[a4paper, lmargin=1cm, rmargin=1cm, tmargin=2cm, bmargin=3cm]{geometry}
\usepackage[utf8]{inputenc}
\usepackage[english]{babel}
\usepackage{graphicx}
\usepackage{amssymb}
\usepackage[hidelinks]{hyperref}
\usepackage{xcolor}
\definecolor{dark-blue}{rgb}{0.15,0.15,0.4}
\hypersetup{colorlinks, linkcolor={dark-blue}, citecolor={dark-blue}, urlcolor={dark-blue}}
\usepackage{multicol}  % \begin{multicols}{2}
\usepackage{enumitem}
\usepackage{lastpage}  % used by the footer
\usepackage{soul}      % \hl

\setlength{\parindent}{0cm}
\setlength{\parskip}{1em}

\usepackage{fancyhdr}
\pagestyle{fancy}
\renewcommand{\headrulewidth}{0pt}
\fancyfoot[L]{\scriptsize Last update: \today}
\fancyfoot[C]{}
\fancyfoot[R]{\scriptsize Page \thepage\ of \pageref{LastPage}}

\usepackage{tikz}
\usetikzlibrary{tikzmark}

\begin{document}
\begin{tikzpicture}[remember picture,overlay]
\fill[blue!10] (current page.north west) rectangle ([yshift=-37ex]current page.north east);
\end{tikzpicture}

\vspace{-12ex}
\makebox[\textwidth]{%
\begin{minipage}[t]{0.3\textwidth}
\centering
\includegraphics[width=10em]{imgs/photo}

\bigskip
\begin{minipage}{13em}
$\bullet$ Machine learning specialist\\
$\bullet$ Computer vision specialist\\
$\bullet$ Programmer
\end{minipage}
\end{minipage}\hfill%
\begin{minipage}[t]{0.6\textwidth}
\vspace{-12ex}
\textbf{\Huge Ricardo Cruz, PhD}\\[6.5ex]
\raisebox{-0.25\height}{\includegraphics{imgs/icon-geo}} Valongo, Portugal\\
\raisebox{-0.25\height}{\includegraphics{imgs/icon-phone}} +351 934741617\\
\raisebox{-0.25\height}{\includegraphics{imgs/icon-mail}} \href{mailto:ricardo.pdm.cruz@gmail.com}{\tt ricardo.pdm.cruz@gmail.com}\\
\raisebox{-0.25\height}{\includegraphics{imgs/icon-home}} \url{http://rpmcruz.github.io}
\end{minipage}}

\vspace{2ex}''', file=f)
print(escape(cv['summary']), file=f)
print(file=f)
print(r'''\centerline{\rule{0.4\linewidth}{0.2pt}}

\begin{minipage}[t]{0.08\linewidth}
\textsc{Skills:}
\end{minipage}
\begin{minipage}[t]{0.92\linewidth}
\small''', file=f)
print(' $\cdot$ '.join(cv['skills']), file=f)
print('\\end{minipage}\n', file=f)

sections = ['Career', 'Teaching', 'Education', 'Projects', 'Publications', 'msc-supervisions', 'bsc-supervisions', 'Awards']
multicols = {'Projects', 'Awards'}

for section_name in sections:
    if section_name == 'Career':
        print(r'\begin{minipage}[t]{0.53\textwidth}', file=f)
    elif section_name == 'Education':
        print(r'\begin{minipage}[t]{0.43\textwidth}', file=f)

    elif section_name != 'bsc-supervisions':
        print('\n\\bigskip', file=f)

    if section_name == 'Projects':
        print('\\centerline{{\\sc\\Large Selected Open-Source Portfolio}}', file=f)
    elif section_name == 'msc-supervisions':
        print(f'\\centerline{{\\sc\\Large Supervisions}}', file=f)
        print(r"Master's Theses\\[-6ex]", file=f)
    elif section_name == 'bsc-supervisions':
        print(r"Bachelor's Projects\\[-6ex]", file=f)
    else:
        print(f'\\centerline{{\\sc\\Large {section_name}}}', file=f)

    if section_name in multicols:
        print(r'\begin{multicols}{2}\setlength{\columnseprule}{0.4pt}\interlinepenalty=10000', file=f)

    if section_name == 'Publications':
        print(r'These are my indexed publications with some publications in \hl{\textbf{highlight}} for emphasis. You may find the papers in my Google Scholar: \url{https://scholar.google.pt/citations?user=pSFY_gQAAAAJ}', file=f)

    print(r'\begin{itemize}[leftmargin=1em, itemsep=0em]', file=f)
    for year in cv[section_name.lower()]:
        for item in year['items']:
            print(r'\item ', file=f)
            if 'year' in year:
                print(f'{year["year"]} $\\vert$ ', file=f)
            if 'title' in item:
                if item.get('highlight'):
                    print('\hl{', file=f)
                if section_name == 'Publications':
                    print(f'\\textbf{{{escape(item["title"])}.}}', file=f)
                else:
                    print(f'\\textbf{{{escape(item["title"])}}}', file=f)
                if item.get('highlight'):
                    print('}', file=f)
            if 'subtitle' in item:
                if section_name not in {'Publications', 'msc-supervisions', 'bsc-supervisions'}:
                    print(r'\\', file=f)
                if 'image' in item and section_name not in {'msc-supervisions', 'bsc-supervisions'}:
                    imgs = item['image'] if type(item['image']) is list else [item['image']]
                    print(r'\begin{minipage}{0.20\linewidth}', file=f)
                    print(' '.join(f'\\includegraphics[width=\linewidth]{{../imgs/{img}}}' for img in imgs), file=f)
                    print(r'\end{minipage}', file=f)
                    print(r'\begin{minipage}{0.80\linewidth}', file=f)
                if section_name == 'Publications':
                    print(f'{escape(item["subtitle"])}.', file=f)
                else:
                    print(escape(item["subtitle"]), file=f)
                if 'image' in item and section_name not in {'msc-supervisions', 'bsc-supervisions'}:
                    print(r'\end{minipage}', file=f)
            if 'description' in item:
                print(f'\\\\{{\\small {escape(item["description"])}}}', file=f)
    print(r'\end{itemize}', file=f)
    if section_name == 'Projects':
        print(r'''\begin{itemize}[leftmargin=1em, itemsep=0em, label=$\blacktriangleright$]\small
\item Find more of my open-source code at\\\href{https://github.com/rpmcruz?tab=repositories}{\tt https://github.com/rpmcruz}.
\end{itemize}''', file=f)
    if section_name in multicols:
        print(r'\end{multicols}', file=f)
    if section_name in ['Teaching', 'Education']:
        print(r'\end{minipage}%', file=f)
        if section_name == 'Teaching':
            print(r'\hfill\raisebox{-0.60\textheight}{\rule{0.5pt}{0.59\textheight}}\hfill%', file=f)
        else:
            print('\\newpage\n', file=f)
print(r'\end{document}', file=f)
f.close()
