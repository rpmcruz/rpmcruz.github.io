import json, re
import sys

class Latex:
    def begin(self, name):
        print(r'\documentclass[12pt]{article}')
        print(r'\usepackage[a4paper, margin=3cm]{geometry}')
        print(r'\usepackage{longtable}')
        print(r'\usepackage{graphicx}')
        print(r'\usepackage[hidelinks]{hyperref}')
        print(f'\\title{{{name}}}')
        print(r'\begin{document}')
        print(r'\maketitle')

    def end(self):
        print(r'\end{document}')

    def markdown(self, text, newline=r'\\'):
        text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1 \\href{\2}{\\includegraphics[width=0.8em]{imgs/link.pdf}}', text)  # links
        text = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', text)  # bold
        text = re.sub(r'\*(.*?)\*', r'\\textit{\1}', text)  # italic
        text = re.sub(r'\=\=(.*?)\=\=', r'\\hl{\1}', text)  # highlight
        text = text.replace('&', r'\&').replace('~', r'$\sim$')  # escape symbols
        text = text.replace('\n', newline + '\n')  # force breaklines
        text = re.sub(r'"(.*?)"', r"``\1''", text)
        return text

    def contacts(self, contacts):
        for icon, text, link in contacts:
            print(f'\\includegraphics[width=0.5cm]{{imgs/{icon}.pdf}} \\href{{{link}}}{{{text}}} ')
        print('\n')

    def section(self, icon, text):
        print(f'\\section{{\\includegraphics[width=1cm]{{imgs/{icon}.pdf}} {text}}}')

    def paragraph(self, text):
        print(self.markdown(text), end='\n\n')

    def description(self, items):
        print(r'\begin{description}')
        for label, text in items:
            print(f'\\item[{label}] {self.markdown(text)}')
        print(r'\end{description}')

    def table(self, rows, filters, columns_type, columns_sort, columns_size):
        sizes = '|'.join(f'p{{{size}}}' if size else 'l' for size in columns_size)
        print(r'{\small\begin{longtable}{|' + sizes + '|}')
        print(r'\hline')
        print('&'.join(rows[0]) + r'\\')
        print(r'\hline\endhead')
        for row in rows:
            print('&'.join(self.markdown(str(v), r'\newline') for v in row.values()) + r'\\')
            print(r'\hline')
        print(r'\end{longtable}}')

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
        print('h1 {background-image:url("imgs/lecture.jpg"); background-size:cover; height:180px; color:white; text-align:center; text-shadow:-2px -2px 2px black, 2px -2px 2px black, -2px 2px 2px black, 2px 2px 2px black;}')
        print('h2 {margin-top:50px; border-bottom:solid;}')
        print('.container {max-width:800px; margin:0 auto;}')
        print('table {width:100%; text-align:left;}')
        # description
        print('@media screen and (min-width:1000px) {div.description {display:flex; flex-direction: column;} div.item {display:flex;} div.left {width:4em; font-weight:bold;} div.right {flex: 1;}')
        print('@media screen and (max-width:999px) {div.item {display:inline;} div.left {display:inline;font-weight:bold;} div.right{display:inline;}}')
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

    def section(self, icon, text):
        print(f'<h2><img width="45px" src="imgs/{icon}.svg"> {text}</h2>')

    def paragraph(self, text):
        print('<p>' + self.markdown(text) + '</p>')

    def description(self, items):
        print('<div class="description">')
        for label, text in items:
            print(f'<div class="item"><div class="left">{label}</div><div class="right">{self.markdown(text)}</div></div>')
        print('</div>')

    def table(self, rows, filters, columns_type, columns_sort, columns_size=None):
        print(f'<div id="filters{self.tables}"></div>')
        print('</div>')  # temporarily disable container
        print(f'<div id="table{self.tables}"></div>')
        print('<div class="container">')  # re-enable container
        print('<script>')
        rows = [{key: self.markdown(str(value)) for key, value in row.items()} for row in rows]
        print(f'table = new Table("table{self.tables}", ' + json.dumps(list(rows[0].keys())) + ', ' + json.dumps(columns_type) + ', ' + json.dumps(columns_sort) + ', ' + json.dumps(rows) + ');')
        filters = {f: list(sorted(set(r[f] for r in rows))) for f in filters}
        print(f'new Filters(table, "filters{self.tables}", ' + json.dumps(filters) + ');')
        print('</script>')
        self.tables += 1
