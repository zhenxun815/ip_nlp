#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: file_utils.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/22/2019 9:28
import os
import re


def save_list2file(list2write, dest_file: str):
    """
    write list elements to file line by line
    :param list2write:
    :param dest_file
    :return:
    """
    with open(dest_file, 'a', encoding='utf-8') as f:
        for item in list2write:
            print('item to write {}'.format(item))
            f.write(str(item) + '\n')
            # f.flush()


def get_files(dir_path, name_regx=None):
    """
    get files whose name match specified name patten under a dir, if file name
    patten is no specified, then return all files name
    :param dir_path:
    :param name_regx:
    :return:
    """
    if os.path.isdir(dir_path):
        files = os.listdir(dir_path)
        if name_regx:
            _pattern = re.compile(name_regx)
            return [os.path.join(dir_path, file) for file in files if _pattern.match(file)]
        return [os.path.join(dir_path, file) for file in files]
    else:
        raise Exception('% is not a dir' % dir_path)
