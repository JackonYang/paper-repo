import os
from urllib.parse import quote
from pdf_pipeline import (
    # check_duplicate_pdf,
    parse_pdf_title,
    render_readme,
)

from pdf_pipeline import utils
from pdf_pipeline.configs import PDF_DIR, PROJ_DIR


def main():
    pdf_files = utils.get_file_list(PDF_DIR, '.pdf')

    pdf_list = []

    # check_duplicate_pdf.main(pdf_files)
    titles = parse_pdf_title.parse_list(pdf_files)
    for pdf_path, title in sorted(titles.items(), key=lambda x: x[0]):
        pdf_list.append({
            'pdf_path': quote(os.path.relpath(pdf_path, PROJ_DIR)),
            'title': title,
        })

    data = {
        'pdf_list': pdf_list,
    }

    render_readme.main(data)


if __name__ == '__main__':
    main()
