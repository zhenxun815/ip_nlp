#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: classification.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/17/2019 12:01


class Classification:
    # docs count of this classification
    count = 0

    def __init__(self, section, main_class, sub_class) -> None:
        self.section = section
        self.main_class = main_class
        self.sub_class = sub_class

    def __str__(self) -> str:
        return '%s_%s_%s' % (self.section, self.main_class, self.sub_class)
