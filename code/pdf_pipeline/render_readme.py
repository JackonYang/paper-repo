import os

from . import meta_io
from . import markdown_io

from .configs import PROJ_DIR


OUT_FILENAME = os.path.join(PROJ_DIR, 'README.md')
TEMPLATE_DIR = os.path.join(PROJ_DIR)
TEMPLATE_NAME = 'readme.tmpl'


def main():
    meta_list = meta_io.get_meta_list()

    data = {
        'meta_list': meta_list,
    }

    # print(meta_list[0])
    markdown_io.render_md(TEMPLATE_DIR, TEMPLATE_NAME, data, OUT_FILENAME)

    print('success! saved in %s' % os.path.abspath(OUT_FILENAME))
