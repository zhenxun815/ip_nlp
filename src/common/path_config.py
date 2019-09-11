#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description:
# @File: path_config.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 8/2/2019 9:38
import os

from utils.file_utils import make_dirs

base_dir = 'E:/ip_data'
# base_dir = '../../resources'
dict_dir = make_dirs(base_dir, 'custom_dict')
cnki_dict = os.path.join(dict_dir, 'cnki_dict.txt')

train_dir = make_dirs(base_dir, 'train/rnn')

train_txt = os.path.join(train_dir, 'train.txt')
test_txt = os.path.join(train_dir, 'test.txt')
val_txt = os.path.join(train_dir, 'val.txt')
vocab_txt = os.path.join(train_dir, 'vocab.txt')

save_dir = make_dirs(train_dir, 'checkpoints/textcnn')
save_path = os.path.join(save_dir, 'best_validation')  # 最佳验证结果保存路径

seged_dir = make_dirs(base_dir, 'clfs/seged')
seged_clf_path = os.path.join(seged_dir, 'rnn')
tensorboard_dir = make_dirs(train_dir, 'tensorboard/textcnn')

logs_dir = make_dirs(base_dir, 'logs')
