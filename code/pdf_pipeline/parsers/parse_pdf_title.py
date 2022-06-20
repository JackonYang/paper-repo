import os
import re

raw_title_flags = [
    ' ',
]

replace_by_default = [
    ('_', ' '),
]

replace_final = [
    ('-', ' '),
]


leading_year = re.compile(r'^(\d{4})\W')
language_info = re.compile(r'\W+(cn|en)\b')
edition_info = re.compile(r'\W+(1st|2nd|3rd|\dth|ed\d)\b.*$')


def format_title(title):
    m = leading_year.findall(title)
    if m:
        year = m[0]
        title = '%s(%s)' % (title[5:], year)

    for c1, c2 in replace_by_default:
        title = title.replace(c1, c2)

    m = language_info.findall(title)
    if m:
        lang = m[0]
        title = re.sub(language_info, '', title) + '(%s)' % lang

    # m = edition_info.findall(title)
    # if m:
    title = re.sub(edition_info, '', title)

    for c in raw_title_flags:
        if c in title:
            return title

    for c1, c2 in replace_final:
        title = title.replace(c1, c2)

    return title.title()


def parse_title_from_path(pdf_path):
    basename = os.path.basename(pdf_path)
    title, ext = os.path.splitext(basename)
    return format_title(title)


def parse(pdf_path):
    """
    Parses the title of a PDF file.
    :param pdf_path: path to the PDF file
    :return: title of the PDF file
    """
    return parse_title_from_path(pdf_path)


def parse_list(pdf_list):
    """
    Parses the title of a PDF file.
    :param pdf_path: path to the PDF file
    :return: title of the PDF file
    """
    pdf_titles = {}
    for pdf_path in pdf_list:
        pdf_titles[pdf_path] = parse(pdf_path)

    return pdf_titles
