# coding: utf-8

import os
from collections import Counter

import numpy as np
import tensorflow.keras as kr

from utils import file_utils


def read_file(filename):
    """读取文件数据"""
    contents, labels = [], []
    with open(filename, encoding='utf-8') as f:
        for line in f:
            try:
                label, content = line.split('\t')
                if content:
                    contents.extend(content.split())
                    section_label = label[0:4]
                    # print('section label is {}'.format(section_label))
                    labels.append(section_label)
            except:
                pass
    return contents, labels


def build_vocab(train_txt_path, vocab_txt_path, vocab_size=5000):
    """根据训练集构建词汇表，存储"""
    data2train, _ = read_file(train_txt_path)

    counter = Counter(data2train)
    count_pairs = counter.most_common(vocab_size - 1)
    words, _ = list(zip(*count_pairs))
    # 添加一个 <PAD> 来将所有文本pad为同一长度
    words = ['<PAD>'] + list(words)
    file_utils.save_list2file(words, vocab_txt_path)


def read_vocab(vocab_dir):
    """读取词汇表"""
    # words = open_file(vocab_dir).read().strip().split('\n')
    with open(vocab_dir, encoding='utf-8') as fp:
        words = [_.strip() for _ in fp.readlines()]
    word_to_id = dict(zip(words, range(len(words))))
    return words, word_to_id


def read_category(seged_dir_path):
    """读取分类目录，固定"""
    # categories = []

    categories = [x[0:4] for x in os.listdir(seged_dir_path)]
    for cat in categories:
        print('cat is {}'.format(cat))
    cat_to_id = dict(zip(categories, range(len(categories))))

    return categories, cat_to_id


def to_words(content, words):
    """将id表示的内容转换为文字"""
    return ''.join(words[x] for x in content)


def process_file(filename, word_to_id, cat_to_id, max_length=600):
    """将文件转换为id表示"""
    contents, labels = read_file(filename)

    data_id, label_id = [], []
    for i in range(len(contents)):
        data_id.append([word_to_id[x] for x in contents[i] if x in word_to_id])
        label_id.append(cat_to_id[labels[i]])

    # 使用keras提供的pad_sequences来将文本pad为固定长度
    x_pad = kr.preprocessing.sequence.pad_sequences(data_id, max_length)
    y_pad = kr.utils.to_categorical(label_id, num_classes=len(cat_to_id))  # 将标签转换为one-hot表示

    return x_pad, y_pad


def batch_iter(x, y, batch_size=64):
    """生成批次数据"""
    data_len = len(x)
    num_batch = int((data_len - 1) / batch_size) + 1

    indices = np.random.permutation(np.arange(data_len))
    x_shuffle = x[indices]
    y_shuffle = y[indices]

    for i in range(num_batch):
        start_id = i * batch_size
        end_id = min((i + 1) * batch_size, data_len)
        yield x_shuffle[start_id:end_id], y_shuffle[start_id:end_id]


if __name__ == '__main__':
    base_dir = 'E:/ip_data'
    train_dir = os.path.join(base_dir, 'train')
    train_txt = os.path.join(train_dir, 'train.txt')
    vocab_txt = os.path.join(train_dir, 'vocab.txt')
    build_vocab(train_txt, vocab_txt, 400000)
