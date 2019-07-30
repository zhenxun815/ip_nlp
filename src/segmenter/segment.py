#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

import jieba
import jieba.analyse

# @Description:
# @File: segment.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/17/2019 10:58

jieba.load_userdict('../../resources/cnki_dict.txt')

# match decimal or single character
pattern = re.compile(r'^[0-9]+(\.[0-9]+)?[a-zA-Z%‰]*$|^[a-zA-Z]$')


# chinese punctuations


def load_stop_words(file_path):
    if not os.path.isfile(file_path):
        raise Exception("stop words file does not exist: " + file_path)
    content = open(file_path, 'rb').read().decode('utf-8')
    return [line for line in content.splitlines()]


def is_digit(words: str):
    matcher = pattern.match(words)
    return matcher is not None


def seg_raw_docs(raw_docs: list):
    return [seg_raw_doc(raw_doc) for raw_doc in raw_docs]


def seg_raw_doc(raw_doc, stop_words: list):
    segmented_title = seg_text(raw_doc['title'], stop_words)
    segmented_abs = seg_text(raw_doc['abs'], stop_words)
    segmented_claim = seg_text(raw_doc['claim'], stop_words)
    segmented_doc = {'pubId': raw_doc['pubId'],
                     'title': segmented_title,
                     'abs':   segmented_abs,
                     'claim': segmented_claim}
    return segmented_doc


def seg_text(text: str, stop_words: list):
    raw_words = jieba.cut(text, cut_all=False)
    # processed_tokens = [t for t in raw_tokens if not should_remove(t)]
    tokens = [token for token in raw_words if token not in stop_words and not is_digit(token)]
    return ' '.join(tokens)


def test_jieba():
    seg_list_all = jieba.cut("小明硕士毕业于中国科学院本发明计算所，后在日本京都大学深造云计算", cut_all=True)  # 全模式
    seg_list_accuracy = jieba.cut("小明硕士毕业于中国科学院本发明计算所，后在日本京都大学深造云计算", cut_all=False)  # 精确模式
    seg_list_search = jieba.cut_for_search("小明硕士毕业于中国科学院本发明计算所，后在日本京都大学深造云计算")  # 搜索引擎模式
    print('cut all result: ', ', '.join(seg_list_all))
    print('cut accuracy result', ', '.join(seg_list_accuracy))
    print('cut for search result: ', ', '.join(seg_list_search))


if __name__ == '__main__':
    text = '本发明H2O涉及园林机电技术领域，具体的说是一种盆栽土壤0.25%养护作业平台，包括机架、平移装置、旋转装置、插孔装置和辅助装置；平移装置安装在底板上部，平移装置用于实现盆栽的径向直线运动；所述的旋转装置安装在平移装置上方中部，旋转装置用于实现盆栽的周向旋转运动；所述的插孔装置位于机架内部，且插孔装置左右对称设置，插孔装置用于实现对盆栽进行松土、施肥、浇水和干燥的功能；所述的辅助装置位于机架上部。本发明采用将直线导轨与蜗杆蜗轮相结合的设计思路，实现盆栽位置的任意调整，并且通过将曲柄滑块机构与针管的相结合，能够实现松土、浇水、施肥、调节PH值和干燥土壤的功能，极大地减少了人工成本，提高了生产效率。", "claim": "1.一种盆栽土壤养护作业平台，其特征在于：包括机架(1)、平移装置(2)、旋转装置(3)、插孔装置(4)和辅助装置(5)，所述的机架(1)为长方体结构，机架(1)的底部中央设有底板(11)，机架(1)上方设有横梁(12)，所述的底板(11)为前后对称结构；所述的平移装置(2)安装在底板(11)上部；所述的旋转装置(3)安装在平移装置(2)上方中部；所述的插孔装置(4)位于机架(1)内部，且插孔装置(4)左右对称设置；所述的辅助装置(5)与机架(1)相连接，且辅助装置(5)位于机架(1)上方。2.根据权利要求1所述的一种盆栽土壤养护作业平台，其特征在于：所述的平移装置(2)包括一号电机(21)、丝杠(22)、滑动板(23)和两根导轨(24)，所述的两根导轨(24)对称安装在底板(11)上；所述的滑动板(23)安装在两根导轨(24)上，且滑动板(23)通过丝杠螺母副与丝杠(22)相连接；所述的丝杠(22)位于滑动板(24)下方中部，丝杠(22)左端通过轴承安装在机架(1)上，丝杠(22)右端通过联轴器与一号电机(21)相连接；所述的一号电机(21)安装在机架(1)上。3.根据权利要求1所述的一种盆栽土壤养护作业平台，其特征在于：所述的旋转装置(3)包括二号电机(31)、蜗杆(32)、蜗轮(33)和底盘(34)，所述的二号电机(31)通过联轴器与蜗杆(32)相连接；所述的蜗杆(32)安装在滑动板(23)上方；所述的蜗轮(33)水平安装在滑动板(23)上方，且蜗轮(33)与蜗杆(32)相啮合；所述的底盘(34)位于蜗轮(33)中部，且底盘(34)与蜗轮(33)相固连。4.根据权利要求1所述的一种盆栽土壤养护作业平台，其特征在于：所述的插孔装置(4)包括两个三号电机(41)、两个下皮带轮(42)、皮带(43)、两个上皮带轮(44)、两个连杆(45)、导向孔(46)、两个针管(47)和两个支撑架(48)，所述的两个三号电机(41)对称安装在机架(1)上；所述的两个下皮带轮(42)分别与两个三号电机(41)相连；所述的支撑架(48)包括前架(481)和后架(482)，两个支撑架(48)对称安装在横梁(12)下部；所述的两个上皮带轮(44)分别安装在两个后架(482)上，且两个上皮带轮(44)分别通过皮带(43)与下皮带轮(42)相连接；所述的连杆(45)一端与上皮带轮(44)偏心相铰接，连杆(45)另一端与针管(47)上端相铰接；所述的导向孔(46)位于前架(481)下部；所述的针管(47)位于导向孔(46)内部，针管(47)包括上部小孔(471)、下部小孔(472)，所述的上部小孔(471)位于针管(47)上部，所述的下部小孔(472)均匀分布于针管(47)下部，所述的针管(47)下部为空心，且空心部分与上部小孔(471)和下部小孔(472)相连通。5.根据权利要求1所述的一种盆栽土壤养护作业平台，其特征在于：所述的辅助装置(5)包括水箱(51)、水泵、水管(53)、储气罐(52)、气泵、和气管(54)，所述的水箱(51)和储气罐(52)均安装在机架(1)上，所述的水管(53)一端与机架(1)左边针管(47)的上部小孔(471)相连接，水管(53)另一端通过水泵与水箱(51)相连接；所述的气管(54)一端与机架(1)右边针管的上部小孔(471)相连接，气管(54)另一端通过气泵与储气罐(52)相连接。'
    seg_list_accuracy = jieba.cut(text, cut_all=False)
    print(' '.join(seg_list_accuracy))
    stop_words = load_stop_words('../../resources/stps/stopWord.txt')
    tokens = seg_text(text, stop_words)
    print(tokens)
    stop_words = load_stop_words('../../resources/stps/stop_words.stp')
    tokens = seg_text(text, stop_words)
    print(tokens)
