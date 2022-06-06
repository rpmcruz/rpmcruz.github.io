import argparse
parser = argparse.ArgumentParser()
parser.add_argument('yaml')
args = parser.parse_args()

import yaml
cv = yaml.load(open(args.yaml), Loader=yaml.Loader)

def escape(x):
    return str(x).replace('--', '&mdash;')

sections = ['Publications', 'Supervisions', 'Career', 'Projects', 'Videos', 'Awards']

for si, section_name in enumerate(sections):
    filename = '../index.html' if si == 0 else f'../{section_name.lower()}.html'
    f = open(filename, 'w')
    print(f'''<html>
<head>
<meta charset="utf-8" />
<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<link rel="stylesheet" type="text/css" href="style.css" />
<title>Ricardo Cruz</title>
</head>

<body>

<div class="header">
<div class="content">

<div class="flex" style="text-align:left;">
<div>
<img width="128" height="112" src="imgs/photo.png"><br>
&bull; Post-doc Researcher<br>
</div>

<div>
<h1>Ricardo Cruz, PhD</h1>
<img width="14" height="14" src="imgs/email.svg"> <a href="mailto:ricardo.pdm.cruz@gmail.com">ricardo.pdm.cruz@gmail.com</a><br>
<img width="14" height="14" src="imgs/github.svg"> <a href="https://github.com/rpmcruz">github.com/rpmcruz</a><br>
<img width="14" height="14" src="imgs/location.svg"> Porto, Portugal
</div>

</div>

<p>Ricardo Cruz earned his Ph.D. in Computer Science in 2021 with special emphasis on computer vision and deep learning. He is currently a post-doc doing research on autonomous driving under the EU research project THEIA, and is also an Invited Assistant Professor at FEUP.</p>
</div>
</div>

<div class="content menu">
<ul>''', file=f)
    for i, s in enumerate(sections):
        href = 'index.html' if i == 0 else f'{s.lower()}.html'
        if i == si:
            print(f'<li><a class="active" href="{href}">{s}</a></li>', file=f)
        else:
            print(f'<li><a href="{href}">{s}</a></li>', file=f)
    print('''</ul>
</div>
<div class="content">
''', file=f)

    if section_name == 'Publications':
        print('<p>Some of my favorite publications are <span class="highlight">highlighted</span>.</p>', file=f)
    for year in cv[section_name.lower()]:
        if 'year' in year:
            print(f'<p class="year">{escape(year["year"])}</p>', file=f)
        print(f'<ul>', file=f)
        for item in year['items']:
            print(f'<li>', file=f)
            if 'title' in item:
                if item.get('highlight'):
                    print(f'<span class="highlight">', file=f)
                if 'link' in item:
                    print(f'<a href="{item["link"]}">', file=f)
                print(f'<b>{escape(item["title"])}</b>', file=f)
                if 'link' in item:
                    print(f'</a>', file=f)
                if item.get('highlight'):
                    print(f'</span>', file=f)
            if 'subtitle' in item:
                print(f'<br>{escape(item["subtitle"])}', file=f)
            if 'description' in item:
                print(f'<br><span class="description">{escape(item["description"])}</span>', file=f)
            if 'image' in item:
                imgs = item['image'] if type(item['image']) is list else [item['image']]
                print(f'<br>', file=f)
                print(''.join(f'<img src="imgs/{img}">' for img in imgs), file=f)
            print(f'</li>', file=f)
        print(f'</ul>', file=f)
    if section_name == 'Projects':
        print('<p style="margin-top:20px">Find more of my code at <a href="https://github.com/rpmcruz?tab=repositories">github.com/rpmcruz</a></p>', file=f)
    print('''</div>\n</body>\n</html>''', file=f)
f.close()
