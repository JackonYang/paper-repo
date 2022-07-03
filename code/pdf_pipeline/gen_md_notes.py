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
    TYPE_DEFAULT_TAG,
    REF_META_DIR,
)

TEMPLATE_DIR = os.path.join(PROJ_DIR)
TEMPLATE_NAME = 'md-notes.tmpl'

markdown_link_re = re.compile(r'\[(.*?)\]\((.*?)\)')
title_escape_re = re.compile(r'\s*(?:[":]+\s*)+')

default_status = 'todo'

ref_default_tag = os.environ.get('REF_DEFAULT_TAG', 'gen-from-ref')


meta_keys_from_yaml = [
    'title',
    'tags',
    'pdf_relpath',
]


def clean_content(content):
    if not content or not isinstance(content, str):
        return ''

    content = content.lstrip()

    pdf_link, new_content = content.split('\n', 1)
    if markdown_link_re.match(pdf_link):
        content = new_content.lstrip()

    return content


def iter_tag_map_filename(tag):
    subfix = '_paper-map.md'
    splitter = '/'
    parts = tag.split(splitter)
    for i in range(len(parts)):
        slug = '-'.join(parts[:i+1])
        new_tag = splitter.join(parts[:i+1])

        map_file = os.path.join(TAG_MAP_DIR, '%s%s' % (slug, subfix))
        if os.path.exists(map_file):
            break

        yield new_tag, map_file

    slug = tag.replace('/', '-')
    map_file = os.path.join(TAG_MAP_DIR, '%s%s' % (slug, subfix))
    if not os.path.exists(map_file):
        return tag, map_file


def add_missing_tag_map(tag_list):
    tasks = []
    for tag in tag_list:
        if tag == TYPE_DEFAULT_TAG:
            continue

        for new_tag, map_file in iter_tag_map_filename(tag):
            if not map_file:
                continue

            data = {
                'tag': new_tag,
                'type_tag': TYPE_DEFAULT_TAG,
            }
            tasks.append([data, map_file])

    for data, map_file in tasks:
        markdown_io.render_md(TEMPLATE_DIR, 'tag-map.tmpl', data, map_file)


def gen_from_pdf_yaml():
    meta_list = meta_io.get_meta_list()

    tag_list = []

    for meta in meta_list:

        meta_key = meta['meta_key']
        out_filename = os.path.join(MD_NOTES_DIR, '%s.md' % meta_key)

        heading_meta = {k: meta.get(k) for k in meta_keys_from_yaml}

        data = markdown_io.load_md_if_exists(out_filename)
        if 'meta' not in data:
            data['meta'] = {}

        heading_meta.update(data['meta'])
        data['meta'].update(meta)

        # ad-hoc changes for data migration
        # heading_meta['tags'].append('paper')

        for t in heading_meta['tags']:
            if t not in tag_list:
                tag_list.append(t)

        data['common_path'] = MD_NOTES_PDF_REL_ROOT

        # ad-hoc fields fix for rendering template
        data['meta'].update(heading_meta)
        heading_meta.pop('title')
        if 'Alias' in heading_meta:
            heading_meta.pop('Alias')
        heading_meta.setdefault('status', default_status)

        data['meta_str'] = yaml.dump(heading_meta).strip()
        data['content'] = clean_content(data['content'])

        markdown_io.render_md(TEMPLATE_DIR, TEMPLATE_NAME, data, out_filename)

    add_missing_tag_map(tag_list)

    print('success! %s notes udpated. notes_dir: %s' % (len(meta_list), MD_NOTES_DIR))


def gen_from_ref_yaml():
    meta_list = meta_io.get_meta_list(REF_META_DIR)

    tag_list = []

    for meta in meta_list:
        if 'title' not in meta:
            print(meta)
            continue

        meta_key = meta['meta_key']
        out_filename = os.path.join(MD_NOTES_DIR, '%s.md' % meta_key)

        if 'tags' not in meta:
            meta['tags'] = [ref_default_tag, TYPE_DEFAULT_TAG]
        elif ref_default_tag not in meta['tags']:
            meta['tags'].append(ref_default_tag)

        heading_meta = {k: meta.get(k) for k in meta_keys_from_yaml}

        data = markdown_io.load_md_if_exists(out_filename)
        if 'meta' not in data:
            data['meta'] = {}

        heading_meta.update(data['meta'])
        data['meta'].update(meta)

        # ad-hoc changes for data migration
        # heading_meta['tags'].append('paper')

        for t in heading_meta['tags']:
            if t not in tag_list:
                tag_list.append(t)

        data['common_path'] = MD_NOTES_PDF_REL_ROOT
        data['notes_common_path'] = '.'  # current dir

        # ad-hoc fields fix for rendering template
        data['meta'].update(heading_meta)
        heading_meta.pop('title')
        if 'Alias' in heading_meta:
            heading_meta.pop('Alias')
        heading_meta.setdefault('status', default_status)

        data['meta_str'] = yaml.dump(heading_meta).strip()
        data['content'] = clean_content(data['content'])

        data['render_ref_list'] = 'references' not in data['content'].lower()

        markdown_io.render_md(TEMPLATE_DIR, TEMPLATE_NAME, data, out_filename)

    add_missing_tag_map(tag_list)

    print('success! %s notes udpated. notes_dir: %s' % (len(meta_list), MD_NOTES_DIR))


def main():
    gen_from_pdf_yaml()
    gen_from_ref_yaml()
