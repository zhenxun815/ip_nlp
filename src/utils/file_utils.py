#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: file_utils.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/22/2019 9:28


def list2file(list2write: list, dest_file: str):
    """
    write list elements to file line by line
    :param list2write:
    :param dest_file
    :return:
    """
    with open(dest_file, 'a', encoding='utf-8') as f:
        for item in list2write:
            f.write(str(item) + '\n')
