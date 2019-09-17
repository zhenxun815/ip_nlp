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


def make_dirs(base_dir, sub_dir):
    _dir = os.path.join(base_dir, sub_dir)
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    return _dir


def save_dict2file(dict2save: dict, dest_file: str, work=None, split=':'):
    print(f'start writing data to: {dest_file}')
    with open(dest_file, 'a', encoding='utf-8') as f:
        for k, v in dict2save.items():
            print(f'item to write k {k},v {v}')
            if work:
                k, v = work(k, v)
            f.write(f'{k}{split}{v}\n')
        f.flush()
    print(f'complete writing data to: {dest_file}')


def save_list2file(list2save, dest_file: str, work=None):
    """
    write list elements to file line by line
    :param work: func, process each item in the list
    :param list2save:
    :param dest_file
    :return:
    """
    print(f'start writing data to: {dest_file}')
    with open(dest_file, 'a', encoding='utf-8') as f:
        for item in list2save:
            # print(f'item to write {item}')
            if work:
                item = work(item)
            f.write(str(item) + '\n')
    print(f'complete writing data to: {dest_file}')


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
        raise Exception(f'{dir_path} is not a dir')


def read_line(file2read, work, split=None):
    print(f'start reading {file2read}')
    with open(file2read, encoding='utf-8') as f:
        for line in f:
            content = line.strip()
            if split:
                content = content.split(split)
            if work:
                yield work(content)
            else:
                yield content
    print(f'complete reading {file2read}')


def remove_redundant(origin_file, dest_file, keep_order=True):
    """
    make lines unique and write to a new file
    :param keep_order: whether to keep the order of origin list or not
    :param origin_file:
    :param dest_file:
    :return:
    """
    print(f'origin file is: {origin_file}, dest file is: {dest_file}')
    lines = read_line(origin_file, lambda line: line)
    if keep_order:
        save_list2file(list(dict.fromkeys(lines)), dest_file)
    else:
        save_list2file(list(set(lines)), dest_file)


if __name__ == '__main__':

    remove_redundant('E:/cnki_trans_clean4.txt', 'E:/cnki_trans_clean5.txt')
