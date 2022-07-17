import os
import re
import yaml
import copy

from . import meta_io
from . import markdown_io
from .utils import get_file_list

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

default_status = 'todo'


meta_keys_from_yaml = [
    'title',
    'tags',
    'pdf_relpath',
    'authors',
    'fieldsOfStudy',
    'meta_key',
    'numCitedBy',
    'ref_count',
    'venue',
    'year',
]


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
