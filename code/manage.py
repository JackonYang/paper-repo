import os
from pdf_pipeline import (
    # check_duplicate_pdf,
    parse_pdf_title,
)

from pdf_pipeline import utils
from pdf_pipeline.configs import PDF_DIR, PROJ_DIR


def main():
    pdf_files = utils.get_file_list(PDF_DIR, '.pdf')

    data = []

    # check_duplicate_pdf.main(pdf_files)
    titles = parse_pdf_title.parse_list(pdf_files)
    for pdf_path, title in titles.items():
        data.append({
            'pdf_path': os.path.relpath(pdf_path, PROJ_DIR),
            'title': title,
        })

    print(data[0])


if __name__ == '__main__':
    main()
