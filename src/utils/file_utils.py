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


def save_list2file(list2write, dest_file: str):
    """
    write list elements to file line by line
    :param list2write:
    :param dest_file
    :return:
    """
    with open(dest_file, 'a', encoding='utf-8') as f:
        for item in list2write:
            # print('item to write {}'.format(item))
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
        raise Exception(f'{dir_path} is not a dir')


def read_line(file2read, work, split=None):
    with open(file2read, encoding='utf-8') as f:
        for line in f:
            if split:
                work_content = line.strip().split(split)
                if len(work_content) > 1:
                    yield work(work_content)
            else:
                yield work(line.strip())


def remove_redundant(origin_file, dest_file):
    """
    make lines unique and write to a new file
    :param origin_file:
    :param dest_file:
    :return:
    """
    print(f'origin file is: {origin_file}, dest file is: {dest_file}')
    lines = read_line(origin_file, lambda line: line)

    unique_lines = []
    for line in lines:
        if unique_lines.count(line) > 0:
            print('line redundant...')
            continue
        print('add line ...')
        unique_lines.append(line)

    save_list2file(unique_lines, dest_file)


if __name__ == '__main__':

    remove_redundant('E:/ip_data/train/1300/test.txt', 'E:/ip_data/train/1300/test2.txt')
