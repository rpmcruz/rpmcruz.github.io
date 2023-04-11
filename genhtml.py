import argparse
parser = argparse.ArgumentParser()
parser.add_argument('yaml')
args = parser.parse_args()

sections = ['Education', 'Employment', 'Teaching', 'Publications', 'Projects',
    'Supervisions', 'Awards']

def escape(s):
    return s.replace('--', '&ndash;')

import yaml
cv = yaml.load(open(args.yaml), Loader=yaml.Loader)

f = open('index.html', 'w')

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
print('h2 {border-bottom: 2px solid}', file=f)
print('a {text-decoration: none}', file=f)
print('a:hover {text-decoration: underline}', file=f)
print('.sc {font-variant: small-caps}', file=f)
print('.small {font-size: small; color: gray}', file=f)
print('.hl {background-color: yellow}', file=f)
print('.nobr {white-space: nowrap}', file=f)
print('.bigskip {margin-top: 30px}', file=f)
print('ul.menu {position: fixed; top: 0; right: 0; list-style: none; margin-right: 30px}', file=f)
print('ul.menu a {display: block}', file=f)
print('@media screen and (min-width: 768px) {body {margin: auto; text-align: justify} div.columns {display: flex} div.left {width: 150px} div.right {flex: 1} .desktop {display: block}}', file=f)
print('@media screen and (max-width: 767px) {body {margin-left: 6px; margin-right: 6px} .desktop {display: none}}', file=f)
print('</style>', file=f)
print('</head>', file=f)
print(file=f)

print('<body id="top">', file=f)

print('<ul class="menu desktop">', file=f)
print(f'<li><a href="#top">Top</a></li>', file=f)
for section in sections:
    print(f'<li><a href="#{section.lower()}">{section}</a></li>', file=f)
print('</ul>', file=f)

print('<h1>Ricardo Cruz, PhD</h1>', file=f)
print('<img height="20px" src="imgs/icon-mail.svg"> <a href="mailto:ricardo.pdm.cruz@gmail.com">ricardo.pdm.cruz@gmail.com</a> <span class="nobr"><img height="20px" src="imgs/pdf.svg"> <a href="rpcruz-cv.pdf">PDF version</a></span>', file=f)

print(f'<p class="bigskip">{cv["summary"]}</p>', file=f)

print('<p><span class="sc">Skills:</span>', end=' ', file=f)
for i, skill in enumerate(cv['skills']):
    if i > 0:
        print(end=r' &middot; ', file=f)
    print(end=skill, file=f)
print('</p>', file=f)

print(r'<img width="100%" src="imgs/lecture.jpg">', file=f)

for section in sections:
    print(f'<h2 id={section.lower()}><img width="40px" src="imgs/{section.lower()}.svg"> {section}</h2>', file=f)
    for item in cv[section.lower()]:
        print('<div class="columns">', file=f)
        print('<div class="left">', file=f)
        if 'year' in item:
            print(escape(str(item['year'])), file=f)
        if 'duration' in item:
            print(f"<br><i>{item['duration']}</i>", file=f)
        print('</div>', file=f)
        print('<div class="right">', file=f)
        print(end='<p>', file=f)
        if 'highlight' in item:
            print(f'<span class="hl"><b>{escape(item["title"])}</b></span>', file=f)
        else:
            print(f'<b>{escape(item["title"])}</b>', file=f)
        if 'link' in item:
            print(f'<a href="{item["link"]}"><img width="20px" src="imgs/link.svg"></a>', file=f)
        print('</p>', file=f)
        print(f"<p>{escape(item['subtitle'])}</p>", file=f)
        if 'summary' in item:
            print('<ul class="small">', file=f)
            for subitem in item['summary']:
                print(f'<li>{escape(subitem)}</li>', file=f)
            print('</ul>', file=f)
        print('</div>', file=f)
        print('</div>', file=f)
    if section == 'Projects':
        print('<p class="bigskip">See my github for more projects: <a href="https://github.com/rpmcruz?tab=repositories">github.com/rpmcruz</a></p>', file=f)
    if section == 'Publications':
        print('<p class="bigskip">My favorite publications are in <span class="hl"><b>highlight</b></span>. See my Google Scholar for more information: <a href="https://scholar.google.com/citations?user=pSFY_gQAAAAJ">scholar.google.com/citations?user=pSFY_gQAAAAJ</a></p>', file=f)

from datetime import datetime
print(f'<center class="bigskip small">Last update: {datetime.today().strftime("%Y-%m-%d")}</center>', file=f)

print(r'</body>', file=f)
f.close()
