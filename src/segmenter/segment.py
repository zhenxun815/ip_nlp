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
dna_pattern = re.compile(r'[ACTGU]{8,}')
chinese_pattern = re.compile(r'[\u4E00-\u9FFF]+')
chemistry_pattern1 = re.compile(r'(?P<chemistry>[a-zA-Z]+)(?P<digit>[0-9]+)?\.[0-9]+[%‰]?')
chemistry_pattern2 = re.compile(r'(?P<chemistry>[a-zA-Z]+)(?P<digit>[0-9]+[%‰])')


# chinese punctuations


def load_stop_words(file_path):
    if not os.path.isfile(file_path):
        raise Exception("stop words file does not exist: " + file_path)
    content = open(file_path, 'rb').read().decode('utf-8')
    return [line for line in content.splitlines()]


stop_words = load_stop_words(path_config.stp_words)


def is_digit(words: str):
    matcher1 = digit_pattern.match(words)
    matcher2 = dna_pattern.match(words.upper())
    return matcher1 or matcher2


def is_chinese(words: str):
    return chinese_pattern.match(words) and words not in stop_words


def is_chemistry(words: str):
    # logger.info(f'str to judge is {words}')
    matcher1 = chemistry_pattern1.match(words)
    matcher2 = chemistry_pattern2.match(words)
    matcher = matcher1 if matcher1 else matcher2

    return matcher.group('chemistry') if matcher else words


def seg_raw_docs(raw_docs: list):
    return [seg_raw_doc(raw_doc) for raw_doc in raw_docs]


def seg_raw_doc(raw_doc):
    print(f"pid {os.getpid()} start seg {raw_doc['pubId']}")
    segmented_title = seg_text(raw_doc['title'])
    segmented_abs = seg_text(raw_doc['abs'])
    # segmented_claim = seg_text(raw_doc['claim'], stop_words)
    segmented_doc = {
            'pubId': raw_doc['pubId'],
            'title': segmented_title,
            'abs':   segmented_abs,
    }
    return segmented_doc


def clear_str(string: str):
    string = re.sub(r'\n', '', string)
    string = re.sub(r'\t', '', string)
    string = re.sub(r'\s+', '', string)
    return string


def seg_text(text: str, to_str=True):
    raw_words = jieba.cut(clear_str(text), cut_all=False)
    tokens = [token for token in raw_words if is_chinese(token)]
    return ' '.join(tokens) if to_str else tokens


def test_jieba():
    seg_list_all = jieba.cut("小明硕士毕业于中国科学院本发明计算所，后在日本京都大学深造云计算", cut_all=True)  # 全模式
    seg_list_accuracy = jieba.cut("小明硕士毕业于中国科学院本发明计算所，后在日本京都大学深造云计算", cut_all=False)  # 精确模式
    seg_list_search = jieba.cut_for_search("小明硕士毕业于中国科学院本发明计算所，后在日本京都大学深造云计算")  # 搜索引擎模式
    print('cut all result: ', ', '.join(seg_list_all))
    print('cut accuracy result', ', '.join(seg_list_accuracy))
    print('cut for search result: ', ', '.join(seg_list_search))


if __name__ == '__main__':
    text = '吴式太极拳,最小二乘拟合,acgacgaCGCAAaaaaa,稀土元素地球化学食指操作追踪球和拇指操作追踪球,本发明H2O涉及S2园林－机电Al1.0%技术领域\t实用新型 公开，具体A云计算的1000ppm说是一种盆\n栽土壤0.25%养护      ' \
           '作业平台，包括200B1机架、平连接，水管(53)另一端通过水泵H2,89%与水箱(51)相连接；所述)的气管隐马尔可夫模型0.01相连接。'
    seg_list_accuracy = jieba.cut(text, cut_all=False)
    print(' '.join(seg_list_accuracy))

    tokens = seg_text(text)
    print(f'tokens is {tokens}')
