#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description:
# @File: segment.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/17/2019 10:58
import os
import re

import jieba
import jieba.analyse

from common import logger_factory
from common import path_config

logger = logger_factory.get_logger('segment')

jieba.load_userdict(path_config.cnki_dict)

# match decimal or single character
digit_pattern = re.compile(r'^[0-9]+(\.[0-9]+)?[a-zA-Z%‰]?|^[a-zA-Z]$')
chemistry_pattern1 = re.compile(r'(?P<chemistry>[a-zA-Z]+)(?P<digit>[0-9]+)?\.[0-9]+[%‰]?')
chemistry_pattern2 = re.compile(r'(?P<chemistry>[a-zA-Z]+)(?P<digit>[0-9]+[%‰])')


# chinese punctuations


def load_stop_words(file_path):
    if not os.path.isfile(file_path):
        raise Exception("stop words file does not exist: " + file_path)
    content = open(file_path, 'rb').read().decode('utf-8')
    return [line for line in content.splitlines()]


def is_digit(words: str):
    matcher = digit_pattern.match(words)
    return matcher is not None


def is_chemistry(words: str):
    # logger.info(f'str to judge is {words}')
    matcher1 = chemistry_pattern1.match(words)
    matcher2 = chemistry_pattern2.match(words)
    matcher = matcher1 if matcher1 else matcher2

    return matcher.group('chemistry') if matcher else words


def seg_raw_docs(raw_docs: list):
    return [seg_raw_doc(raw_doc) for raw_doc in raw_docs]


def seg_raw_doc(raw_doc, stop_words: list):
    segmented_title = seg_text(raw_doc['title'], stop_words)
    segmented_abs = seg_text(raw_doc['abs'], stop_words)
    # segmented_claim = seg_text(raw_doc['claim'], stop_words)
    segmented_doc = {'pubId': raw_doc['pubId'],
                     'title': segmented_title,
                     'abs':   segmented_abs,
                     }
    return segmented_doc


def clear_str(string: str):
    string = re.sub(r'\n', '', string)
    string = re.sub(r'\t', '', string)
    string = re.sub(r'\s+', '', string)
    return string


def seg_text(text: str, stop_words: list):
    raw_words = jieba.cut(clear_str(text), cut_all=False)
    tokens = [is_chemistry(token) for token in raw_words if token not in stop_words and not is_digit(token)]
    return ' '.join(tokens)


def test_jieba():
    seg_list_all = jieba.cut("小明硕士毕业于中国科学院本发明计算所，后在日本京都大学深造云计算", cut_all=True)  # 全模式
    seg_list_accuracy = jieba.cut("小明硕士毕业于中国科学院本发明计算所，后在日本京都大学深造云计算", cut_all=False)  # 精确模式
    seg_list_search = jieba.cut_for_search("小明硕士毕业于中国科学院本发明计算所，后在日本京都大学深造云计算")  # 搜索引擎模式
    print('cut all result: ', ', '.join(seg_list_all))
    print('cut accuracy result', ', '.join(seg_list_accuracy))
    print('cut for search result: ', ', '.join(seg_list_search))


if __name__ == '__main__':
    text = '本发明H2O涉及S2园林－机电Al1.0%技术领域\t实用新型 公开，具体A云计算的1000ppm说是一种盆\n栽土壤0.25%养护      ' \
           '作业平台，包括200B1机架、平连接，水管(53)另一端通过水泵H2,89%与水箱(51)相连接；所述)的气管0.01相连接。'
    seg_list_accuracy = jieba.cut(text, cut_all=False)
    print(' '.join(seg_list_accuracy))

    stop_words = load_stop_words('../../resources/stps/stop_words.stp')

    tokens = seg_text(text, stop_words)
    print(f'tokens is {tokens}')
