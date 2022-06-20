import os
import sys
import argparse
from urllib.parse import quote
from pdf_pipeline import (
    check_duplicate_pdf,
    parse_pdf_title,
    render_readme,
)

from pdf_pipeline import utils
from pdf_pipeline.configs import PDF_DIR, PROJ_DIR


def run_check_dup():
    return check_duplicate_pdf.main()


def run_gen_meta():
    pdf_files = utils.get_file_list(PDF_DIR, '.pdf')

    pdf_list = []
    titles = parse_pdf_title.parse_list(pdf_files)
    for pdf_path, title in sorted(titles.items(), key=lambda x: x[0]):
        pdf_list.append({
            'pdf_path': quote(os.path.relpath(pdf_path, PROJ_DIR)),
            'title': title,
        })

    data = {
        'pdf_list': pdf_list,
    }

    return render_readme.main(data)


pipelines = {
    'check-dup': run_check_dup,
    'gen-meta': run_gen_meta,
}

pipeline_choices = ', '.join(pipelines.keys())


def init_argparser():
    parser = argparse.ArgumentParser(description='Commond Line Interface for Paper Repo.')
    parser.add_argument(
        'pipeline', metavar='pipeline', type=str,
        choices=pipelines.keys(),
        help='choices: %s' % pipeline_choices)

    return parser


def run(args):
    pipe_func = pipelines[args.pipeline]
    return pipe_func()


def main():
    parser = init_argparser()
    args = parser.parse_args()

    err_no = run(args)
    return err_no


if __name__ == '__main__':
    err_no = main()
    sys.exit(err_no)
