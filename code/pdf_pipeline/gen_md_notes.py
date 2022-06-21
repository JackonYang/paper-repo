import os

from . import meta_io
from . import markdown_io

from .configs import (
    MD_NOTES_PDF_REL_ROOT,
    PROJ_DIR,
    MD_NOTES_DIR,
)

TEMPLATE_DIR = os.path.join(PROJ_DIR)
TEMPLATE_NAME = 'md-notes.tmpl'


def main():
    meta_list = meta_io.get_meta_list()

    for meta in meta_list:

        meta_key = meta['meta_key']
        out_filename = os.path.join(MD_NOTES_DIR, '%s.md' % meta_key)

        data = markdown_io.load_md_if_exists(out_filename)
        if 'meta' in data:
            data['meta'].update(meta)
        else:
            data['meta'] = meta

        data['common_path'] = MD_NOTES_PDF_REL_ROOT

        markdown_io.render_md(TEMPLATE_DIR, TEMPLATE_NAME, data, out_filename)

    print('success! %s notes udpated. notes_dir: %s' % (len(meta_list), MD_NOTES_DIR))
