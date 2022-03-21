blocks = {
    'begin_document': '',
    'end_document': '',

    'begin_section': lambda section: '''<html>
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
&bull; Invited Assistant Professor
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
<ul>
<li><a %shref="index.html">Publications</a></li>
<li><a %shref="projects.html">Projects</a></li>
<li><a %shref="teaching.html">Teaching</a></li>
<li><a %shref="supervisions.html">Supervisions</a></li>
<li><a %shref="videos.html">Videos</a></li>
<li><a %shref="awards.html">Awards</a></li>
</ul>
</div>

<div class="content">
''' % ('class="active"' if section == 'Publications' else '', 'class="active"' if section == 'Projects' else '', 'class="active"' if section == 'Teaching' else '', 'class="active"' if section == 'Supervisions' else '', 'class="active"' if section == 'Videos' else '', 'class="active"' if section == 'Awards' else ''),
    'end_section': '''</div>
</body>
</html>''',

    'year': '<p class="year">{}</p>',

    'begin_item': '<div class="item">',
    'end_item': '</div>',
    'begin_item_hl': '<div class="item highlight">',
    'end_item_hl': '</div>',
    'begin_item_link': '<a class="item" href="{}">',
    'end_item_link': '</a>',
    'begin_item_link_hl': '<a class="item highlight" href="{}">',
    'end_item_link_hl': '</a>',

    'image': lambda imgs: ' '.join('<img src="imgs/{}">'.format(img) for img in imgs),
    'title': '<p><b>{}</b></p>',
    'subtitle': '<p>{}</p>',
    'description': '<p><small>{}</small></p>',
    'same_file': False,
}
