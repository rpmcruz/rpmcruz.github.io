import argparse
parser = argparse.ArgumentParser()
parser.add_argument('yaml')
parser.add_argument('format', choices=['html', 'tex'])
args = parser.parse_args()

import yaml
cv = yaml.load(open(args.yaml), Loader=yaml.Loader)

if args.format == 'html':
    from blocks_html import blocks
else:
    from blocks_tex import blocks

if blocks['same_file']:
    f = open(f'cv.{args.format}', 'w')
    print(blocks['begin_document'], file=f)
for si, section_name in enumerate(['Publications', 'Projects', 'Teaching', 'Supervisions', 'Videos', 'Awards']):
    if not blocks['same_file']:
        filename = 'index.html' if si == 0 else f'{section_name.lower()}.{args.format}'
        f = open(filename, 'w')
    print(blocks['begin_section'](section_name), file=f)
    section = cv[section_name.lower()]
    prev_year = None
    if args.format == 'html':
        if section_name == 'Publications':
            print('<p>Some of my favorite publications are <span style="border:1px dashed black;">highlighted</span>.</p>', file=f)
    for item in section:
        year = item.get('year')
        if year != prev_year:
            print(blocks['year'].format(year), file=f)
            prev_year = year
        hlsuffix = '_hl' if item.get('highlight') else ''
        if 'link' in item:
            print(blocks['begin_item_link' + hlsuffix].format(item['link']), file=f)
        else:
            print(blocks['begin_item' + hlsuffix], file=f)
        if 'image' in item:
            print(blocks['image'].format(item['image']), file=f)
        for field in ['title', 'subtitle', 'description']:
            if field in item:
                print(blocks[field].format(item[field]), file=f)
        if 'link' in item:
            print(blocks['end_item_link' + hlsuffix], file=f)
        else:
            print(blocks['end_item' + hlsuffix], file=f)
    if args.format == 'html':
        if section_name == 'Projects':
            print('<p style="margin-top:20px">Find more of my code at <a href="https://github.com/rpmcruz?tab=repositories">github.com/rpmcruz</a></p>', file=f)
    print(blocks['end_section'].format(section_name), file=f)
if blocks['same_file']:
    print(blocks['end_document'], file=f)
