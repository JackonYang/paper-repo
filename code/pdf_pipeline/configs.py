import os

PROJ_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..'))

PDF_DIR = os.path.join(PROJ_DIR, 'pdfs')
META_DIR = os.path.join(PROJ_DIR, 'metas')
REF_META_DIR = os.path.join(PROJ_DIR, 'ref-metas')

REFERENCE_INFO_DIR = os.path.join(PROJ_DIR, 'extra-data/ref-info')

MD_NOTES_DIR = os.path.join(PROJ_DIR, '../01-zettelkasten/02-References')
MD_NOTES_PDF_REL_ROOT = '../../..'

TAG_MAP_DIR = os.path.join(PROJ_DIR, '../01-zettelkasten/06-Content Maps')

TYPE_DEFAULT_TAG = 'paper'


if __name__ == '__main__':
    print(PROJ_DIR)
    print('exists: %s' % os.path.exists(PROJ_DIR))
    # print(PDF_DIR)
    # print(META_DIR)
