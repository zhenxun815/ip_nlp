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
eng_pattern = re.compile(r'[a-zA-Z][a-zA-Z0-9]+')

area_list = list(file_utils.read_line('D:/tq_workspace/ip_nlp/resources/stps/area.txt', lambda line: line))
stp_list = list(file_utils.read_line('D:/tq_workspace/ip_nlp/resources/stps/stp_dict.stp', lambda line: line))
phrase_count = 0


def extract_eng(raw_phrase_txt, eng_file):
    engs_lists = file_utils.read_line(raw_phrase_txt, lambda line: eng_pattern.findall(line))
    file_utils.save_list2file(engs_lists, eng_file, lambda engs: '\n'.join(engs))


def reg_phrase(raw_phrase):
    for area in area_list:
        # print(f'area{area}')
        if raw_phrase.startswith(area):
            return []
    raw_phrase = brackets_pattern.sub(':', raw_phrase)
    raw_phrase = character_pattern.sub(':', raw_phrase)
    return remove_stp(raw_phrase)


def remove_stp(raw_phrase: str):
    print(f'before remove stp {raw_phrase}')
    for stp in stp_list:
        if raw_phrase.find(stp) > -1:
            raw_phrase = raw_phrase.replace(stp, ':')
    print(f'after remove stp {raw_phrase}')
    return raw_phrase.split(':')


def should_add(words):
    if len(words) > 1:
        print(f'add {words}')
        return True
    print(f'not add {words}')
    return False


def not_names(words):
    start = words[0]
    end = words[-1]
    # print(f'{start}')
    suff_list = ['报', '厂', '店', '房', '馆', '会', '局', '刊', '郎', '楼', '司', '所', '社', '团', '校', '学', '院']
    pre_list = ['阿', '奥', '埃', '艾',
                '巴', '贝', '本', '比', '别', '索', '拜', '彼', '伯', '博', '布',
                '达', '大', '德', '杜', '迪',
                '厄', '恩',
                '弗', '菲', '福', '费', '冯', '丰',
                '格', '戈', '盖',
                '豪', '海', '黑', '赫', '霍', '哈',
                '贾', '津', '加', '季',
                '卡', '克', '库', '科',
                '拉', '莱', '赖', '朗', '勒', '里', '利', '林', '铃' '卢', '鲁', '洛', '伦', '罗', '吕',
                '马', '麦', '门', '梅', '米', '姆', '穆', '莫', '默', '孟',
                '纳', '尼', '涅', '诺',
                '欧',
                '佩', '帕', '皮', '普',
                '齐', '乔', '切',
                '让',
                '萨', '赛', '塞' '瑟', '苏', '斯', '沙', '舍', '史', '施', '什', '索', '朔', '舒',
                '瓦', '沃', '韦', '魏', '危', '维', '威', '温', '翁', '乌',
                '希', '西', '席', '夏', '肖', '谢', '休', '许',
                '雅', '亚', '扬', '耶', '叶', '伊', '乙', '尤', '于', '约',
                '泽', '扎', '兹', '佐']

    return start not in pre_list and end not in suff_list


def clean(raw_phrase_txt):
    reged_phrases = file_utils.read_line(raw_phrase_txt, lambda line: reg_phrase(line))
    clearn_phrases = [words for reged_phrase in reged_phrases for words in reged_phrase if should_add(words)]
    # clearn_phrases.sort()
    return list(set(clearn_phrases))


def count_phrase(phrases: list):
    phrase_dict = {}
    for phrase in phrases:
        count = phrases.count(phrase)
        phrase_dict[phrase] = count
        print(f'phrase {phrase},count {count}')
    return phrase_dict


def group_phrases(origin_file, short_file, common_file, long_file):
    phrases = file_utils.read_line(origin_file)
    short_phrases = []
    common_phrases = []
    long_phrases = []
    for phrase in phrases:
        print(f'{phrase}')
        if len(phrase) < 3:
            short_phrases.append(phrase)
        elif len(phrase) > 10:
            long_phrases.append(phrase)
        else:
            common_phrases.append(phrase)

    file_utils.save_list2file(short_phrases, short_file)
    file_utils.save_list2file(common_phrases, common_file)
    file_utils.save_list2file(long_phrases, long_file)


def seg_long_phrases(origin_long_txt, seged_long_txt2):
    segs_list = file_utils.read_line(origin_long_txt, lambda line: segment.seg_text(line))
    seg_list = [seg for segs in segs_list for seg in segs.split(' ') if len(seg) > 1]
    file_utils.save_list2file(list(set(seg_list)), seged_long_txt2)


def join_phrases(phrase_txt1, phrase_txt2, phrase_union_txt):
    print(f'start join...')
    s1 = set(file_utils.read_line(phrase_txt1))
    s2 = set(file_utils.read_line(phrase_txt2))
    l = list(s1.union(s2))
    l.sort()
    file_utils.save_list2file(l, phrase_union_txt)


if __name__ == '__main__':
    raw_phrase_txt = 'E:/cnki_trans.txt'
    clean_dict_txt = 'E:/cnki_trans_clean.txt'
    short_txt = 'E:/cnki_trans_clean_short.txt'
    common_txt = 'E:/cnki_trans_clean_common.txt'
    long_txt = 'E:/cnki_trans_clean_long.txt'
    phrase_union_txt = 'E:/cnki_trans_union.txt'
    stp1 = 'D:/tq_workspace/ip_nlp/resources/stps/stp_dict.stp'
    stp2 = 'D:/tq_workspace/ip_nlp/resources/stps/stp_words.txt'
    stp3 = 'D:/tq_workspace/ip_nlp/resources/stps/stpAll.txt'

    join_phrases(stp1, stp2, stp3)
