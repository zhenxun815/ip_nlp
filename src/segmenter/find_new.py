#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools
# @Description:
# @File: find_new.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 9/25/2019 11:28
import os
import re
from multiprocessing import Pool

from segmenter.dict_utils import load_dictionary, generate_ngram, save_model, load_model
from segmenter.trie_model import TrieNode
from utils import file_utils

chinese_pattern = re.compile(r'[\u4E00-\u9FFF]+')
"""
basedir = 'E:/dict'
abs_dir = 'E:/dict/abs'
new_words_dir = 'E:/dict/nwd'
"""
basedir = '/home/tqhy/ip_nlp/resources/custom_dict'
abs_dir = '/home/tqhy/ip_nlp/resources/clfs/abs/seged'
new_words_dir = '/home/tqhy/ip_nlp/resources/custom_dict/new_words'

root_name = basedir + "/root.pkl"


def is_chinese(words: str, stp_words):
    result = chinese_pattern.match(words) and words not in stp_words
    print(f'words is {words}, result is {result}')
    return result


def load_data(filename):
    """
    :param filename:
    :return: 二维数组,[[句子1分词list], [句子2分词list],...,[句子n分词list]]
    """
    data = []
    count = 0
    with open(filename, 'r') as f:
        for line in f:
            if count == 800:
                break
            word_list = line.split()[0:200]
            data.append(word_list)
            count += 1
    return data


def load_data_2_root(data, model):
    print('------> 插入节点')
    for word_list in data:
        # print(f'start gen ngram: {word_list}')
        ngrams = generate_ngram(word_list, 3)
        for d in ngrams:
            model.add(d)
    print('------> 插入成功')


def find_new_words(root, file_pair):
    abs_file, new_words_file = file_pair[0], file_pair[1]
    if os.path.exists(new_words_file):
        print(f'clf {new_words_file} has already found new words ...')
        return
    print(f'start find new word in {abs_file}')
    datas = load_data(abs_file)
    model = root
    topN = 2
    if len(datas) > 0:
        tmp = []
        count = 0
        words2add = set()
        for item in datas:
            tmp.append(item)
            count += 1
            if count % 40 == 0:
                load_data_2_root(tmp, model)
                result, add_word = model.find_word(topN)
                words2add.update(add_word.keys())
                print(f'words2add: {words2add}, {count}')
                tmp.clear()
        if len(tmp) > 0:
            print(f'{words2add}')
            load_data_2_root(tmp, model)
            result, add_word = model.find_word(topN)
            words2add.update(add_word.keys())
            print(f'words2add: {words2add}, {count}')
            tmp.clear()
        file_utils.save_list2file(words2add, new_words_file)


if __name__ == "__main__":

    if os.path.exists(root_name):
        root = load_model(root_name)
    else:
        dict_name = basedir + '/dict.txt'
        word_freq = load_dictionary(dict_name)
        root = TrieNode('*', word_freq)
        save_model(root, root_name)

    file_pairs = [(os.path.join(abs_dir, fname), os.path.join(new_words_dir, fname)) for fname in
                  os.listdir(abs_dir)]
    find_func = functools.partial(find_new_words, root)
    pool = Pool(40)
    pool.map(find_func, file_pairs)
    pool.close()
    pool.join()
