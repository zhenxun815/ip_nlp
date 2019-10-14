#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description:
# @File: create_dict.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 9/16/2019 11:38
import re

from segmenter import segment
from utils import file_utils

brackets_pattern = re.compile(r'\(.*\)')
character_pattern = re.compile(r'[a-zA-Z0-9]+')
english_pattern = re.compile(r'[a-zA-Z][a-zA-Z0-9]+')
chinese_pattern = re.compile(r'[\u4E00-\u9FFF]+')

phrase_count = 0


def extract_eng(raw_phrase_txt, eng_file):
    engs_lists = file_utils.read_line(raw_phrase_txt, lambda line: english_pattern.findall(line))
    file_utils.save_list2file(engs_lists, eng_file, lambda engs: '\n'.join(engs))


def extract_chn(raw_phrase):
    return chinese_pattern.findall(raw_phrase)


def should_add(words):
    if len(words) > 1:
        print(f'add {words}')
        return True
    print(f'not add {words}')
    return False


def clean(raw_phrase_txt):
    reged_phrases = file_utils.read_line(raw_phrase_txt, lambda line: extract_chn(line))
    clearn_phrases = [words for reged_phrase in reged_phrases for words in reged_phrase]
    # clearn_phrases.sort()
    return set(clearn_phrases)


def count_phrase(phrases: list):
    phrase_dict = {}
    for phrase in phrases:
        count = phrases.count(phrase)
        phrase_dict[phrase] = count
        print(f'phrase {phrase},count {count}')
    return phrase_dict


def group_phrases(origin_file, short_file, median_file, long_file):
    phrases = file_utils.read_line(origin_file)
    short_phrases = []
    median_phrases = []
    long_phrases = []
    for phrase in phrases:
        print(f'{phrase}')
        if len(phrase) < 6:
            short_phrases.append(phrase)
        elif len(phrase) > 10:
            long_phrases.append(phrase)
        else:
            median_phrases.append(phrase)

    file_utils.save_list2file(short_phrases, short_file)
    file_utils.save_list2file(median_phrases, median_file)
    file_utils.save_list2file(long_phrases, long_file)


def seg_long_phrases(origin_long_txt, seged_long_txt2):
    segs_list = file_utils.read_line(origin_long_txt, lambda line: segment.seg_text(line))
    seg_list = [seg for segs in segs_list for seg in segs.split(' ') if len(seg) > 1]
    file_utils.save_list2file(list(set(seg_list)), seged_long_txt2)


def join_phrases(phrase_union_txt, *phrase_txts):
    print(f'start join...')
    phrase_set = set()
    for phrase_txt in phrase_txts:
        for phrase in file_utils.read_line(phrase_txt):
            if len(phrase) < 6:
                phrase_set.add(phrase)
        print(f'set phrases is:  {phrase_set}')
    l = list(phrase_set)
    l.sort()
    file_utils.save_list2file(l, phrase_union_txt)


if __name__ == '__main__':
    raw_phrase_txt = 'E:/cnki_trans.txt'
    cnki_dict_txt = 'E:/cnki_dict.txt'
    short_txt = 'E:/cnki_short.txt'
    median_txt = 'E:/cnki_median.txt'
    median_txt2 = 'E:/cnki_median2.txt'
    long_txt = 'E:/cnki_long.txt'
    phrase_union_txt = 'E:/cnki_union.txt'
    stp1 = 'D:/tq_workspace/ip_nlp/resources/stps/stp_dict.stp'
    stp2 = 'D:/tq_workspace/ip_nlp/resources/stps/stp_words.txt'
    stp3 = 'D:/tq_workspace/ip_nlp/resources/stps/stpAll.txt'

    nwd_dir = 'E:/dict/nwd'
    nwd_dict_txt = 'E:/dict/nwd_dict.txt'
    # clean_phrases = clean(cnki_dict_txt)
    # file_utils.save_list2file(clean_phrases, clean_dict_txt)
    # join_phrases(cnki_dict_txt, raw_phrase_txt, phrase_union_txt)
    # nwd_files = file_utils.get_files(nwd_dir)
    # join_phrases(nwd_dict_txt, *nwd_files)
    st = 'A21D    '
    print(f"{len(st.split())}")
