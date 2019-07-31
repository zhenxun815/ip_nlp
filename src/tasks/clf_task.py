#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path

# @Description:
# @File: clf_task.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/18/2019 10:02
import mongo.doc_service as db_service
from models.classification import Classification
from mongo.utils import json_encoder
from utils.clf_utils import gen_from_clf_str


def get_clf_str_from_file(clf_names_file_path: str):
    """
    read classifications name string from file and return a generator whose
    item is a Classification obj
    :param clf_names_file_path:file path store classification infos
    :return:
    """
    with open(clf_names_file_path, encoding='utf-8') as f:
        for line in f.readlines():
            # print('read classification line str is {}'.format(line))
            yield gen_from_clf_str(line)


def write_clf_docs(store_dir: str, clf: Classification, docs: list):
    """
    write ip docs json string to a local file line by line, the file was named
    in format like 'A_01_B_300.txt'. The number in file name is the count of docs
    stored in the file.
    :param store_dir:
    :param clf:
    :param docs: get from mongo, each item is a Bson obj
    :return:
    """
    doc_count = len(docs)
    print('start write tasks {} with count {}'.format(clf, doc_count))

    file_name = '%s_%d.txt' % (clf, doc_count)
    file_path = path.join(store_dir, file_name)
    print('tasks docs store file path is {}'.format(file_path))

    json_docs = json_encoder.docs2jsons(docs)
    print('json docs count {}'.format(len(json_docs)))
    with open(file_path, 'a', encoding='utf-8') as f:
        for json in json_docs:
            f.write(json + '\n')


def write_clfs(clfs_info_file_path, store_dir_path, limit=300, write_less=True):
    """
    write docs of classifications in the classification info file to local file
    and yield the written Classification obj
    :param clfs_info_file_path:
    :param store_dir_path:
    :param limit: max count of docs to write
    :param write_less: whether write clf whose docs count less than limit or not
    :return:
    """
    classifications = get_clf_str_from_file(clfs_info_file_path)
    store_dir = store_dir_path
    for clf in classifications:
        print('classification str is: {}'.format(clf))
        clf_docs = db_service.find_cursor_by_clf('ip_doc', 'raw', limit, section=clf.section,
                                                 mainClass=clf.main_class,
                                                 subClass=clf.sub_class)
        docs2write = list(clf_docs)
        print('clf doc count {}'.format(len(docs2write)))
        if write_less or len(docs2write) == limit:
            write_clf_docs(store_dir, clf, docs2write)
            print('write clf {}'.format(clf))
            yield clf


if __name__ == '__main__':
    clf_names_file = '../../resources/clf_names.txt'
    store_dir = '../../resources/clfs/raw'
    written_clf_names_file = '../../resources/clfs_gt_5000.txt'
    clfs = write_clfs(clf_names_file, store_dir, limit=5000, write_less=False)
    with open(written_clf_names_file, 'w', encoding='utf-8') as f:
        for clf in clfs:
            f.write(str(clf) + '\n')
