from .configs import PDF_DIR

from . import utils


def check_by_md5(pdf_files):
    pdf_md5s = {}
    has_dup = False

    for pdf_file in pdf_files:
        md5 = utils.md5_for_file(pdf_file)
        if md5 in pdf_md5s:
            has_dup = True
            print('===== dup found =====')
            print('md5: %s' % md5)
            print('file1: %s' % pdf_file)
            print('file2: %s' % pdf_md5s[md5])
        else:
            pdf_md5s[md5] = pdf_file

    if not has_dup:
        print('no dup found by md5')

    return has_dup


def main():
    pdf_files = utils.get_file_list(PDF_DIR, '.pdf')

    has_dup = check_by_md5(pdf_files)
    if has_dup:
        return


if __name__ == '__main__':
    main()
