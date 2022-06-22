import os
from urllib.parse import quote

from .configs import (
    META_DIR,
    PDF_DIR,
    PROJ_DIR,
)
from . import meta_io
from . import utils
from .parsers import parse_pdf_title


# read default tag from env
default_tag = os.environ.get('DEFAULT_TAG', 'other-default')


def update_file_facts(pdf_path):
    meta_key = meta_io.filepath2key(pdf_path)
    meta_path = meta_io.key2meta_path(meta_key)

    basename = os.path.basename(pdf_path)
    raw_filename, ext = os.path.splitext(basename)

    filesize = os.path.getsize(pdf_path)

    context = {
        'meta_key': meta_key,
        'raw_filename': raw_filename,
        'raw_ext': ext,
        'filesize': filesize,
        'filesize_readable': utils.getSizeInNiceString(filesize),
        'content_md5': utils.md5_for_file(pdf_path),
        'url_slug': quote(raw_filename),
        'pdf_relpath': quote(os.path.relpath(pdf_path, PROJ_DIR)),
        'meta_relpath': quote(os.path.relpath(meta_path, PROJ_DIR)),
    }

    meta_io.update_meta(meta_key, context)


def guess_from_filename(meta_key):
    meta = meta_io.read_meta(meta_key)

    assert 'raw_filename' in meta
    raw_filename = meta['raw_filename']

    title = parse_pdf_title.format_title(raw_filename)

    context = {
        'title': title,
    }

    meta_io.update_meta(meta_key, context)


def add_default_tags(meta_key):
    meta = meta_io.read_meta(meta_key)

    if 'tags' not in meta:
        meta['tags'] = [default_tag, 'paper']
        meta_io.update_meta(meta_key, meta)


def gen_meta(pdf_path):
    update_file_facts(pdf_path)

    meta_key = meta_io.filepath2key(pdf_path)
    guess_from_filename(meta_key)
    add_default_tags(meta_key)


def clean_extra_meta():
    pdf_files = utils.get_filename_list(PDF_DIR, '.pdf')
    meta_files = utils.get_filename_list(META_DIR, '.yaml')

    extra = set(meta_files) - set(pdf_files)
    for meta_key in extra:
        meta_io.remove(meta_key)


def main():
    clean_extra_meta()

    pdf_files = utils.get_file_list(PDF_DIR, '.pdf')

    for pdf_path in pdf_files:
        gen_meta(pdf_path)
