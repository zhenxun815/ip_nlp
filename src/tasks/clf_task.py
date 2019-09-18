#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description:
# @File: clf_task.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/18/2019 10:02

from os import path

from common import logger_factory
from models.classification import Classification
from mongo import clf_service
from mongo import doc_service
from mongo.utils import json_encoder
from utils import file_utils
from utils.clf_utils import gen_from_clf_str

logger = logger_factory.get_logger('clf_task')


def get_clf_str_from_file(clf_names_file_path: str):
    """
    read classifications name string from file and return a generator whose
    item is a Classification obj
    :param clf_names_file_path:file path store classification infos
    :return:
    """
    return file_utils.read_line(clf_names_file_path, lambda line: gen_from_clf_str(line))


def write_clf_docs(store_dir: str, clf: Classification, docs):
    """
    write ip docs json string to a local file line by line, the file was named
    in format like 'A_01_B_300.txt'. The number in file name is the count of docs
    stored in the file.
    :param store_dir:
    :param clf:
    :param docs: get from mongo, each item is a Bson obj
    :return:
    """
    doc_list = list(docs)
    file_suffix = f'{len(doc_list)}.txt'
    logger.info(f'start write tasks {clf} with suffix {file_suffix}')

    file_name = f'{clf}_{file_suffix}'
    file_path = path.join(store_dir, file_name)
    logger.info(f'tasks docs store file path is {file_path}')

    file_utils.save_list2file(doc_list, file_path, lambda doc: json_encoder.doc2json(doc))


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
            write_clf_docs(store_dir, clf, clf_docs)
            logger.info(f'write clf {clf}')
            yield clf


if __name__ == '__main__':
    clf_names_file = '/home/tqhy/ip_nlp/resources/clfs/clfs_all.txt'
    store_dir = '/home/tqhy/ip_nlp/resources/clfs/raw'
    written_clf_names_file = '/home/tqhy/ip_nlp/resources/clfs/clfs_limit_2500.txt'
    clfs = write_clfs(clf_names_file, store_dir, limit=2500, write_less=True)
    with open(written_clf_names_file, 'w', encoding='utf-8') as f:
        for clf in clfs:
            f.write(str(clf) + '\n')
