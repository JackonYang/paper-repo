import os
from .api import download_ref_links

CUR_DIR = os.path.abspath(os.path.dirname(__file__))


def read_urls_from_file(file_path):
    with open(file_path, 'r') as f:
        data = f.readlines()
    return [i.strip() for i in data if i.strip()]


def download_urls(urls):
    for url in urls:
        data = download_ref_links(url)
        print('%s refs downloaded. url: %s' % (
            len(data['links']), url))


def demo():
    list_file = os.path.join(CUR_DIR, 'url.list')
    urls = read_urls_from_file(list_file)
    download_urls(urls)


if __name__ == '__main__':
    demo()
