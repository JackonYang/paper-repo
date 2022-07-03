import os
import yaml
import json
from turtle import title

from configs import (
    REFERENCE_INFO_DIR,
    REF_META_DIR,
)

CUR_DIR = os.path.abspath(os.path.dirname(__file__))


def init_paper_dict(dirpath):
    paper_info = {}
    for file_path in os.listdir(dirpath):
        if not file_path.endswith('.json'):
            continue

        pid = file_path.split('-')[-1].split('.')[0]
        paper_info[pid] = {}

    return paper_info


def save_yaml(paper_info, paper_cnt, dirpath):
    # for pid, cnt in paper_cnt.items():
    #     if cnt < 2:
    #         print(pid)
    #         print(paper_info[pid])

    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    for pid, info in paper_info.items():
        with open(os.path.join(dirpath, '%s.yaml' % pid), 'w') as f:
            yaml.safe_dump(info, f)


def main():
    paper_info = init_paper_dict(REFERENCE_INFO_DIR)

    paper_cnt = {p: 0 for p in paper_info}

    for file_path in os.listdir(REFERENCE_INFO_DIR):
        if not file_path.endswith('.json'):
            continue

        cur_pid = file_path.split('-')[-1].split('.')[0]
        with open(os.path.join(REFERENCE_INFO_DIR, file_path), 'r') as f:
            data = json.load(f)

            if 'page_url' not in data:
                continue

            # update info 1
            paper_info[cur_pid].update({
                'url': data['page_url'],
                'ref_count': data['meta_info']['totalCitations'],
            })

            paper_refs = []
            # update info 2
            for ref in data['links']:
                if 'id' not in ref:
                    continue
                pid = ref['id']
                if pid in paper_info:
                    paper_cnt[pid] += 1
                    # if paper_cnt[pid] > 1:
                    #    continue

                    pid = ref.pop('id')
                    paper_refs.append({
                        'pid': pid,
                        'title': ref['title'],
                    })
                    ref.pop('isKey')
                    if 'citationContexts' in ref:
                        ref.pop('citationContexts')
                    if 'tldr' in ref:
                        ref.pop('tldr')

                    for k, v in ref.items():
                        if isinstance(v, dict) and 'fragments' in v:
                            ref[k] = v['text']

                    paper_info[pid].update(ref)
            paper_info[cur_pid]['references'] = paper_refs

    save_yaml(paper_info, paper_cnt, REF_META_DIR)


if __name__ == '__main__':
    main()
