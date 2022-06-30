import os
import json
from .api import download_ref_links
from configs import (
    REFERENCE_INFO_DIR,
)

CUR_DIR = os.path.abspath(os.path.dirname(__file__))

url_ptn = 'https://www.semanticscholar.org/paper/%s/%s?sort=total-citations'


def append_url(urls, url):
    base_url = url.split('?', 1)[0]
    pid = base_url.split('/')[-1]

    outfile = os.path.join(REFERENCE_INFO_DIR, 'ref-info-%s.json' % pid)
    urls.append([pid, url, outfile])

    return urls


def read_urls_from_file(file_path):
    with open(file_path, 'r') as f:
        data = f.readlines()

    urls = []
    for url in data:
        append_url(urls, url)
    return urls


def read_urls_from_refs(dir_path):
    urls = []
    for file_path in os.listdir(dir_path):
        if not file_path.endswith('.json'):
            continue
        with open(os.path.join(dir_path, file_path), 'r') as f:
            data = json.load(f)
        for ref in data['links']:
            if 'id' not in ref or 'slug' not in ref:
                continue

            pid = ref['id']
            url = url_ptn % (ref['slug'], pid)
            outfile = os.path.join(REFERENCE_INFO_DIR, 'ref-info-%s.json' % pid)

            urls.append([pid, url, outfile])

    return urls


def download_urls(urls):

    if not os.path.exists(REFERENCE_INFO_DIR):
        os.makedirs(REFERENCE_INFO_DIR)

    ref_urls = []

    for idx, task in enumerate(urls):
        pid, url, outfile = task

        if os.path.exists(outfile):
            continue

        data = download_ref_links(pid, url, outfile)
        new_ref_links = data['links']
        ref_urls.extend(new_ref_links)
        print('(%s/%s)%s refs downloaded. url: %s' % (
            idx + 1, len(urls), len(new_ref_links), url))

    return ref_urls


def filter_valuable_urls(urls, min_count=5):
    # count occurence of each url
    url_count = {}
    for task in urls:
        if isinstance(task, str):
            url = task
        else:
            url = task[1]

        if url not in url_count:
            url_count[url] = 0
        url_count[url] += 1
    new_urls = []
    for url in url_count:
        if url_count[url] > min_count:
            append_url(new_urls, url)
    return new_urls


def demo():
    list_file = os.path.join(CUR_DIR, 'url.list')
    urls = read_urls_from_file(list_file)
    download_urls(urls)

    pre_count = 0

    while True:
        urls2 = read_urls_from_refs(REFERENCE_INFO_DIR)
        chosen_urls = filter_valuable_urls(urls2)

        cur_cnt = len(chosen_urls)
        if cur_cnt == pre_count:
            break

        pre_count = cur_cnt
        print("orig count: %s, chosen count: %s" % (len(urls2), len(chosen_urls)))
        download_urls(chosen_urls)


if __name__ == '__main__':
    demo()
