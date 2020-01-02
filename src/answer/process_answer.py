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

from answer.ClfInfo import ClfInfo
from utils import file_utils


def ans_score(my_ans_dir, right_ans_dir):
    que_count = 0
    right_answer_count = 0
    for ans_file_name in os.listdir(my_ans_dir):
        my_ans_file = os.path.join(my_ans_dir, ans_file_name)
        right_ans_file = os.path.join(right_ans_dir, ans_file_name)
        my_ans_dict = dict(file_utils.read_line(my_ans_file, lambda split: (split[0], split[1]), split=':'))
        right_ans_dict = dict(file_utils.read_line(right_ans_file, lambda split: (split[0], split[1]), split=':'))
        for _q, my_ans in my_ans_dict.items():
            right_ans = right_ans_dict[_q]
            print(f'{_q}, my:{my_ans}, right:{right_ans}')
            que_count += 1
            if my_ans == right_ans:
                right_answer_count += 1

    total_score = right_answer_count / que_count
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


def get_clf_info_dict(clf_count_info_file: str) -> list([dict]):
    """

    :type clf_count_info_file: str
    """
    info_list = file_utils.read_line(clf_count_info_file,
                                     lambda info: (info[0], ClfInfo(info[0], info[1])),
                                     ':')
    return dict(info_list)


def get_clf_que_info(ques_clf):
    ques_clf_count_dict = {}
    for clf in ques_clf:
        # print(f'clf is {clf}')
        if clf in ques_clf_count_dict.keys():
            count = ques_clf_count_dict.get(clf)
            # print(f'count is :{count}')
            ques_clf_count_dict.update({clf: count + 1})
        else:
            # print(f'add new clf')
            ques_clf_count_dict.update({clf: 1})
    # list_utils.print_dict(ques_clf_count_dict)

    return ques_clf_count_dict


if __name__ == '__main__':
    my_anss = 'E:/ip_data/classification/my_answers'
    right_anss = 'E:/ip_data/classification/right_answers'
    raw_answers_dir = 'E:/ip_data/classification/201904/pic'
    clf_file = 'F:/ip_data/ip_search/classification/clf_count.txt'
    # process_raw_answers(raw_answers_dir, right_anss)
    # right_ans_distribution(right_anss, clf_file)
    # ans_score(my_anss, right_anss)

    clf_infos = get_clf_info_dict(clf_file)
    # list_utils.print_dict(clf_infos, lambda clf_info: f'{clf_info.clf_count}')

    my_ans_dict = get_all_ans_dict(my_anss)
    right_ans_dict = get_all_ans_dict(right_anss)
    # for k,v in right_ans_dict:
    clf_que_info = get_clf_que_info(right_ans_dict.values())

    for clf_name, que_count in clf_que_info.items():
        clf_info = clf_infos.get(clf_name)
        clf_info.que_count = que_count
        clf_infos.update({clf_name: clf_info})
        info = clf_infos.get(clf_name)
        print(f'{info.clf_name},{info.clf_count},{info.que_count}')

    for que, right_ans in right_ans_dict.items():
        my_ans = my_ans_dict.get(que)
        clf_info = clf_infos.get(right_ans)
        if my_ans == right_ans:
            clf_info.right_que_count = clf_info.right_que_count + 1
            clf_infos.update({right_ans: clf_info})
            print(f'que{que}, right ans {right_ans},my ans {my_ans}')
            info = clf_infos.get(right_ans)
            print(f'{info.clf_name},{info.clf_count},{info.que_count},{info.right_que_count}')

    clf_need = set()
    for clf, clf_info in clf_infos.items():

        if clf_info.que_count > 0:
            score = clf_info.right_que_count / clf_info.que_count
            print(f'{clf_info.clf_name},score is {score}')
            if score < 0.5:
                clf_need.add(clf_info)
        # elif int(clf_info.clf_count) < 10000:
        # clf_need.add(clf_info)
    for info in clf_need:
        print(f'{info.clf_name}')
