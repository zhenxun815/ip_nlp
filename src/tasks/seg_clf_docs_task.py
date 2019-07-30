#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: seg_clf_docs_task.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/30/2019 11:17

import json
from os import path

from segmenter import segment
from utils import file_utils


def seg_docs_under_dir(dir_path, file_name_regx):
    files2reg = file_utils.get_files(dir_path, file_name_regx)
    print(files2reg)
    stop_words = segment.load_stop_words('../../resources/stps/stopWord.txt')
    for file in files2reg:
        with open(file) as f:
            for line in f:
                clf_json = json.loads(line)
                seged_doc = segment.seg_raw_doc(clf_json, stop_words)
                yield path.basename(file), seged_doc


if __name__ == '__main__':
    regx = r'[A-Z][0-9]{2}[A-Z]_5000.txt'
    raw_dir_path = '../../resources/clfs/raw'
    seged_dir_path = '../../resources/clfs/seged'
    seg_tup = seg_docs_under_dir(raw_dir_path, regx)

    for file_name, doc in seg_tup:
        print('file is {},seged doc is {}'.format(file_name, doc['pubId']))
        seged_file = path.join(seged_dir_path, file_name)
        with open(seged_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')
