#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
# @Description:
# @File: segment.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/17/2019 10:58
from string import punctuation

import jieba

from mongo import doc_service

# match decimal or single character
pattern = re.compile(r'^[0-9]+(\.[0-9]+)?[a-zA-Z]*$|^[a-zA-Z]$')
# chinese punctuations
cn_punctuation = '，。、【】“”：；～（）《》‘’？！①②③④⑤⑥⑦⑧⑨⑩()、％…·℃—￥'
# combine english and chinese punctuations
all_punctuation = punctuation + cn_punctuation


def is_digit(words: str):
    matcher = pattern.match(words)
    return matcher is not None


def should_remove(token: str):
    return token in all_punctuation or is_digit(token)


def seg_raw_docs(raw_docs: list):
    return [seg_raw_doc(raw_doc) for raw_doc in raw_docs]


def seg_raw_doc(raw_doc):
    segmented_title = seg_text(raw_doc['title'])
    segmented_abs = seg_text(raw_doc['abs'])
    segmented_claim = seg_text(raw_doc['claim'])
    segmented_doc = {'pubId': raw_doc['pubId'],
                     'title': segmented_title,
                     'abs':   segmented_abs,
                     'claim': segmented_claim}
    return segmented_doc


def seg_text(text: str):
    raw_tokens = jieba.cut(text, cut_all=False)
    processed_tokens = [t for t in raw_tokens if not should_remove(t)]
    return ' '.join(processed_tokens)


def test_jieba():
    seg_list_all = jieba.cut("小明硕士毕业于中国科学院计算所，后在日本京都大学深造", cut_all=True)  # 全模式
    seg_list_accuracy = jieba.cut("小明硕士毕业于中国科学院计算所，后在日本京都大学深造", cut_all=False)  # 精确模式
    seg_list_search = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
    print('cut all result: ', ', '.join(seg_list_all))
    print('cut accuracy result', ', '.join(seg_list_accuracy))
    print('cut for search result: ', ', '.join(seg_list_search))


if __name__ == '__main__':
    raw_docs = doc_service.find_some('ip_doc', 'raw', 3)
    seged_docs = seg_raw_docs(raw_docs)
    for doc in seged_docs:
        print(doc['pubId'])
        print(doc['title'])
        print(doc['abs'])
        print(doc['claim'])
