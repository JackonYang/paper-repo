import os
import re
import codecs
import yaml
import copy

from jinja2 import Environment, FileSystemLoader


META_BOUNDARY = re.compile(r'^-{3,}\s*$', re.MULTILINE)


default_data = {
    'meta': {},
    'content': '',
}


def render_md(template_dir, template_name, data, out_filename):
    env = Environment(
        loader=FileSystemLoader(template_dir),
        keep_trailing_newline=True)
    template = env.get_template(template_name)

    content = template.render(data)

    with codecs.open(out_filename, 'w', 'utf8') as f:
        f.write(content)


def split_meta(content):

    meta = {}

    if META_BOUNDARY.match(content):
        _, fm, content = META_BOUNDARY.split(content, 2)
        meta = yaml.safe_load(fm.strip()) or {}

    data = {
        'meta': meta,
        'content': content.strip(),
    }
    return data


def load_md(filepath):

    with open(filepath, 'r') as fr:
        content = fr.read()

    return split_meta(content)


def load_md_if_exists(filepath):
    data = copy.deepcopy(default_data)
    if os.path.exists(filepath):
        data = load_md(filepath)

    return data
