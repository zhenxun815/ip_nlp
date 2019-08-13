#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: pre_data.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/31/2019 10:16

import json
import os
import re
from os import path
from random import choice


def read_enough(file_path):
    """
    read doc file with enough count
    :param file_path:
    :return:
    """
    clf_name = path.basename(file_path)[0:4]
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            content = gen_content_from_doc(line)
            if len(content) > 0:
                yield clf_name, content.replace('\n', '').replace('\t', '')


def read_less(file_path):
    """
    read doc count less than needed and return docs list with enough count
    :param file_path:
    :return:
    """
    all_contents = []
    train_contents = []
    val_contents = []
    test_contents = []
    clf_name = path.basename(file_path)[0:4]
    print(f'clf is {clf_name}')
    with open(file_path) as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            # print(f'index: {index}, count: {line}')
            content = gen_content_from_doc(line)
            if len(content) == 0:
                continue
            if index % 25 in range(20):
                train_contents.append(content)
            elif index % 25 in range(20, 23):
                val_contents.append(content)
            elif index % 25 in range(23, 25):
                test_contents.append(content)

    all_contents.extend(makeup_less(train_contents, 2000))
    all_contents.extend(makeup_less(val_contents, 300))
    all_contents.extend(makeup_less(test_contents, 200))
    print(f'length of train docs {len(train_contents)}')
    print(f'length of val docs {len(val_contents)}')
    print(f'length of test docs {len(test_contents)}')
    print(f'all contents length {len(all_contents)}')
    for content in all_contents:
        yield clf_name, content


def makeup_less(makeup_contents: list, target: int):
    """
    duplicate random docs to make up the difference
    :param all_contents:
    :param makeup_contents:
    :param target:
    :return:
    """
    while len(makeup_contents) < target:
        makeup_contents.append(choice(makeup_contents))

    return makeup_contents


def gen_content_from_doc(line):
    """
    parse line string to doc json, return text content from doc's abs or title on the basis of words count
    :param line:
    :return:
    """
    seged_doc = json.loads(line)
    abs_ = seged_doc['abs']
    title = seged_doc['title']
    content = abs_ if len(abs_) > len(title) else title
    content.replace('\n', '').replace('\t', '')
    return content


def parse_filename(filename):
    """
    parse file name such as 'A01B_99.txt', return a tuple as ('A01B', 99)
    :param filename:
    :return:
    """
    name_pattern = re.compile(r'(?P<clf_name>[A-Z][0-9]{2}[A-Z])_(?P<doc_count>[0-9]+)\.txt')
    matcher = name_pattern.match(filename)
    if matcher:
        clf_name = matcher.group('clf_name')
        doc_count = matcher.group('doc_count')
        return clf_name, int(doc_count)


def save_group_file(train_dir):
    """
    save doc to train.txt, val.txt and test.txt, if doc count less than 2500, replenish by some replicas
    :param train_dir:
    :return:
    """
    train_txt = os.path.join(train_dir, 'train.txt')
    val_txt = os.path.join(train_dir, 'val.txt')
    test_txt = os.path.join(train_dir, 'test.txt')
    clf_limit1300 = os.path.join(train_dir, 'clf_limit2500.txt')
    f_clf = open(clf_limit1300, 'a', encoding='utf-8')
    f_train = open(train_txt, 'a', encoding='utf-8')
    f_val = open(val_txt, 'a', encoding='utf-8')
    f_test = open(test_txt, 'a', encoding='utf-8')

    seged_dir = train_dir.replace('train', 'clfs/seged')

    for f_name in os.listdir(seged_dir):
        if f_name.find('old') > 0:
            continue

        clf_name, doc_count = parse_filename(f_name)

        clf_docs_file = os.path.join(seged_dir, f_name)
        if doc_count < 25:
            continue
        if doc_count < 2500:
            write_group(read_less(clf_docs_file), f_train, f_val, f_test)
        else:
            write_group(read_enough(clf_docs_file), f_train, f_val, f_test)
        f_clf.write(f'{clf_name}\n')
        print('Finished:', clf_name)

    f_clf.flush()
    f_clf.close()
    f_train.flush()
    f_train.close()
    f_val.flush()
    f_val.close()
    f_test.flush()
    f_test.close()


def write_group(contents, f_train, f_val, f_test):
    """
    write contents to specified files
    :param contents:
    :param f_test:
    :param f_train:
    :param f_val:
    :return:
    """

    count = 0
    for clf_name, content in contents:
        # print('cat_name is {}, content is {}'.format(clf_name, content))
        line2write = '%s\t%s\n' % (clf_name, content)
        if count < 2000:
            f_train.write(line2write)
        elif count < 2300:
            f_val.write(line2write)
        else:
            f_test.write(line2write)
        count += 1
    return clf_name


if __name__ == '__main__':
    save_group_file('E:/ip_data/train/limit2500')
