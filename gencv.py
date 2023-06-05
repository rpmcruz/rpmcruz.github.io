import argparse
parser = argparse.ArgumentParser()
parser.add_argument('markdown')
parser.add_argument('template', choices=['tex', 'html'])
args = parser.parse_args()

import re

# convert the markdown to a more friendly representation
ast = {}
f = open(args.markdown)

# header
assert f.readline() == '---\n'
ast['header'] = {}
while (line := f.readline()) != '---\n':
    key, value = line.split(': ')
    ast['header'][key] = value.rstrip()

# body
ast['body'] = {'type': 'document', 'parent': None, 'children': []}
node = ast['body']
for line in f:
    line = line.rstrip()
    if line == '': continue
    # environment
    environments = {r'\*': 'itemize', '-': 'itemize', r'\+': 'description',
        r'1\.': 'enumerate'}
    found_environment = False
    for sym, env in environments.items():
        matches = re.match(r'^\s*' + sym + r'\s', line)
        if matches:
            indent = len(matches.group(0))
            text = line[indent:]
            if 'indent' not in node or indent > node['indent']:
                child = {'type': env, 'parent': node, 'children': [], 'indent': indent}
                node['children'].append(child)
                node = child
            while indent < node['indent']:
                node = node['parent']
            if env == 'description':
                label, text = text.split(': ', 1)
            item = {'type': 'item', 'text': text, 'parent': node}
            if env == 'description':
                item['label'] = label
            node['children'].append(item)
            found_environment = True
    if found_environment: continue
    # if indented, then it continues from the previous text
    if line[0].isspace():
        node['children'][-1]['text'] += '\n' + line.lstrip()
        continue
    # close any environment if exists
    while 'indent' in node:
        node = node['parent']
    # heading
    matches = re.match(r'^(#+)\s', line)
    if matches:
        node['children'].append({
            'type': 'heading',
            'depth': len(matches.group(1)),
            'text': line[len(matches.group(0)):],
        })
        continue
    # paragraph
    node['children'].append({
        'type': 'paragraph',
        'text': line,
    })
f.close()

# render ast to latex or html

class HTML:
    def begin_document(self, f, header):
        print(r'<html>', file=f)
        print(r'<head>', file=f)
        print(r'<meta charset="utf-8" />', file=f)
        print(r'<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">', file=f)
        print(f"<title>{header['title']}</title>", file=f)
        print(file=f)
        print('<style>', file=f)
        print('body {font-family: serif; max-width: 850px; margin: auto; margin-top: 20px; margin-bottom: 20px}', file=f)
        print('h1 {margin-bottom: 0}', file=f)
        print('h2 {border-bottom: 2px solid; font-variant: small-caps}', file=f)
        print('a {text-decoration: none}', file=f)
        print('a:hover {text-decoration: underline}', file=f)
        print('.sc {font-variant: small-caps}', file=f)
        print('.small {font-size: x-small}', file=f)
        print('.hl {background-color: yellow}', file=f)
        print('.nobr {white-space: nowrap}', file=f)
        print('.bigskip {margin-top: 30px}', file=f)
        print('ul.menu {background-color: white; position: fixed; top: 0; right: 0; list-style: none; padding-left: 20px; padding-right: 30px; border: 1px solid black; font-size: x-small}', file=f)
        print('ul.menu a {display: block}', file=f)
        print('@media screen and (min-width: 1000px) {body {margin: auto; text-align: justify} div.columns {display: flex; flex-direction: column} div.item {display: flex} div.left {width: 150px; font-weight: bold} div.right {flex: 1} .desktop {display: block}}', file=f)
        print('@media screen and (max-width: 999px) {body {margin-left: 6px; margin-right: 6px} .desktop {display: none} div.item {display: inline} div.left {display: inline; font-weight: bold} div.right {display: inline}}', file=f)
        print('</style>', file=f)
        print('</head>', file=f)
        print(file=f)
        print('<body id="top">', file=f)

    def end_document(self, f):
        from datetime import datetime
        print(f'<center class="bigskip small">Last update: {datetime.today().strftime("%Y-%m-%d")}</center>', file=f)
        print(r'</body>', file=f)
        print(r'</html>', file=f)

    def insert_toc(self, f, body):
        sections = [('-'.join(w.lower() for w in s['text'].split() if '!' not in w), self.process_text(s['text'])) for s in body if s['type'] == 'heading']
        print('<ul class="menu desktop">', file=f)
        print(f'<li><a href="#top">Top</a></li>', file=f)
        for anchor, title in sections:
            print(f'<li><a href="#{anchor}">{title}</a></li>', file=f)
        print('</ul>', file=f)

    def insert_title(self, f, text):
        print(f'<h1>{text}</h1>', file=f)

    def insert_information(self, f, key, value, link):
        print(f'<img height="20px" src="imgs/profile-{key}.svg">', end=' ', file=f)
        if link is None:
            print(value, end=' ', file=f)
        else:
            print(f'<a href="{link}">{value}</a>', end=' ', file=f)

    def begin_itemize(self, f, node):
        if node['parent']['type'] != 'document':
            print('<ul class="small">', file=f)
        else:
            print('<ul>', file=f)

    def end_itemize(self, f, node):
        print('</ul>', file=f)

    def begin_enumerate(self, f, node):
        print('<ol>', file=f)

    def end_enumerate(self, f, node):
        print('</ol>', file=f)

    def begin_description(self, f, node):
        print('<div class="columns">', file=f)

    def end_description(self, f, node):
        print('</div>', file=f)

    def insert_item(self, f, node):
        text = self.process_text(node['text'])
        if 'label' in node:
            print(f'<div class="item"><div class="left">{node["label"]}</div><div class="right">{text}</div></div>', file=f)
        else:
            print(f'<li>{text}</li>', file=f)

    def insert_heading(self, f, node):
        h = f'h{node["depth"]+1}'
        text = self.process_text(node['text'])
        anchor = '-'.join(w.lower() for w in node['text'].split() if '!' not in w)
        print(f'<{h} id={anchor}>{text}</{h}>', file=f)

    def insert_paragraph(self, f, node):
        text = self.process_text(node['text'])
        print(f'<p>{text}</p>', file=f)

    def process_text(self, text):
        text = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img style="width:\1" src="\2">', text)  # images
        text = re.sub(r'\[\]\((.*?)\)', r'<a src="\1"><img width="20px" src="imgs/link.svg"></a>', text)  # empty links
        text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a src="\2">\1</a>', text)  # non-empty links
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  # bold
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)  # italic
        text = text.replace('&', '&amp;').replace('--', '&ndash;')
        text = text.replace('\n', '<br>\n')  # force breaklines
        text = re.sub(r'\=\=(.*?)\=\=', r'<span class="hl">\1</span>', text)  # highlight
        return text

