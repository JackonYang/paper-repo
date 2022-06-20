import os
from urllib.parse import quote

from .configs import (
    PDF_DIR,
    PROJ_DIR,
)
from . import meta_io
from . import utils
from .parsers import parse_pdf_title


def update_file_facts(pdf_path):
    meta_key = meta_io.filepath2key(pdf_path)

    basename = os.path.basename(pdf_path)
    raw_filename, ext = os.path.splitext(basename)

    filesize = os.path.getsize(pdf_path)

    context = {
        'mata_key': meta_key,
        'raw_filename': raw_filename,
        'raw_ext': ext,
        'filesize': filesize,
        'filesize_readable': utils.getSizeInNiceString(filesize),
        'content_md5': utils.md5_for_file(pdf_path),
        'url_slug': quote(raw_filename),
        'pdf_relpath': quote(os.path.relpath(pdf_path, PROJ_DIR)),
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


def gen_meta(pdf_path):
    update_file_facts(pdf_path)

    meta_key = meta_io.filepath2key(pdf_path)
    guess_from_filename(meta_key)


def main():
    pdf_files = utils.get_file_list(PDF_DIR, '.pdf')

    for pdf_path in pdf_files:
        gen_meta(pdf_path)
