import sys
import argparse
from pdf_pipeline import (
    check_duplicate_pdf,
    gen_meta_data,
    render_readme,
    gen_md_notes,
)


def run_check_dup():
    return check_duplicate_pdf.main()


def run_gen_meta():
    gen_meta_data.main()
    return render_readme.main()


def run_update_readme():
    return render_readme.main()


def run_gen_md_notes():
    return gen_md_notes.main()


pipelines = {
    'check-dup': run_check_dup,
    'gen-meta': run_gen_meta,
    'update-readme': run_update_readme,
    'gen-notes-md': run_gen_md_notes,
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
