#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path

from common import logger_factory
from models.classification import Classification
from mongo import clf_service
# @Description:
# @File: clf_task.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/18/2019 10:02
from mongo import doc_service
from mongo.utils import json_encoder
from utils.clf_utils import gen_from_clf_str

logger = logger_factory.get_logger('clf_task')


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


def write_clf_docs(store_dir: str, clf: Classification, docs, file_suffix: str):
    """
    write ip docs json string to a local file line by line, the file was named
    in format like 'A_01_B_300.txt'. The number in file name is the count of docs
    stored in the file.
    :param store_dir:
    :param clf:
    :param docs: get from mongo, each item is a Bson obj
    :param file_suffix: file name suffix
    :return:
    """
    logger.info(f'start write tasks {clf} with suffix {file_suffix}')

    file_name = f'{clf}_{file_suffix}'
    file_path = path.join(store_dir, file_name)
    logger.info(f'tasks docs store file path is {file_path}')

    with open(file_path, 'a', encoding='utf-8') as f:
        for doc in docs:
            f.write(f'{json_encoder.doc2json(doc)}\n')


def write_clfs(clfs_info_file_path, store_dir_path, limit=0, write_less=True):
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
        if not write_less:
            count = clf_service.count_docs('ip_doc', 'raw',
                                           section=clf.section,
                                           mainClass=clf.main_class,
                                           subClass=clf.sub_class)

        logger.info(f'classification str is: {clf}, doc count: {count}')

        if write_less or count >= limit:
            clf_docs = doc_service.find_by_clf('ip_doc', 'raw', limit,
                                               section=clf.section,
                                               mainClass=clf.main_class,
                                               subClass=clf.sub_class)
            write_clf_docs(store_dir, clf, clf_docs, '5000.txt')
            logger.info(f'write clf {clf}')
            yield clf


if __name__ == '__main__':
    clf_names_file = '../../resources/clf_all.txt'
    store_dir = 'E:/ip_data/raw'
    written_clf_names_file = '../../resources/clfs_gt_5000.txt'
    clfs = write_clfs(clf_names_file, store_dir, limit=5000, write_less=False)
    with open(written_clf_names_file, 'w', encoding='utf-8') as f:
        for clf in clfs:
            f.write(str(clf) + '\n')
