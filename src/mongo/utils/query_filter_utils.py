#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: query_filter_utils.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 8/6/2019 11:58


def get_clf_query_filter(kwargs):
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
    return query_filter
