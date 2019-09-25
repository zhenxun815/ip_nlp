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
from multiprocessing import Pool, cpu_count

import jieba

from segmenter.dict_utils import load_dictionary, generate_ngram, save_model, load_model
from segmenter.trie_model import TrieNode
from utils import file_utils

chinese_pattern = re.compile(r'[\u4E00-\u9FFF]+')

basedir = 'E:/dict'
abs_dir = 'E:/dict/abs'
new_words_dir = 'E:/dict/nwd'
"""
basedir = '/home/tqhy/ip_nlp/resources/custom_dict'
abs_dir = '/home/tqhy/ip_nlp/resources/clfs/abs/no_limit'
new_words_dir = '/home/tqhy/ip_nlp/resources/custom_dict/new_words'
"""
root_name = basedir + "/root.pkl"


def is_chinese(words: str, stp_words):
    result = chinese_pattern.match(words) and words not in stp_words
    print(f'words is {words}, result is {result}')
    return result


def load_data(filename, stp_words):
    """
    :param filename:
    :param stopwords:
    :return: 二维数组,[[句子1分词list], [句子2分词list],...,[句子n分词list]]
    """
    data = []
    with open(filename, 'r') as f:
        for line in f:
            word_list = [x for x in jieba.cut(line.strip(), cut_all=False) if is_chinese(x, stp_words)]
            data.append(word_list)
    return data


def load_data_2_root(data, model):
    print('------> 插入节点')
    for word_list in data:
        # tmp 表示每一行自由组合后的结果（n gram）
        # tmp: [['它'], ['是'], ['小'], ['狗'], ['它', '是'], ['是', '小'], ['小', '狗'], ['它', '是', '小'], ['是', '小', '狗']]
        ngrams = generate_ngram(word_list, 3)
        for d in ngrams:
            model.add(d)
    print('------> 插入成功')


def find_new_words(root, stp_words, file_pair):
    abs_file, new_words_file = file_pair[0], file_pair[1]
    print(f'start find new word in {abs_file}')
    datas = load_data(abs_file, stp_words)
    model = root
    if len(datas) > 0:
        load_data_2_root(datas, model)
        topN = 10
        result, add_word = model.find_word(topN)
        file_utils.save_dict2file(add_word, new_words_file, work=lambda k, v: (k, ''), split='')


if __name__ == "__main__":

    stp_words = file_utils.read_line(basedir + '/stp_words.txt')

    if os.path.exists(root_name):
        root = load_model(root_name)
    else:
        dict_name = basedir + '/dict.txt'
        word_freq = load_dictionary(dict_name)
        root = TrieNode('*', word_freq)
        save_model(root, root_name)

    file_pairs = [(os.path.join(abs_dir, fname), os.path.join(new_words_dir, fname)) for fname in
                  os.listdir(abs_dir)]
    find_func = functools.partial(find_new_words, root, list(stp_words))
    pool = Pool(int(cpu_count() / 2))
    pool.map(find_func, file_pairs)
    pool.close()
    pool.join()
