import argparse
parser = argparse.ArgumentParser()
parser.add_argument('yaml')
parser.add_argument('template', choices=['latex', 'html'])
args = parser.parse_args()

def escape(s):
    return s.replace('&', r'\&').replace('~', r'$\sim$')

import yaml, re, os

class LatexTemplate:
    def begin_document(self, f):
        print(r'\documentclass[12pt]{article}', end='\n\n', file=f)
        print(r'\usepackage[a4paper, margin={2.5cm}]{geometry}', file=f)
        print(r'\setlength\parindent{0pt}', file=f)
        print(file=f)
        print(r'\usepackage{xcolor}', file=f)
        print(r'\usepackage{graphicx}', file=f)
        print(r'\usepackage[colorlinks=true, linkcolor=blue, urlcolor=blue, pdfauthor={Ricardo Cruz}, pdftitle={Ricardo Cruz CV}]{hyperref}', file=f)
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

    def insert_toc(self, f, sections):
        pass

    def end_document(self, f):
        print(r'\end{document}', file=f)

    def insert_title(self, f, name):
        print(f'\pdfbookmark{{Title}}{{Title}}{{\Large {name}}}', end='\n\n', file=f)

    def insert_information(self, f, icon, text, link):
        print(f'{{\\footnotesize \\raisebox{{-0.25\height}}{{\includegraphics[width=16px]{{imgs/profile-{icon}}}', end='', file=f)
        if link is None:
            print(text, end='', file=f)
        else:
            print(f'\href{{{link}}}{{{text}}}', end='', file=f)
        print('}', end='\n', file=f)

    def insert_biography(self, f, text):
        print(text, end='\n\n', file=f)

    def insert_skills(self, f, skills):
        print(r'\textsc{Skills:}', file=f)
        for i, skill in enumerate(skills):
            if i > 0:
                print(end=r' $\cdot$ ', file=f)
            print(end=skill, file=f)
        print(end='\n\n', file=f)

    def insert_picture(self, f, fname):
        print(f'\includegraphics[width=\linewidth]{{imgs/{fname}}}', end='\n\n', file=f)

    def insert_space(self, f):
        print('\n\\bigskip', file=f)

    def begin_section(self, f, icon, name):
        print(f'\\pdfbookmark{{{name}}}{{{name}}}\\includegraphics[width=2em]{{imgs/section-{icon}.pdf}} \\textsc{{\large {name}}} \\hrulefill', end='\n\n', file=f)

    def end_section(self, f, name):
        pass

    def begin_environment(self, f, type):
        print(f'\\begin{{{type}}}', file=f)

    def end_environment(self, f, type):
        print(f'\\end{{{type}}}', file=f)

    def begin_item(self, f, type, label):
        end = f'[{label}] ' if label else ' '
        print(r'\item', end=end, file=f)

    def end_item(self, f, type):
        pass

    def insert_text(self, f, text):
        text = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', text)  # bold
        text = re.sub(r'\*(.*?)\*', r'\\textit{\1}', text)  # italic
        text = text.replace('&', r'\&').replace('~', r'$\sim$')
        print(text, file=f)

    def filename(self, name):
        return f'{name}.tex'

    def compile(self, filename):
        if os.system(f'pdflatex -halt-on-error {filename} > /dev/null 2>&1') != 0:
            print(f'Error: pdflatex failed to compile {filename}')
            os._exit(1)
        os.system(f'pdflatex -halt-on-error {filename} > /dev/null 2>&1')
        for ext in ['aux', 'log', 'out']:#, 'tex']:
            os.remove(filename[:-3] + ext)

