#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: clf_service.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/18/2019 12:01
from mongo.connect import get_collection


def count_docs(db_name: str, clc_name: str, **kwargs):
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
    print('start count tasks {}'.format(kwargs))
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

    count = clc.count_documents(query_filter)
    print('count is {}'.format(count))
    return count


def get_clfs():
    clc = get_collection('ip_doc', 'raw')
