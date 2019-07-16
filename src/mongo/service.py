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
from pymongo import MongoClient


def get_db(db_name):
    """
    connect to mongo and get the param specified db obj
    :param db_name: the db's name
    :return:
    """
    client = MongoClient(host='192.168.1.205', port=27017, username='tqhy', password='tqhy817')
    return client.get_database(db_name)  # same with: client[db_name]


def create_index(db_name, clc_name, field_name, sort=ASCENDING):
    """
    create index of doc field to specified db's collection
    :param db_name:
    :param clc_name:
    :param field_name:
    :param sort: default direction is asc
    :return:
    """
    db = get_db(db_name)
    clc = db.get_collection(clc_name)
    clc.create_index([(field_name, sort)], background=True)


def remove_redundant(db_name, clc_name):
    """
    remove redundant docs
    :param db_name:
    :param clc_name:
    :return:
    """
    db = get_db(db_name)
    clc = db.get_collection(clc_name)

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


def find_by_classification(db_name, clc_name, limit=300, **kwargs):
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
    db = get_db(db_name)
    clc = db.get_collection(clc_name)

    query_filter = {}
    if 'section' in kwargs:
        query_filter['section'] = kwargs['section']
    else:
        print('section must not be null')
        return

    if 'mainClass' in kwargs:
        query_filter['mainClass'] = kwargs['mainClass']
    if 'subClass' in kwargs:
        query_filter['subClass'] = kwargs['subClass']

    cursor = clc.find(query_filter).limit(limit)

    for doc in cursor:
        print(doc)


def count_by_classification(db_name, clc_name, **kwargs):
    """
    get doc count of specified classification
    :param db_name:
    :param clc_name:
    :param kwargs:
                section required
                mainClass
                subClass
    :return: int, if query section is null, return 0
    """
    print('query param is {}'.format(kwargs))
    db = get_db(db_name)
    clc = db.get_collection(clc_name)

    query_filter = {}
    if 'section' in kwargs:
        query_filter['section'] = kwargs['section']
    else:
        print('section must not be null')
        return 0

    if 'mainClass' in kwargs:
        query_filter['mainClass'] = kwargs['mainClass']
    if 'subClass' in kwargs:
        query_filter['subClass'] = kwargs['subClass']

    count = clc.count_documents(query_filter)
    print('count is {}'.format(count))
    return count


if __name__ == '__main__':
    db_ip_doc = 'ip_doc'
    clc_raw = 'raw'
    # remove_redundant('ip_doc', 'raw')
    start_time = time.time()
    # find_by_classification(db_ip_doc, clc_raw, 300, section='C', mainClass='08', subClass='B')
    count_by_classification(db_ip_doc, clc_raw, section='C', mainClass='08', subClass='B')
    end_time = time.time()
    print('complete...,take time {}s'.format(end_time - start_time))
