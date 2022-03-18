tex_blocks = {
    'begin_document': r'''\documentclass[11pt]{article}

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

    'begin_item': '',
    'end_item': '',
    'begin_item_hl': '\\colorbox{gray}{',
    'end_item_hl': '}',

    'title': '\\textbf{{{}}}',
    'subtitle': '\\\\{}',
    'description': '\\\\{{\small {}}}',
    'same_file': True,
}
