from configs import (
    REFERENCE_INFO_DIR,
)
from lib_cache import jcache
import logging
import requests
import json
import os

logger = logging.getLogger(__name__)


@jcache
def send_request(url):
    print('xxxxxx')
    response = requests.get(
        url=url,
        headers={
            "Accept": "text/html",
            "Accept-Language": "zh,zh-CN;en-US;",
            "Dnt": "1",
            "Referer": "https://www.google.com.hk/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "Accept-Encoding": "gzip",
            "Cookie": "s2Hist=2022-06-26T00%3A00%3A00.000Z%7C1; tid=rBIABmK3zsyfvgAIDNZrAg==; s2Exp=pdp_promo_banner_multi_arm_v2%3D-control%26external_content_display%3D-hidden%26abstract_highlighter_v2%3D-highlighted_abstract_default_toggle_off%26alerts_two_types_relevance_v2%3Drelevance_author%26new_ab_framework_aa%3Dcontrol%26new_ab_framework_mock_ab%3Dcontrol",
        },
    )
    return response.text


@jcache
def send_refs(pid, offset, referer):
    response = requests.get(
        url="https://www.semanticscholar.org/api/1/paper/%s/citations" % pid,
        params={
            "sort": "relevance",
            "offset": "%s" % offset,
            "citationType": "citedPapers",
            "citationsPageSize": "10",
        },
        headers={
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Dnt": "1",
            "Referer": referer,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "Accept-Encoding": "gzip",
        },
    )
    return response.json()


def download_ref_links(page_url):

    links = []

    base_url = page_url.split('?', 1)[0]
    pid = base_url.split('/')[-1]

    meta_info = send_refs(pid, 0, page_url)
    links.extend(meta_info.pop('citations'))
    total_links = meta_info['totalCitations']

    for i in range(10, total_links, 10):
        ret = send_refs(pid, i, page_url)
        links.extend(ret['citations'])

    data = {
        'links': links,
        'meta_info': meta_info,
        'page_url': page_url,
    }

    if not os.path.exists(REFERENCE_INFO_DIR):
        os.makedirs(REFERENCE_INFO_DIR)

    fpath = os.path.join(REFERENCE_INFO_DIR, 'ref-info-%s.json' % pid)

    with open(fpath, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)

    return data
