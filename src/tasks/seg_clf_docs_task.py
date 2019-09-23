#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: seg_clf_docs_task.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/30/2019 11:17

import json
import os
from multiprocessing import Pool, cpu_count
from os import path

from segmenter import segment
from utils import file_utils

NUMBER_OF_PROCESSES = cpu_count()


def seg_clf_file(clf_file_pair):
    raw_clf_file, seged_clf_file = clf_file_pair
    print(f'seg file {raw_clf_file} to {seged_clf_file}')
    seged_lines = file_utils.read_line(raw_clf_file, lambda line: segment.seg_raw_doc(json.loads(line)))
    file_utils.save_list2file(seged_lines, seged_clf_file, lambda doc_json: json.dumps(doc_json, ensure_ascii=False))


def seg_docs_under_dir(raw_files_dir, seged_files_dir):
    file_pairs = [(path.join(raw_files_dir, filename), path.join(seged_files_dir, filename)) for filename in
                  os.listdir(raw_files_dir)]
    print(f'file pairs {file_pairs}')
    pool = Pool(2)
    pool.map(seg_clf_file, file_pairs)
    pool.close()
    pool.join()


if __name__ == '__main__':
    raw_dir = 'E:/ip_data/clfs/raw/2500'
    seged_dir = 'E:/ip_data/clfs/new_seged/2500'
    print(f'core num {NUMBER_OF_PROCESSES}')
    seg_docs_under_dir(raw_dir, seged_dir)
