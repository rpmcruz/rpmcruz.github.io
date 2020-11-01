import argparse
parser = argparse.ArgumentParser()
parser.add_argument('yaml')
parser.add_argument('template')
args = parser.parse_args()

from jinja2 import Template
import yaml
cv = yaml.load(open(args.yaml), Loader=yaml.Loader)
template = Template(open(args.template).read(), trim_blocks=True, lstrip_blocks=True)
out = template.render(**cv)

outname = args.yaml.split('.')[0] + '.' + args.template.split('.')[-1]
open(outname, 'w').write(out)

