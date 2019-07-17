#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: segment.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/17/2019 10:58


import jieba
import mongo.service as db_service

from os import path
from models.classification import Classification
from utils.classification_utils import gen_from_clf_str
from mongo.utils import json_encoder


def get_clf_str(classification_file_path):
    with open(classification_file_path, encoding='utf-8') as f:
        for line in f.readlines():
            yield gen_from_clf_str(line)
        # print('read classification line str is {}'.format(line))


def test_jieba():
    seg_list_all = jieba.cut("小明硕士毕业于中国科学院计算所，后在日本京都大学深造", cut_all=True)  # 全模式
    seg_list_accuracy = jieba.cut("小明硕士毕业于中国科学院计算所，后在日本京都大学深造", cut_all=False)  # 精确模式
    seg_list_search = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
    print('cut all result: ', ', '.join(seg_list_all))
    print('cut accuracy result', ', '.join(seg_list_accuracy))
    print('cut for search result: ', ', '.join(seg_list_search))


def write_clf_docs(store_dir: str, clf: Classification, docs: list):
    doc_count = len(docs)
    print('start write clf {} with count {}'.format(clf, doc_count))

    file_name = '%s_%d.txt' % (clf, doc_count)
    file_path = path.join(store_dir, file_name)
    print('clf docs store file path is {}'.format(file_path))

    json_docs = json_encoder.docs2jsons(docs)
    print('json docs count {}'.format(len(json_docs)))
    with open(file_path, 'a', encoding='utf-8') as f:
        for json in json_docs:
            f.write(json + '\n')
            # f.write(linesep)


if __name__ == '__main__':
    classifications = get_clf_str('../../resources/classifications.txt')
    store_dir = '../../resources/clfs/'
    for clf in classifications:
        print('classification str is: {}'.format(clf))
        clf_docs = db_service.find_by_classification('ip_doc', 'raw', section=clf.section,
                                                     mainClass=clf.main_class,
                                                     subClass=clf.sub_class)

        write_clf_docs(store_dir, clf, clf_docs)
