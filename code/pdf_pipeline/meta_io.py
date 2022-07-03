import yaml
import os

from .utils import get_file_list

from .configs import (
    META_DIR,
    MISC_INFO_DIR,
)


def key2meta_path(key):
    return os.path.join(META_DIR, '%s.yaml' % key)


def filepath2key(filepath):
    basename = os.path.basename(filepath)
    raw_filename, ext = os.path.splitext(basename)

    return raw_filename


def read_meta(meta_key):
    meta_path = key2meta_path(meta_key)
    with open(meta_path, 'r') as f:
        meta = yaml.safe_load(f)
    return meta


def read_misc_info(filename):
    meta_path = os.path.join(MISC_INFO_DIR, filename)
    if not os.path.exists(meta_path):
        return {}

    with open(meta_path, 'r') as f:
        meta = yaml.safe_load(f)
    return meta


def save_meta(meta_key, content):
    meta_path = key2meta_path(meta_key)
    with open(meta_path, 'w') as fw:
        yaml.dump(content, fw)


def save_misc_info(filename, content):
    if not os.path.exists(MISC_INFO_DIR):
        os.makedirs(MISC_INFO_DIR)
    meta_path = os.path.join(MISC_INFO_DIR, filename)
    with open(meta_path, 'w') as fw:
        yaml.dump(content, fw)


def remove(meta_key):
    meta_path = key2meta_path(meta_key)
    os.remove(meta_path)


def update_meta(meta_key, content):
    meta_path = key2meta_path(meta_key)
    if os.path.exists(meta_path):
        meta = read_meta(meta_key)
    else:
        meta = {}

    meta.update(content)
    save_meta(meta_key, meta)


def get_meta_list(meta_root=META_DIR, sort_by_name=True):
    meta_files = get_file_list(meta_root, '.yaml')
    if sort_by_name:
        meta_files = sorted(meta_files)

    data = []
    for meta_path in meta_files:
        with open(meta_path, 'r') as f:
            meta = yaml.safe_load(f)
            data.append(meta)

    return data
