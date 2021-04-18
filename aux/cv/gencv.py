import argparse
parser = argparse.ArgumentParser()
parser.add_argument('yaml')
parser.add_argument('template')
parser.add_argument('output')
args = parser.parse_args()

import re
def myurlize(text, start_block, end_block):
    return re.sub(r'(http\S+)', start_block + r'\1' + end_block, text)

from jinja2 import Template
import yaml
cv = yaml.load(open(args.yaml), Loader=yaml.Loader)
template = Template(open(args.template).read(),
    trim_blocks=True, lstrip_blocks=True,
    block_start_string='@%', block_end_string='%@',
    variable_start_string='@@', variable_end_string='@@',
    comment_start_string='@#', comment_end_string='#@')
out = template.render(cv=cv, myurlize=myurlize)
open(args.output, 'w').write(out)
