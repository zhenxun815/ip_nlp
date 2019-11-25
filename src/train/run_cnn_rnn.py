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

from utils import file_utils


def load_data(data_path):
    datas = file_utils.read_line(data_path,
                                 lambda line_contents: (line_contents[0], line_contents[1]),
                                 split='\t')

    # return zip(*datas)
    return datas


# def get_df_labels(df, label_dict):
def get_df_labels(df, label_dict, label_set):
    label_ids = df['labels'].map(lambda label: label_dict[label])

    return kr.utils.to_categorical(label_ids, num_classes=len(label_set))


def create_lstm_model():
    model_lstm = kr.models.Sequential()
    model_lstm.add(kr.layers.Embedding(max_vocab_size, 200, input_length=300))
    model_lstm.add(kr.layers.LSTM(100, dropout=0.2, recurrent_dropout=0.2))
    model_lstm.add(kr.layers.Dense(1, activation='sigmoid'))
    model_lstm.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model_lstm


def create_embedding_matrix(vectors_file, word_index, embedding_dim):
    vocab_size = len(word_index) + 1  # Adding again 1 because of reserved 0 index
    matrix = np.zeros((vocab_size, embedding_dim))
    with open(vectors_file) as f:
        for line in f:
            word, *vector = line.split()
            if word in word_index:
                idx = word_index[word]
                matrix[idx] = np.array(vector, dtype=np.float32)[:embedding_dim]

    nonzero_elements = np.count_nonzero(np.count_nonzero(matrix, axis=1))
    print(f'embedding matrix non zero portion: {nonzero_elements / vocab_size}')
    return matrix


def find_words_not_in_vec(word_index, vectors_file, inclue_file, exclude_file):
    vec_words = file_utils.read_line(vectors_file, lambda line: line.split()[0])
    print(f'{vec_words[0]}')
    exclude_words = [word for word in word_index if word not in vec_words]
    include_words = [word for word in word_index if word in vec_words]
    file_utils.save_list2file(exclude_words, exclude_file)
    file_utils.save_list2file(include_words, inclue_file)


# def create_conv_model():
def create_conv_model(vocab_size, embedding_matrix, cat_num):
    model_conv = kr.models.Sequential()
    model_conv.add(kr.layers.Embedding(vocab_size, embedding_dim,
                                       weights=[embedding_matrix],
                                       trainable=False,
                                       input_length=max_len))
    model_conv.add(kr.layers.Conv1D(128, 3, activation='relu'))

    # model_conv.add(kr.layers.MaxPooling1D(pool_size=3))
    model_conv.add(kr.layers.GlobalMaxPool1D())
    # model_conv.add(kr.layers.Flatten())
    model_conv.add(kr.layers.Dense(256, activation='relu'))
    model_conv.add(kr.layers.Dropout(0.3))
    model_conv.add(kr.layers.Dense(cat_num, activation='relu'))
    model_conv.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model_conv


# def run_model():
def run_model(train_text, train_labels, test_text, test_labels):
    model = create_conv_model()
    model.summary()
    model.fit(train_text, train_labels, validation_data=(test_text, test_labels), epochs=10, batch_size=100)
    loss, accuracy = model.evaluate(train_text, train_labels, verbose=False)
    print(f'loss: {loss}, accuracy: {accuracy}')


if __name__ == '__main__':
    max_vocab_size = 20000
    max_len = 150
    embedding_dim = 256

    train_df = pd.read_csv('E:/ip_data/train/no_limit_sample/train.txt', sep='\t', names=['labels', 'texts'])
    train_df = train_df.dropna()
    label_set = train_df['labels'].unique()
    cat_num = len(label_set)
    label_dict = dict(zip(label_set, range(cat_num)))
    print(f'{train_df.describe()}')
    print(f'{train_df.head()}')
    train_labels = get_df_labels(train_df, label_dict, label_set)

    test_df = pd.read_csv('E:/ip_data/train/no_limit_sample/test.txt', sep='\t', names=['labels', 'texts'])
    test_df = test_df.dropna()

    tokenizer = kr.preprocessing.text.Tokenizer(num_words=max_vocab_size)
    tokenizer.fit_on_texts(train_df['texts'])
    tokenizer.fit_on_texts(test_df['texts'])

    train_sequences = tokenizer.texts_to_sequences(train_df['texts'])
    # list_utils.print_all(sequences, print_commont='sequence: ', print_index=True)
    vocab_size = len(tokenizer.word_index) + 1
    train_text = kr.preprocessing.sequence.pad_sequences(train_sequences, maxlen=max_len, padding='post',
                                                         truncating='post')
    # print(f'real_vocab_size: {vocab_size}')
    # print(f"{train_df['texts'][2]}")
    # print(f"{train_sequences[2]}")
    # print(f"{train_text[2]}")

    test_df = pd.read_csv('E:/ip_data/train/no_limit_sample/test.txt', sep='\t', names=['labels', 'texts'])
    test_df = test_df.dropna()
    test_labels = get_df_labels(test_df, label_dict, label_set)
    # print(f'{train_labels}')
    test_sequences = tokenizer.texts_to_sequences(test_df['texts'])
    test_text = kr.preprocessing.sequence.pad_sequences(test_sequences, maxlen=max_len, padding='post',
                                                        truncating='post')

    embedding_matrix = create_embedding_matrix('E:/ip_data/train/no_limit_sample/vectors.txt',
                                               tokenizer.word_index,
                                               embedding_dim)

    # print(f'embedding_matrix: {embedding_matrix}')
    """
    find_words_not_in_vec(tokenizer.word_index,
                          'E:/ip_data/train/no_limit_sample/vectors.txt',
                          'E:/ip_data/train/no_limit_sample/exclude.txt',
                          'E:/ip_data/train/no_limit_sample/include.txt')
    """
    # run_model()
