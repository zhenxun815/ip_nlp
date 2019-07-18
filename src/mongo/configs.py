#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: configs.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/18/2019 12:05


class MongoConfigs:
    """configs of mongodb"""
    # uri configs
    db_host = '192.168.1.205'
    db_port = 27017
    username = 'tqhy'
    password = 'tqhy817'
    auth_source = 'admin'

    # db configs
    db_ip_doc = 'ip_doc'
    clc_raw = 'raw'
    clc_seg = 'seg'
    index_section = 'section'
    index_main_class = 'mainClass'
    index_sub_class = 'subClass'
