import os

PROJ_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..'))

PDF_DIR = os.path.join(PROJ_DIR, 'pdfs')
META_DIR = os.path.join(PROJ_DIR, 'metas')


if __name__ == '__main__':
    print(PROJ_DIR)
    print('exists: %s' % os.path.exists(PROJ_DIR))
    # print(PDF_DIR)
    # print(META_DIR)
