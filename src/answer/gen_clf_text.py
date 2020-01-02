#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description:
# @File: gen_clf_text.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 12/12/2019 11:39
from utils import file_utils


def get_content_dict(answers_dir, spliter):
    total_content_dict = {}
    for content_file in file_utils.get_files(answers_dir):
        content_dict = dict(file_utils.read_line(content_file,
                                                 lambda content: (content[0], content[1]),
                                                 split=spliter))
        total_content_dict.update(content_dict)

    return total_content_dict


def gen_train_text(answers_dir, seged_texts_dir, train_file):
    total_answers = get_content_dict(answers_dir, ':')
    # list_utils.print_dict(total_answers)

    total_seged_texts = get_content_dict(seged_texts_dir, '\t')
    # list_utils.print_dict(total_seged_texts)

    train_list = [(clf, total_seged_texts.get(_id)) for _id, clf in total_answers.items()]
    # list_utils.print_list(train_list)

    file_utils.save_list2file(train_list, train_file, lambda pair: f'{pair[0]}\t{pair[1]}')


if __name__ == '__main__':
    answers_dir_path = 'E:/ip_data/classification/20190903/right_answers/'
    seged_texts_dir_path = 'E:/ip_data/classification/20190903/seged/'
    train_file_path = 'E:/ip_data/classification/20190903/train.txt'
