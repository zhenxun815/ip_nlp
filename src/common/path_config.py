#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: path_config.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 8/2/2019 9:38
import os

base_dir = 'E:/ip_data'
cnki_dict = os.path.join(base_dir, 'cnki_dict.txt')
train_dir = os.path.join(base_dir, 'train')
train_txt = os.path.join(train_dir, 'train.txt')
test_txt = os.path.join(train_dir, 'test.txt')
val_txt = os.path.join(train_dir, 'val.txt')
vocab_txt = os.path.join(train_dir, 'vocab.txt')

save_dir = os.path.join(train_dir, 'checkpoints/textcnn')
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
save_path = os.path.join(save_dir, 'best_validation')  # 最佳验证结果保存路径

seged_clf_path = os.path.join(base_dir, 'seged')
tensorboard_dir = os.path.join(base_dir, 'tensorboard/textcnn')

logs_dir = os.path.join(base_dir, 'logs')
