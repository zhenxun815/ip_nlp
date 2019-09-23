#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
# @Description:
# @File: process_question.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 8/9/2019 17:32
import os

from segmenter import segment


def seg_raw_txts(raw_txts_dir, seged_txts_dir):
    for txt_name in os.listdir(raw_txts_dir):
        seged_result = seg_raw_docs(os.path.join(raw_txts_dir, txt_name))
        seged_txt = os.path.join(seged_txts_dir, txt_name)
        store_seged_txts(seged_txt, seged_result)


def seg_raw_docs(question_file_path):
    with open(question_file_path) as f:
        line = f.readline()
        docs = json.loads(line)
        for doc_id, doc_content in docs.items():
            seged_ab = segment.seg_text(doc_content['ab'])
            # print(f'doc id {doc_id}, doc ab {seged_ab}')
            yield doc_id, seged_ab


def store_seged_txts(seged_txt, result):
    print(f'seged_txt is {seged_txt}')
    with open(seged_txt, 'a', encoding='utf-8') as f:
        for doc_id, seged_ab in result:
            line2write = f'{doc_id}\t {seged_ab} \n'
            f.write(line2write)





if __name__ == '__main__':

    raw_questions_dir = 'E:/ip_data/自动分类号单1-20190903/json'
    seged_question_dir = 'E:/ip_data/自动分类号单1-20190903/seged2'

    # seg_raw_txts(raw_questions_dir, seged_question_dir)
