import argparse
parser = argparse.ArgumentParser()
parser.add_argument('yaml')
parser.add_argument('template')
parser.add_argument('output')
args = parser.parse_args()

from jinja2 import Template
import yaml
cv = yaml.load(open(args.yaml), Loader=yaml.Loader)
template = Template(open(args.template).read(),
    trim_blocks=True, lstrip_blocks=True,
    block_start_string='@%', block_end_string='%@',
    variable_start_string='@@', variable_end_string='@@',
    comment_start_string='@#', comment_end_string='#@')
out = template.render(cv=cv)
open(args.output, 'w').write(out)