class HtmlTemplate:
    def begin_document(self, f):
        print(r'<html>', file=f)
        print(r'<head>', file=f)
        print(r'<meta charset="utf-8" />', file=f)
        print(r'<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">', file=f)
        print(r'<title>Ricardo Cruz CV</title>', file=f)
        print(file=f)

        print('<style>', file=f)
        print('body {font-family: serif; max-width: 850px; margin: auto; margin-top: 20px; margin-bottom: 20px}', file=f)
        print('p {margin: 0}', file=f)
        print('h1 {margin-bottom: 0}', file=f)
        print('h2 {border-bottom: 2px solid; font-variant: small-caps}', file=f)
        print('a {text-decoration: none}', file=f)
        print('a:hover {text-decoration: underline}', file=f)
        print('.sc {font-variant: small-caps}', file=f)
        print('.small {font-size: small; color: gray}', file=f)
        print('.hl {background-color: yellow}', file=f)
        print('.nobr {white-space: nowrap}', file=f)
        print('.bigskip {margin-top: 30px}', file=f)
        print('ul.menu {background-color: white; position: fixed; top: 0; right: 0; list-style: none; padding-left: 20px; padding-right: 30px; border: 1px solid black}', file=f)
        print('ul.menu a {display: block}', file=f)
        print('@media screen and (min-width: 768px) {body {margin: auto; text-align: justify} div.columns {display: flex; flex-direction: column} div.item {display: flex} div.left {width: 100px; font-weight: bold} div.right {flex: 1} .desktop {display: block}}', file=f)
        print('@media screen and (max-width: 767px) {body {margin-left: 6px; margin-right: 6px} .desktop {display: none} div.item {display: inline} div.left {display: inline; font-weight: bold} div.right {display: inline}}', file=f)
        print('</style>', file=f)
        print('</head>', file=f)
        print(file=f)

        print('<body id="top">', file=f)

    def insert_toc(self, f, sections):
        print('<ul class="menu desktop">', file=f)
        print(f'<li><a href="#top">Top</a></li>', file=f)
        for section in sections:
            print(f'<li><a href="#{section.lower()}">{section}</a></li>', file=f)
        print('</ul>', file=f)

    def end_document(self, f):
        from datetime import datetime
        print(f'<center class="bigskip small">Last update: {datetime.today().strftime("%Y-%m-%d")}</center>', file=f)
        print(r'</body>', file=f)
        print(r'</html>', file=f)

    def insert_title(self, f, name):
        print(f'<h1>{name}</h1>', file=f)

    def insert_information(self, f, icon, text, link):
        print(f'<img height="20px" src="imgs/profile-{icon}.svg">', end=' ', file=f)
        if link is None:
            print(text, end=' ', file=f)
        else:
            print(f'<a href="{link}">{text}</a>', end=' ', file=f)

    def insert_biography(self, f, text):
        print(f'<p>{text}</p>', file=f)

    def insert_skills(self, f, skills):
        print('<p><span class="sc">Skills:</span>', end=' ', file=f)
        for i, skill in enumerate(skills):
            if i > 0:
                print(end=r' &middot; ', file=f)
            print(end=skill, file=f)
        print('</p>', file=f)

    def insert_picture(self, f, fname):
        print(f'<img width="100%" src="imgs/{fname}">', file=f)

    def insert_space(self, f):
        print('<div class="bigskip"></div>', file=f)

    def begin_section(self, f, icon, name):
        print(f'<h2 id={name.lower()}><img width="40px" src="imgs/section-{icon}.svg"> {name}</h2>', file=f)

    def end_section(self, f, name):
        pass

    def begin_environment(self, f, type):
        if type == 'description':
            print('<div class="columns">', file=f)
        elif type == 'itemize':
            print('<ul>', file=f)
        elif type == 'enumerate':
            print('<ol>', file=f)

    def end_environment(self, f, type):
        if type == 'description':
            print('</div>', file=f)
        elif type == 'itemize':
            print('</ul>', file=f)
        elif type == 'enumerate':
            print('</ol>', file=f)

    def begin_item(self, f, type, label):
        if type == 'description':
            print(f'<div class="item"><div class="left">{str(label).replace("--", "&mdash;")}</div><div class="right">', file=f)
        else:
            print('<li>', file=f)

    def end_item(self, f, type):
        if type == 'description':
            print(f'</div></div>', file=f)
        else:
            print('</li>', file=f)

    def insert_text(self, f, text):
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  # bold
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)  # italic
        text = text.replace('&', '&amp;').replace('--', '&ndash;')
        print(text, file=f)

    def filename(self, name):
        return 'index.html'

    def compile(self, filename):
        pass

cv = yaml.load(open(args.yaml), Loader=yaml.Loader)
template = globals()[f'{args.template.title()}Template']()
filename = template.filename(args.yaml[:-5])
f = open(filename, 'w')

template.begin_document(f)
template.insert_toc(f, [section['title'] for section in cv.values()])
for i, (name, section) in enumerate(cv.items()):
    if i > 0:
        template.insert_space(f)
    if name == 'profile':
        template.insert_title(f, section['name'])
        for key in ['location', 'email', 'phone', 'website', 'orcid']:
            value = section[key]
            if key == 'phone': link = 'tel:' + value.replace(' ', '')
            elif key == 'email': link = 'mailto:' + value
            elif key == 'website': link = value
            elif key == 'orcid': link = 'https://orcid.org/' + value
            else: link = None
            template.insert_information(f, key, value, link)
        template.insert_space(f)
        template.insert_biography(f, section['biography'])
        template.insert_skills(f, section['skills'])
        template.insert_space(f)
        template.insert_picture(f, section['picture'])
    else:
        template.begin_section(f, section['icon'], section['title'])
        env = section['environment']
        template.begin_environment(f, env)
        for item in section['listing']:
            template.begin_item(f, env, item.get('label'))
            template.insert_text(f, item['text'])
            template.end_item(f, env)
        template.end_environment(f, env)
        template.end_section(f, section['title'])
template.end_document(f)
f.close()
template.compile(filename)
