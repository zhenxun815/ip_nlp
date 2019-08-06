#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description:
# @File: test.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/15/2019 10:30
import time

from pymongo import ASCENDING

from common import logger_factory
from mongo.connect import get_collection
from mongo.utils.query_filter_utils import get_clf_query_filter

logger = logger_factory.get_logger('doc_service')


def create_index(db_name, clc_name, field_name, sort=ASCENDING):
    """
    create index of doc field to specified db's collection
    :param db_name:
    :param clc_name:
    :param field_name:
    :param sort: default direction is asc
    :return:
    """

    clc = get_collection(db_name, clc_name)
    clc.create_index([(field_name, sort)], background=True)


def remove_redundant(db_name, clc_name):
    """
    remove redundant docs
    :param db_name:
    :param clc_name:
    :return:
    """
    clc = get_collection(db_name, clc_name)

    redundant_docs = clc.aggregate([
            {'$group': {
                    '_id':       {'pubId': '$pubId'},
                    'uniqueIds': {'$addToSet': '$_id'},
                    'count':     {'$sum': 1}
            }},
            {'$match': {
                    'count': {'$gt': 1}
            }}], allowDiskUse=True)
    print('redundant_docs {}'.format(type(redundant_docs)))
    for doc in redundant_docs:
        logger.info(f'{doc}')
        obj_ids = doc['uniqueIds']
        logger.info(f'obj ids is {obj_ids}')
        for i in range(len(obj_ids)):
            if i == len(obj_ids) - 1:
                break
            clc.remove(obj_ids[i])


def find_some(db_name: str, clc_name: str, limit: int):
    """
    find specified count of docs return a generator, whose item is a Bson obj
    :param db_name:
    :param clc_name:
    :param limit:
    :return:
    """
    logger.info(f'start find_some with limit {limit}')
    clc = get_collection(db_name, clc_name)
    limit = 0 if limit < 0 else limit
    cursor = clc.find({}).limit(limit)
    while cursor.alive:
        yield cursor.next()


def find_all(db_name: str, clc_name: str):
    """
    find all docs and return a generator, whose item is a Bson obj
    :param db_name:
    :param clc_name:
    :return:
    """
    logger.info('start find_all')
    return find_some(db_name, clc_name, 0)


def find_by_clf(db_name, clc_name, limit=300, **kwargs):
    """
    find docs by classification infos and return a generator, whose item is a Bson obj
    :param db_name:
    :param clc_name:
    :param limit:
    :param kwargs:
    :return:
    """
    cursor = find_cursor_by_clf(db_name, clc_name, limit, **kwargs)
    while cursor.alive:
        yield cursor.next()


def find_cursor_by_clf(db_name, clc_name, limit, **kwargs):
    """
    get docs obj by classification params
    :param db_name:
    :param clc_name:
    :param limit:
    :param kwargs:
                section required
                mainClass
                subClass
    :return:
    """
    logger.info(f'start search tasks with {kwargs}')
    clc = get_collection(db_name, clc_name)

    query_filter = get_clf_query_filter(kwargs)

    cursor = clc.find(query_filter).limit(limit)
    logger.info(f'search tasks {kwargs} complete')
    return cursor


if __name__ == '__main__':
    db_ip_doc = 'ip_doc'
    clc_raw = 'raw'
    # remove_redundant('ip_doc', 'raw')
    start_time = time.time()
    docs = find_some(db_ip_doc, clc_raw, 3)
    # count = len(list(docs))
    # print('count is {}'.format(count))
    for doc in docs:
        logger.info(f'find doc pubId {doc["pubId"]}')

    end_time = time.time()
    logger.info(f'complete...,take time {end_time - start_time}s')
