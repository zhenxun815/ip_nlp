#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description:
# @File: collect_new.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 1/2/2020 11:18
import os
import shutil
from collections import Counter

from utils import file_utils


def verify(word: str):
    word_len = len(word)
    if word_len % 2 == 0:
        half_word = word[0:int(word_len / 2)]
        return half_word if word.count(half_word) == 2 else word
    return word


def collect_new_dict(dict_dir: str, dest_dict_file: str):
    new_dict_files = file_utils.get_files(dict_dir)
    word_counter = Counter([verify(word) for dict_file in new_dict_files for word in file_utils.read_line(dict_file)])
    # list_utils.print_list(word_counter.keys())
    file_utils.save_list2file(word_counter.keys(), dest_dict_file)


if __name__ == '__main__':
    # collect('E:/dict/new_words','E:/dict/new_words.txt')
    # file_utils.remove_redundant('E:/dict/new_words.txt','E:/dict/new_words2.txt')
    clf_names_file_path = '/home/tqhy/ip_nlp/resources/clfs/class_needed.txt'
    clf_raw_dir = '/home/tqhy/ip_nlp/resources/clfs/raw/no_limit'
    lower_score_dir = '/home/tqhy/ip_nlp/resources/clfs/raw/lower_score'

    clf_to_collect = list(file_utils.read_line(clf_names_file_path))
    for file_names in os.listdir(clf_raw_dir):
        if file_names[0:4] in clf_to_collect:
            src_file = os.path.join(clf_raw_dir, file_names)
            dest_file = os.path.join(lower_score_dir, file_names)
            shutil.copyfile(src_file, dest_file)
