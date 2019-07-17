#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: classification_utils.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/17/2019 12:12
import re
from models.classification import Classification

# classification regex
_pattern = re.compile(r'(?P<section>[A-Z])(?P<main_class>[0-9]{2})(?P<sub_class>[A-Z])')


def gen_from_clf_str(clf_str: str) -> Classification:
    """
    get a Classification obj from original classification string, e.g.: H03H
    :param clf_str:
    :return:
    """
    matcher = _pattern.match(clf_str)
    if matcher:
        section = matcher.group('section')
        main_class = matcher.group('main_class')
        sub_class = matcher.group('sub_class')
        # print('section {}, mainClass {}, subClass {}'.format(section, main_class, sub_class))
        return Classification(section, main_class, sub_class)
    print('{} not match classification string pattern'.format(clf_str))
    return None


if __name__ == '__main__':
    gen_from_clf_str('H04F')
