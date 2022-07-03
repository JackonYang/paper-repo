from configs import (
    REFERENCE_INFO_DIR,
    REF_META_DIR,
)
import json
import os
import re
import yaml
import copy


CUR_DIR = os.path.abspath(os.path.dirname(__file__))

title_format_re = re.compile(r'[\W\s]+')


def clean_title_encoding(title):
    title = title.replace('–', '-')
    title = title.replace('—', '-')
    title = title.replace('’', '\'')
    return title


def init_paper_dict(dirpath):
    paper_info = {}
    for file_path in os.listdir(dirpath):
        if not file_path.endswith('.json'):
            continue

        pid = file_path.split('-')[-1].split('.')[0]
        with open(os.path.join(REFERENCE_INFO_DIR, file_path), 'r') as f:
            data = json.load(f)

        paper_info[pid] = data

    return paper_info


def save_yaml(paper_info, dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    for pid, info in paper_info.items():
        with open(os.path.join(dirpath, '%s.yaml' % pid), 'w') as f:
            yaml.safe_dump(info, f)


def clean_ref(old_ref):
    if isinstance(old_ref, str):
        return old_ref

    if 'fragments' in old_ref:
        return old_ref['text']

    if isinstance(old_ref, dict):
        return clean_dict(old_ref)

    if isinstance(old_ref, list):
        return [clean_ref(x) for x in old_ref]

    print("error. unknown: %s" % old_ref)


def clean_dict(old_ref):

    ref = copy.deepcopy(old_ref)
    for k, v in ref.items():
        if k == 'authors':
            ref[k] = [i[-1]['text'] for i in v]
        elif isinstance(v, dict) and 'fragments' in v:
            ref[k] = v['text']
        elif isinstance(v, list):
            ref[k] = [clean_ref(x) for x in v]
        else:
            ref[k] = v

    return ref


ref_cnt_thre = [
    (2015, 100),
    (2010, 1000),
    (2000, 3000),
    (1990, 10000),
    (1950, 30000),
]


def is_drop_by_cited_cnt(cited_cnt, year):
    for y, thre in ref_cnt_thre:
        if year > y:
            return cited_cnt < thre

    return True


def is_drop_by_title(title, meta_key, cited_cnt):
    if len(meta_key) < 10:
        # print(title)
        return True

    if not meta_key.isascii():
        # print(cited_cnt, title, meta_key, meta_key.isascii())
        return True

    return False


def title2meta_key(title):
    return title_format_re.sub('-', title.lower()).strip(' -')


def add_info_by_ref(ref_info, new_info):
    ignore_fields = [
        'isKey',
        'citationContexts',
        'tldr',
    ]

    for k, v in ref_info.items():
        if k in ignore_fields:
            continue
        new_info[k] = v


def get_info_from_raw(data):
    if 'meta_info' not in data:
        print(data)
        return

    if data['meta_info'].get('responseType') == 'CANONICAL':
        return

    if 'totalCitations' in data['meta_info']:
        ref_cnt = data['meta_info']['totalCitations']
    else:
        print('no totalCitations: %s' % data)
        ref_cnt = -1

    if 'page_url' not in data:
        print('no page_url: %s' % data)
        url = ''
    else:
        url = data['page_url']

    return {
        'url': url,
        'ref_count': ref_cnt,
    }


def main():
    raw_paper_info = init_paper_dict(REFERENCE_INFO_DIR)
    paper_info = {}
    paper_ref_map = {}

    # year_info = []

    for cur_pid, data in raw_paper_info.items():

        if 'page_url' not in data:
            continue

        paper_ref_map[cur_pid] = []
        paper_refs = paper_ref_map[cur_pid]
        # update info 2
        for ref in data['links']:
            if 'id' not in ref:
                continue
            pid = ref.pop('id')
            cited_cnt = ref.get('numCitedBy', -1)
            year = ref.get('year', -1)

            show_ref_link = (
                pid in raw_paper_info and not is_drop_by_cited_cnt(cited_cnt, year)
            )

            ref = clean_ref(ref)
            ref['title'] = clean_title_encoding(ref['title'])
            ref['meta_key'] = title2meta_key(ref['title'])

            if show_ref_link and is_drop_by_title(ref['title'], ref['meta_key'], cited_cnt):
                show_ref_link = False

            if show_ref_link and pid not in paper_info:
                # year_info.append([year, cited_cnt, ref['title']])
                new_info = get_info_from_raw(raw_paper_info[pid])
                if new_info:
                    paper_info[pid] = new_info
                    add_info_by_ref(ref, paper_info[pid])

            paper_refs.append({
                'pid': pid,
                'title': ref['title'],
                'show_ref_link': show_ref_link,
                'numCitedBy': ref.get('numCitedBy', -1),
                'fieldsOfStudy': ref.get('fieldsOfStudy', []),
                'year': ref.get('year', -1),
                'meta_key': ref['meta_key'],
            })

    for pid, info in paper_info.items():
        info['references'] = paper_ref_map[pid]

    print('final paper cnt: %s, raw paper cnt: %s' % (
        len(paper_info), len(raw_paper_info)))
    # with open('year-info.txt', 'w') as fw:
    #     for raw in sorted(year_info, reverse=True):
    #         fw.write('%4d, %s, %s\n' % tuple(raw))
    save_yaml(paper_info, REF_META_DIR)


if __name__ == '__main__':
    main()
