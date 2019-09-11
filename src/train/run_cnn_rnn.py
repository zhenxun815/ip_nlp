#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
# @Description:
# @File: run_cnn_rnn.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 8/19/2019 10:22
import pandas as pd
import tensorflow.python.keras as kr

from utils.file_utils import read_line


def load_data(data_path):
    datas = read_line(data_path,
                      lambda line_contents: (line_contents[0], line_contents[1]),
                      split='\t')

    # return zip(*datas)
    return datas


def get_df_labels(df):
    label_set = df['labels'].unique()
    label_dict = dict(zip(label_set, range(len(label_set))))
    label_ids = df['labels'].map(lambda label: label_dict[label])
    return np.array(label_ids)


def create_lstm_model():
    model_lstm = kr.models.Sequential()
    model_lstm.add(kr.layers.Embedding(vocabulary_size, 200, input_length=300))
    model_lstm.add(kr.layers.LSTM(100, dropout=0.2, recurrent_dropout=0.2))
    model_lstm.add(kr.layers.Dense(1, activation='sigmoid'))
    model_lstm.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model_lstm


def create_conv_model():
    model_conv = kr.models.Sequential()
    model_conv.add(kr.layers.Embedding(vocabulary_size, 256, input_length=300))
    model_conv.add(kr.layers.Conv1D(256, 3, activation='relu'))
    model_conv.add(kr.layers.MaxPooling1D(pool_size=4))
    model_conv.add(kr.layers.Dropout(0.5))
    model_conv.add(kr.layers.LSTM(256))
    model_conv.add(kr.layers.Dropout(0.5))
    model_conv.add(kr.layers.Dense(50, activation='softmax'))
    model_conv.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model_conv


if __name__ == '__main__':
    # contents = load_data('../../resources/train/test.txt')
    contents = load_data('E:/ip_data/train/rnn/train.txt')

    df = pd.DataFrame(data=contents, columns=['labels', 'texts'])
    df = df.dropna()
    print(f'{df.describe()}')
    print(f'{df.head()}')
    df_labels = get_df_labels(df)

    vocabulary_size = 20000
    tokenizer = kr.preprocessing.text.Tokenizer(num_words=vocabulary_size)
    tokenizer.fit_on_texts(df['texts'])
    sequences = tokenizer.texts_to_sequences(df['texts'])
    data = kr.preprocessing.sequence.pad_sequences(sequences, maxlen=300, padding='post', truncating='post')

    model = create_conv_model()
    model.fit(data, df_labels, validation_split=0.2, epochs=3)
