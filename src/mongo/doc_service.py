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
from mongo.connect import get_collection


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
        print(doc)
        obj_ids = doc['uniqueIds']
        print('obj ids is {}'.format(obj_ids))
        for i in range(len(obj_ids)):
            if i == len(obj_ids) - 1:
                break
            clc.remove(obj_ids[i])


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
    print('start search tasks {}'.format(kwargs))
    clc = get_collection(db_name, clc_name)

    query_filter = {}
    if 'section' in kwargs:
        query_filter['section'] = str(kwargs['section']).upper()
    else:
        print('section must not be null')
        return {}

    if 'mainClass' in kwargs:
        query_filter['mainClass'] = str(kwargs['mainClass']).upper()
    if 'subClass' in kwargs:
        query_filter['subClass'] = str(kwargs['subClass']).upper()

    cursor = clc.find(query_filter).limit(limit)
    print('search tasks {} complete'.format(kwargs))
    return cursor


if __name__ == '__main__':
    db_ip_doc = 'ip_doc'
    clc_raw = 'raw'
    # remove_redundant('ip_doc', 'raw')
    start_time = time.time()
    docs = find_by_clf(db_ip_doc, clc_raw, section='c', mainClass='08', subClass='b')
    # count = len(list(docs))
    # print('count is {}'.format(count))
    for doc in docs:
        print('find doc pubId {}'.format(doc['pubId']))

    end_time = time.time()
    print('complete...,take time {}s'.format(end_time - start_time))
