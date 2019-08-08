#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description:
# @File: logger_factory.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/19/2019 10:29
import logging
import sys
import time
from logging.handlers import TimedRotatingFileHandler
from os import path

from common import path_config

FORMATTER = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')

TRAIN_LOG_FILE_NAME = time.strftime('train_%y_%m_%d_%H_%M.log', time.localtime())
DEFAULT_LOG_FILE_NAME = 'ip_nlp.log'


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler(train_log=False):
    log_file_name = TRAIN_LOG_FILE_NAME if train_log else DEFAULT_LOG_FILE_NAME
    log_file = path.join(path_config.logs_dir, log_file_name)
    file_handler = TimedRotatingFileHandler(log_file, when='D', encoding='utf-8', backupCount=5)
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name, train_log=False):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)  # better to have too much log than not enough
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler(train_log))
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger
