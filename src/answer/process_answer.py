#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
# @Description:
# @File: process_ans.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 9/12/2019 10:12
import os
from functools import reduce

from utils import file_utils


def ans_score(my_ans_dir, right_ans_dir):
    que_count = 0
    right_anser_count = 0
    for ans_file_name in os.listdir(my_ans_dir):
        my_ans_file = os.path.join(my_ans_dir, ans_file_name)
        right_ans_file = os.path.join(right_ans_dir, ans_file_name)
        my_ans_dict = dict(file_utils.read_line(my_ans_file, lambda split: (split[0], split[1]), split=':'))
        right_ans_dict = dict(file_utils.read_line(right_ans_file, lambda split: (split[0], split[1]), split=','))
        for _q, my_ans in my_ans_dict.items():
            right_ans = right_ans_dict[_q]
            print(f'{_q}, my:{my_ans}, right:{right_ans}')
            que_count += 1
            if my_ans == right_ans:
                right_anser_count += 1

    total_score = right_anser_count / que_count
    print(f'total score is {total_score}')


def read_ans(ans_file):
    return file_utils.read_line(ans_file, lambda split: (split[0], split[1]), split=':')


def dict_ans(ans_dir):
    for ans_file in os.listdir(ans_dir):
        yield {que: ans for (que, ans) in read_ans(os.path.join(ans_dir, ans_file))}


def get_all_ans_dict(ans_dir):
    return reduce(lambda x, y: dict(x, **y), list(dict_ans(ans_dir)), {})


def right_ans_distribution(right_ans_dir, clf_count_file):
    clf_info_dict = dict(file_utils.read_line(clf_count_file, lambda split: (split[0], split[1]), split=':'))
    total_doc_count = 0
    total_que_count = 0
    for k, v in clf_info_dict.items():
        # print(f'clf info k: {k}, v: {v}')
        total_doc_count += int(v)

    clf_que_count_dict = {clf: 0 for clf, count in clf_info_dict.items()}
    all_que_dict = get_all_ans_dict(right_ans_dir)
    for k, v in all_que_dict.items():
        # print(f'all ans k {k},v {v}')
        total_que_count += 1
        clf_que_count_dict[v] += 1

    clf_que_count_dict = {k: int(v) * 100 / total_que_count for (k, v) in clf_que_count_dict.items()}
    clf_info_list = [(k, int(v) * 100 / total_doc_count) for (k, v) in clf_info_dict.items()]
    clf_info_list.sort(key=lambda ele: ele[1], reverse=True)
    print(f'total_que_count {total_que_count}, total_doc_count {total_doc_count}')

    for k, v in clf_info_list:
        doc_portion = '{0:.3f}%'.format(v)
        que_portion = '{0:.3f}%'.format(clf_que_count_dict.get(k))
        print(f'clf : {k}, doc portion {doc_portion}, que portion: {que_portion}')
        # print(f'clf : {k}, que portion: {v}, doc portion {clf_info_dict.get(k)}')


def process_raw_answer(raw_answer_file):
    with open(raw_answer_file, encoding='utf-8') as f:
        raw_answer_pairs = json.loads(f.readline())
        for pub_id, clf_str in raw_answer_pairs.items():
            yield f"{pub_id}:{clf_str[0:4]}"


def process_raw_answers(raw_answers_dir, processed_answer_dir):
    for raw_answer in os.listdir(raw_answers_dir):
        raw_answer_file = os.path.join(raw_answers_dir, raw_answer)
        processed_answers = process_raw_answer(raw_answer_file)
        store_answer_file = os.path.join(processed_answer_dir, raw_answer)
        file_utils.save_list2file(processed_answers, store_answer_file)


if __name__ == '__main__':
    my_anss = 'C:/Users/qing/Desktop/自动分类号单1-20190903/my_answers'
    right_anss = 'C:/Users/qing/Desktop/自动分类号单1-20190903/right_answers'
    raw_answers_dir = 'C:/Users/qing/Desktop/自动分类号单1-20190903/20190903/pic'
    clf_file = 'F:/ip_data/ip_search/classification/clf_count.txt'
    # process_raw_answers(raw_answers_dir, right_anss)
    right_ans_distribution(right_anss, clf_file)
    # ans_score(my_anss, right_anss)
