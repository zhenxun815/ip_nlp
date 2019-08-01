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
from os import path

from utils import clf_utils


def read_docs_file(file_path):
    cat_name = path.basename(file_path)[0:4]
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            print(line)
            seged_doc = json.loads(line)
            abs_ = seged_doc['abs']
            title = seged_doc['title']
            content = abs_ if len(abs_) > len(title) else title

            yield cat_name, content.replace('\n', '').replace('\t', '')


def save_group_file(base_dir):
    """
    将多个文件整合并存到3个文件中
    dirname: 原数据目录
    文件内容格式:  类别\t内容
    """
    train_dir = os.path.join(base_dir, 'train')
    train_txt = os.path.join(train_dir, 'train.txt')
    test_txt = os.path.join(train_dir, 'test.txt')
    val_txt = os.path.join(train_dir, 'val.txt')
    f_train = open(train_txt, 'a', encoding='utf-8')
    f_test = open(test_txt, 'a', encoding='utf-8')
    f_val = open(val_txt, 'a', encoding='utf-8')

    seged_dir = os.path.join(base_dir, 'seged')

    seq_size = 0

    for f_name in os.listdir(seged_dir):
        prefix_str = f_name.split('_')[0]
        print('prefix str is {}'.format(prefix_str))
        if not clf_utils.is_clf_str(prefix_str):
            continue
        count = 0
        clf_docs_file = os.path.join(seged_dir, f_name)
        for cat_name, content in read_docs_file(clf_docs_file):
            tmp_seq_size = content.count(' ')
            seq_size = tmp_seq_size if tmp_seq_size > seq_size else seq_size
            print('seq_size is {}'.format(seq_size))
            print('cat_name is {}, content is {}'.format(cat_name, content))
            line2write = '%s\t%s\n' % (cat_name, content)
            if count < 4000:
                f_train.write(line2write)
            elif count < 4400:
                f_val.write(line2write)
            else:
                f_test.write(line2write)
            count += 1

        print('Finished:', cat_name)

    f_train.flush()
    f_train.close()
    f_test.flush()
    f_test.close()
    f_val.flush()
    f_val.close()


if __name__ == '__main__':
    save_group_file('E:/ip_data')
