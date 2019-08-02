#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description:
# @File: clf_tokens_task.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/22/2019 14:10
import json
import os.path

from common import logger_factory

logger = logger_factory.get_logger('clf_tokens_task')


def get_tokens(file_path):
    with open(file_path) as f:
        line = f.readline()
        line_json = json.loads(line)
        logger.info(f'line_json is {line_json}')
        keys = line_json['key']
        logger.info(f'keys is {keys}')
        for doc_id, tokens in keys.items():
            # logger.info(f'id {doc_id}, tokens {tokens}')
            yield tokens


def write_tokens(store_file_path, clf_name, tokens):
    with open(store_file_path, 'a', encoding='utf-8') as f:
        for token in tokens:
            content = f'{clf_name} \t {token}\n'
            # logger.info(f'content to write is {content}')
            f.write(content)


def do_work(base_path, store_train_file_path, store_val_file_path):
    for file in os.listdir(base_path):
        splits = file.split('.')
        clf_name = splits[0].replace('_', '')
        logger.info(f'clf_name is {clf_name}')
        if file.endswith('.json'):
            file_path = os.path.join(base_path, file)
            logger.info(f'file to parse is {file_path}')
            tokens = list(get_tokens(file_path))
            clf_tokens_count = len(tokens)
            if clf_tokens_count > 10:
                write_tokens(store_val_file_path, clf_name, tokens[:5])
                write_tokens(store_train_file_path, clf_name, tokens[5:])


# base_path = '/home/tqhy/ip_nlp/resources/result/keys_TextRank'
# store_file_path = os.path.join(base_path, 'ip_tokens.txt')
if __name__ == '__main__':
    base_path = '/home/tqhy/ip_nlp/resources/result/keys_TextRank'
    store_train_file_path = os.path.join(base_path, 'cnews.train.txt')
    store_val_file_path = os.path.join(base_path, 'cnews.val.txt')
    do_work(base_path, store_train_file_path, store_val_file_path)
