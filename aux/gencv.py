import argparse
parser = argparse.ArgumentParser()
parser.add_argument('yaml')
parser.add_argument('format', choices=['html', 'tex'])
args = parser.parse_args()

import shutil
import yaml
cv = yaml.load(open(args.yaml), Loader=yaml.Loader)

html_blocks = {
    'header': '---\nlayout: default\nactive: {}\n---',
    'year': '<p class="year">{}</p>',
    'item_begin_link_hl': '<a class="item highlight" href="{}">',
    'item_end_link_hl': '</a>',
    'item_begin_link': '<a class="item" href="{}">',
    'item_end_link': '</a>',
    'item_begin': '<div class="item">',
    'item_begin_hl': '<div class="item highlight">',
    'item_end': '</div>',
    'item_end_hl': '</div>',
    'image': '<img src="imgs/{}">',
    'title': '<p><b>{}</b></p>',
    'subtitle': '<p>{}</p>',
    'description': '<p><small>{}</small></p>',
    'same_file': False,
}

tex_blocks = {
    'header': r'''\documentclass[11pt]{article}

\usepackage[a4paper, lmargin=1cm, rmargin=1cm, tmargin=2cm, bmargin=3cm]{geometry}
\usepackage[utf8]{inputenc}
\usepackage[english]{babel}
\usepackage{graphicx}
\usepackage{amssymb}
\usepackage[hidelinks]{hyperref}
\usepackage{xcolor}
\definecolor{dark-blue}{rgb}{0.15,0.15,0.4}
\hypersetup{colorlinks, linkcolor={dark-blue}, citecolor={dark-blue}, urlcolor={dark-blue}}
\usepackage{changepage}  % \begin{adjustwidth}
\usepackage{multicol}  % \begin{multicols}{2}

\setlength{\parindent}{0cm}
\setlength{\parskip}{1em}

\usepackage{lastpage}
\usepackage{fancyhdr}
\pagestyle{fancy}
\renewcommand{\headrulewidth}{0pt}
\fancyfoot[L]{Last update: \today}
\fancyfoot[C]{}
\fancyfoot[R]{Page \thepage\ of \pageref{LastPage}}

\usepackage{tikz}
\usetikzlibrary{tikzmark, calc}

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
\textbf{\Huge Ricardo Cruz}\\[6.5ex]
\raisebox{-0.25\height}{\includegraphics{imgs/icon-geo}} Valongo, Portugal\\
\raisebox{-0.25\height}{\includegraphics{imgs/icon-phone}} +351 934741617\\
\raisebox{-0.25\height}{\includegraphics{imgs/icon-mail}} \href{mailto:ricardo.pdm.cruz@gmail.com}{\tt ricardo.pdm.cruz@gmail.com}\\
\raisebox{-0.25\height}{\includegraphics{imgs/icon-home}} \url{http://rpmcruz.github.io}
\end{minipage}}

\vspace{2ex}

For the last few years, I have been working at INESC TEC -- an institute that does both academic research and industry development. I have been doing both machine learning and computer vision, working in TensorFlow, PyTorch, and OpenCV.

I have just completed my Ph.D. in Computer Science (june 2021). During the Ph.D., I have been serving a few hours per week as a Teacher Assistant at the Faculty of Engineering, University of Porto, helping teach Python and C++. In 2021, I was awarded the Pedagogy Award based on student feedback.

\centerline{\rule{0.4\linewidth}{0.2pt}}

\begin{minipage}[t]{0.08\linewidth}
\textsc{Skills:}
\end{minipage}
\begin{minipage}[t]{0.92\linewidth}
\small
Python $\cdot$ C $\cdot$ C++ $\cdot$ Java $\cdot$ R $\cdot$ MATLAB $\cdot$ TensorFlow $\cdot$ PyTorch $\cdot$ OpenCV $\cdot$ SQL $\cdot$ Git
\end{minipage}
''',
    'year': '\\bigskip\n\\centerline{{\\sc\\large {}}}',
    'item_begin': '',
    'item_begin_hl': '\\colorbox{gray}{',
    'item_end': '',
    'item_end_hl': '}',
    'title': '\\textbf{{{}}}',
    'subtitle': '\\\\{}',
    'description': '\\\\{{\small {}}}',
    'same_file': True,
}

blocks = html_blocks if args.format == 'html' else tex_blocks

if blocks['same_file']:
    f = open(f'cv.{args.format}', 'w')
for section_name in ['Publications', 'Projects', 'Teaching', 'Supervisions', 'Workshops', 'Awards']:
    if not blocks['same_file']:
        f = open(f'{section_name.lower()}.{args.format}', 'w')
    print(blocks['header'].format(section_name), file=f)
    section = cv[section_name.lower()]
    last_year = None
    if args.format == 'html':
        if section_name == 'Publications':
            print('<p>Some of my favorite publications are <span style="border:1px dashed black;">highlighted</span>.</p>', file=f)
    for item in section:
        if item['year'] != last_year:
            print(blocks['year'].format(item['year']), file=f)
            last_year = item['year']
        hlsuffix = '_hl' if item.get('highlight') else ''
        if 'link' in item:
            print(blocks['item_begin_link' + hlsuffix].format(item['link']), file=f)
        else:
            print(blocks['item_begin' + hlsuffix], file=f)
        if 'image' in item:
            print(blocks['image'].format(item['image']), file=f)
        for field in ['title', 'subtitle', 'description']:
            if field in item:
                print(blocks[field].format(item[field]), file=f)
        if 'link' in item:
            print(blocks['item_end_link' + hlsuffix], file=f)
        else:
            print(blocks['item_end' + hlsuffix], file=f)
    if args.format == 'html':
        if section_name == 'Projects':
            print('<p style="margin-top:20px">Find more of my code at <a href="https://github.com/rpmcruz?tab=repositories">github.com/rpmcruz</a></p>', file=f)
    if args.format == 'html':
        shutil.copyfile('publications.html', 'index.html')
