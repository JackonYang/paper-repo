import os
import re
import yaml

from . import meta_io
from . import markdown_io

from .configs import (
    MD_NOTES_PDF_REL_ROOT,
    PROJ_DIR,
    MD_NOTES_DIR,
    TAG_MAP_DIR,
)

TEMPLATE_DIR = os.path.join(PROJ_DIR)
TEMPLATE_NAME = 'md-notes.tmpl'

markdown_link_re = re.compile(r'\[(.*?)\]\((.*?)\)')


meta_keys_from_yaml = [
    'title',
    'tags',
]


def clean_content(content):
    if not content or not isinstance(content, str):
        return ''

    content = content.lstrip()

    pdf_link, new_content = content.split('\n', 1)
    if markdown_link_re.match(pdf_link):
        content = new_content.lstrip()

    return content


def add_missing_tag_map(tag_list):
    for t in tag_list:
        map_file = os.path.join(TAG_MAP_DIR, '%s Paper Map.md' % t)
        if os.path.exists(map_file):
            continue

        data = {
            'tag': t,
        }

        markdown_io.render_md(TEMPLATE_DIR, 'tag-map.tmpl', data, map_file)


def main():
    meta_list = meta_io.get_meta_list()

    tag_list = []

    for meta in meta_list:

        meta_key = meta['meta_key']
        out_filename = os.path.join(MD_NOTES_DIR, '%s.md' % meta_key)

        heading_meta = {k: meta[k] for k in meta_keys_from_yaml}

        data = markdown_io.load_md_if_exists(out_filename)
        if 'meta' not in data:
            data['meta'] = {}

        heading_meta.update(data['meta'])
        data['meta'].update(meta)

        for t in data['meta']['tags']:
            if t not in tag_list:
                tag_list.append(t)

        data['common_path'] = MD_NOTES_PDF_REL_ROOT

        heading_meta.pop('title')
        data['meta_str'] = yaml.dump(heading_meta)
        data['content'] = clean_content(data['content'])

        markdown_io.render_md(TEMPLATE_DIR, TEMPLATE_NAME, data, out_filename)

    add_missing_tag_map(tag_list)

    print('success! %s notes udpated. notes_dir: %s' % (len(meta_list), MD_NOTES_DIR))
