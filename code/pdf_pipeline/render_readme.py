import os
import codecs

from jinja2 import Environment, FileSystemLoader

from .configs import PROJ_DIR

OUT_FILENAME = os.path.join(PROJ_DIR, 'README.md')
TEMPLATE_DIR = os.path.join(PROJ_DIR)
TEMPLATE_NAME = 'readme.tmpl'


def render_md(template_dir, template_name, data, out_filename):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)

    content = template.render(data)

    with codecs.open(out_filename, 'w', 'utf8') as f:
        f.write(content)

    print('success! saved in %s' % os.path.abspath(out_filename))


def main(data):
    render_md(TEMPLATE_DIR, TEMPLATE_NAME, data, OUT_FILENAME)