class TEX:
    def begin_document(self, f, header):
        print(r'\documentclass[12pt]{article}', end='\n\n', file=f)
        print(r'\usepackage[a4paper, margin={2.5cm}]{geometry}', file=f)
        print(r'\setlength\parindent{0pt}', file=f)
        print(file=f)
        print(r'\usepackage{xcolor}', file=f)
        print(r'\usepackage{graphicx}', file=f)
        print(r'\usepackage[colorlinks=true, linkcolor=blue, urlcolor=blue, pdfauthor={Ricardo Cruz}, pdftitle={' + header['title'] + '}]{hyperref}', file=f)
        print(r'\usepackage{soulutf8}  % \hl', file=f)
        print(r'\usepackage{enumitem}', file=f)
        print(r'\newlength{\widestlabel}  % used by description', file=f)
        print(r'\setlist{nosep,leftmargin=0.4cm}', file=f)
        print(r'\usepackage{titlesec}  % change \section look', file=f)
        print(r'\titleformat{\section}{\normalfont\Large\scshape}{}{0pt}{}[{\vspace{-0.5ex}\titlerule[0.8pt]}]', file=f)
        print(r'\renewcommand{\thesection}{}  % no section numbers', file=f)
        print(r'\renewcommand{\thesubsection}{}', file=f)
        print(r'\renewcommand{\thesubsubsection}{}', file=f)
        print(r'\makeatletter\renewcommand\tableofcontents{\@starttoc{toc}}\makeatother', file=f)
        print(r'\usepackage{tocloft}\renewcommand{\cftsecleader}{\cftdotfill{\cftdotsep}}\renewcommand{\cftsubsecdotsep}{\cftnodots}\setlength{\cftbeforesecskip}{-.5ex}', file=f)
        print(r'\usepackage{parskip}  % gives more spacing', file=f)
        print(file=f)
        print(r'% footer', file=f)
        print(r'\usepackage{fancyhdr, lastpage}', file=f)
        print(r'\pagestyle{fancy}', file=f)
        print(r'\makeatletter\let\ps@plain\ps@fancy\makeatother', file=f)
        print(r'\renewcommand{\headrulewidth}{0pt}', file=f)
        print(r'\fancyhead{}', file=f)
        print(r'\fancyfoot[L]{\scriptsize Last update: \today}', file=f)
        print(r'\fancyfoot[C]{}', file=f)
        print(r'\fancyfoot[R]{\scriptsize Page \thepage\ of \pageref{LastPage}}', file=f)
        print(file=f)
        print(r'\begin{document}', end='\n\n', file=f)

    def end_document(self, f):
        print(r'\end{document}', file=f)

    def insert_toc(self, f, body):
        print(r'\setcounter{tocdepth}{2}\tableofcontents', end='\n\n', file=f)

    def insert_title(self, f, text):
        print(f'{{\Large {text}}}', end='\n\n', file=f)

    def insert_information(self, f, key, value, link):
        print(f'{{\\footnotesize \\raisebox{{-0.25\height}}{{\includegraphics[width=16px]{{imgs/profile-{key}}}}}~', end='', file=f)
        if link is None:
            print(value, end='', file=f)
        else:
            print(f'\href{{{link}}}{{{value}}}', end='', file=f)
        print('}', end='\n', file=f)

    def begin_itemize(self, f, node):
        print(r'\begin{itemize}', file=f)
        if node['parent']['type'] != 'document':
            # second degree itemize
            print(r'\footnotesize', file=f)

    def end_itemize(self, f, node):
        print(r'\end{itemize}', file=f)

    def begin_enumerate(self, f, node):
        print(r'\begin{enumerate}', file=f)

    def end_enumerate(self, f, node):
        print(r'\end{enumerate}', file=f)

    def begin_description(self, f, node):
        largest_label = max((c.get('label', '') for c in node['children']), key=len)
        print(f'\\settowidth{{\\widestlabel}}{{\\textbf{{{largest_label}}}}}', file=f)
        print(r'\begin{description}[style=sameline, labelwidth=\dimexpr\widestlabel+\labelsep, leftmargin=!]', file=f)

    def end_description(self, f, node):
        print(r'\end{description}', file=f)

    def insert_item(self, f, node):
        label = f'[{node["label"]}] ' if 'label' in node else ' '
        text = self.process_text(node['text'])
        print(f'\\item{label}{text}', file=f)

    def insert_heading(self, f, node):
        toc = ' '.join(w for w in node['text'].split() if '!' not in w)
        section = ('sub'*(node['depth']-1)) + 'section'
        text = self.process_text(node['text'])
        print(f'\\{section}[{toc}]{{{text}}}', file=f)

    def insert_paragraph(self, f, node):
        text = self.process_text(node['text'])
        print('\n' + text, file=f)

    def process_text(self, text):
        # two special cases for svg images
        text = re.sub(r'!\[\]\((.*?)\.svg\)', r'\\includegraphics[width=\\linewidth]{\1.pdf}', text)  # images without size
        text = re.sub(r'!\[(.*?)\]\((.*?)\.svg\)', r'\\includegraphics[width=\1]{\2.pdf}', text)  # images
        text = re.sub(r'!\[\]\((.*?)\)', r'\\includegraphics[width=\\linewidth]{\1}', text)  # images without size
        text = re.sub(r'!\[(.*?)\]\((.*?)\)', r'\\includegraphics[width=\1]{\2}', text)  # images
        text = re.sub(r'\[\]\((.*?)\)', r'\\href{\1}{\\includegraphics[width=0.8em]{imgs/link.pdf}}', text)  # empty links
        text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\\href{\2}{\1}', text)  # non-empty links
        text = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', text)  # bold
        text = re.sub(r'\*(.*?)\*', r'\\textit{\1}', text)  # italic
        text = re.sub(r'\=\=(.*?)\=\=', r'\\hl{\1}', text)  # highlight
        text = text.replace('&', r'\&').replace('~', r'$\sim$')  # escape symbols
        text = text.replace('\n', '\\\\\n')  # force breaklines
        text = re.sub(r'"(.*?)"', r"``\1''", text)
        return text

template = globals()[args.template.upper()]()
f = open(args.markdown[:-2] + args.template, 'w')

def process_ast(node):
    if 'children' in node:
        getattr(template, f"begin_{node['type']}")(f, node)
        for child in node['children']:
            process_ast(child)
        getattr(template, f"end_{node['type']}")(f, node)
    else:
        getattr(template, f"insert_{node['type']}")(f, node)

template.begin_document(f, ast['header'])
template.insert_title(f, ast['header']['title'])
if args.template == 'html':  # link to PDF version
    template.insert_information(f, 'pdf', 'PDF version', args.markdown[:-2] + 'pdf')
for key, value in ast['header'].items():
    link = None
    if key in 'title': continue
    if key == 'email': link = 'mailto:' + value
    if key == 'website': link = 'https://' + value
    if key == 'orcid': link = 'https://orcid.org/' + value
    template.insert_information(f, key, value, link)
template.insert_toc(f, ast['body']['children'])
for node in ast['body']['children']:
    process_ast(node)
template.end_document(f)

f.close()
