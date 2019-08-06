#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common import logger_factory
# @Description:
# @File: clf_service.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/18/2019 12:01
from mongo.connect import get_collection
from mongo.utils.query_filter_utils import get_clf_query_filter

logger = logger_factory.get_logger('clf_service')


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
    logger.info(f'start count tasks {kwargs}')
    clc = get_collection(db_name, clc_name)

    query_filter = get_clf_query_filter(kwargs)
    count = clc.count_documents(query_filter)
    logger.info(f'count is {count}')
    return count


def get_clfs():
    clc = get_collection('ip_doc', 'raw')
