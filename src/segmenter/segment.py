#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: segment.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/17/2019 10:58


import jieba


def test_jieba():
    seg_list_all = jieba.cut("小明硕士毕业于中国科学院计算所，后在日本京都大学深造", cut_all=True)  # 全模式
    seg_list_accuracy = jieba.cut("小明硕士毕业于中国科学院计算所，后在日本京都大学深造", cut_all=False)  # 精确模式
    seg_list_search = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
    print('cut all result: ', ', '.join(seg_list_all))
    print('cut accuracy result', ', '.join(seg_list_accuracy))
    print('cut for search result: ', ', '.join(seg_list_search))




if __name__ == '__main__':
    test_jieba()
