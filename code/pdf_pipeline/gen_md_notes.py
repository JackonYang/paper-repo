import os
import re

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


def clean_content(content):
    content = content.lstrip()

    pdf_link, new_content = content.split('\n', 1)
    if markdown_link_re.match(pdf_link):
        content = new_content.lstrip()

    if content.startswith('#'):
        groups = content.split('\n', 1)
        if len(groups) == 1:
            content = ''
        else:
            content = groups[1].lstrip()

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

        data = markdown_io.load_md_if_exists(out_filename)
        if 'meta' in data:
            data['meta'].update(meta)
        else:
            data['meta'] = meta

        if 'tags' not in data['meta']:
            data['meta']['tags'] = 'other-default'

        for t in data['meta']['tags'].split(','):
            if t not in tag_list:
                tag_list.append(t)

        data['common_path'] = MD_NOTES_PDF_REL_ROOT
        data['content'] = clean_content(data['content'])

        markdown_io.render_md(TEMPLATE_DIR, TEMPLATE_NAME, data, out_filename)

    add_missing_tag_map(tag_list)

    print('success! %s notes udpated. notes_dir: %s' % (len(meta_list), MD_NOTES_DIR))