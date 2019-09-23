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
import random
import re
from os import path

from utils import file_utils


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

    all_contents.extend(makeup_less(train_contents, 8000))
    all_contents.extend(makeup_less(val_contents, 1000))
    all_contents.extend(makeup_less(test_contents, 1000))
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
        makeup_contents.append(random.choice(makeup_contents))

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
    clf_limit2500 = os.path.join(train_dir, 'clf_limit2500.txt')
    f_clf = open(clf_limit2500, 'a', encoding='utf-8')
    f_train = open(train_txt, 'a', encoding='utf-8')
    f_val = open(val_txt, 'a', encoding='utf-8')
    f_test = open(test_txt, 'a', encoding='utf-8')

    seged_dir = train_dir.replace('train', 'clfs/seged')

    for f_name in os.listdir(seged_dir):

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


def get_less_clf(seged_dir, count=10000):
    less_clf = []
    enough_clf = []
    for f_name in os.listdir(seged_dir):
        clf_name, doc_count = parse_filename(f_name)
        if doc_count < count:
            less_clf.append(clf_name)
        else:
            enough_clf.append(clf_name)
    return less_clf, enough_clf


def split_list(data_list: list, portion: tuple, shuffle=True):
    """

    :param data_list:
    :param portion: tuple
    :param shuffle:
    :return:
    """
    length = len(data_list)
    train_portion = portion[0]
    val_portion = portion[1]
    test_portion = portion[2]
    portion_total = train_portion + val_portion + test_portion
    if length < portion_total:
        print(f'not meet min size to split')
        return
    else:
        random.shuffle(data_list)
        split_index1 = int(length * train_portion / portion_total)
        split_index2 = int(length * val_portion / portion_total) + split_index1
        train_list = data_list[0:split_index1]
        val_list = data_list[split_index1:split_index2]
        test_list = data_list[split_index2:]
        return [train_list, val_list, test_list]


def concat_all(clf_dir, dest_dir, portion):
    file_names = ['train.txt', 'val.txt', 'test.txt']
    clf_name_file = os.path.join(dest_dir, 'clf_name.txt')
    clf_names = []
    for clf_file in os.listdir(clf_dir):
        clf_name = clf_file[0:4]
        clf_file_path = os.path.join(clf_dir, clf_file)
        texts = file_utils.read_line(clf_file_path, lambda line: json.loads(line)['abs'])
        splits = split_list(list(texts), portion)
        if splits:
            clf_names.append(clf_name)
            print(f'write clf {clf_name}')
            for index, list2write in enumerate(splits):
                dest_file = os.path.join(dest_dir, file_names[index])
                file_utils.save_list2file(list2write, dest_file, lambda text: f'{clf_name}\t{text}')
        else:
            print(f'not split')
    file_utils.save_list2file(clf_names, clf_name_file)


def create_copus(seged_clf_dir, copus_file):
    for seged_clf_file in os.listdir(seged_clf_dir):
        print(f'add clf {seged_clf_file}')
        file2read = os.path.join(seged_clf_dir, seged_clf_file)
        texts = file_utils.read_line(file2read, lambda line: json.loads(line)['abs'])
        file_utils.save_list2file(texts, copus_file, filter_func=lambda text: text and len(text) > 0, new_line=False)
    print(f'create copus complete')


def get_clf_info(dir):
    clf_dict = {}
    total_count = 0
    for fname in os.listdir(dir):
        clf_info = fname.split('.')[0]
        clf_name = clf_info.split('_')[0]
        clf_count = int(clf_info.split('_')[1])
        clf_dict[clf_name] = clf_count
        print(f'clf_info: {clf_info},clf_name: {clf_name}, clf_count: {clf_count}')
        total_count += clf_count

    return clf_dict, total_count


if __name__ == '__main__':
    # save_group_file('E:/ip_data/train/rnn')
    # concat_all('E:/ip_data/clfs/new_seged/limit10000', 'E:/ip_data/clfs/', (5, 2, 3))
    # create_copus('E:/ip_data/clfs/new_seged/no_limit','E:/ip_data/clfs/new_seged/no_limit_t/copus.txt')
    seged_dir = 'E:/ip_data/clfs/new_seged/no_limit'
    select_dir = 'E:/ip_data/clfs/new_seged/no_limit_t'
    clf_dict, total_count = get_clf_info(seged_dir)
    for clf_file in os.listdir(seged_dir):
        clf_name = clf_file[0:4]
        clf_count = clf_dict[clf_name]
        read_count = int(clf_count / total_count * 10000)
        if read_count > 20:
            file2read = os.path.join(seged_dir, clf_file)
            lines = list(file_utils.read_line(file2read))
            random.shuffle(lines)
            print(f'clf {clf_name}, clf count {clf_count}, write count {read_count}')
            save_file = f'{clf_name}_{read_count}.txt'
            file_utils.save_list2file(lines[0:read_count], os.path.join(select_dir, save_file))
