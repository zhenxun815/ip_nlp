#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description:
# @File: classify.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 8/5/2019 10:27

import gzip
import os
import pickle
from functools import reduce

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn import metrics
from sklearn.base import TransformerMixin
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from common import logger_factory
from utils import file_utils

logger = logger_factory.get_logger('spacy_nlp')


def load(file_path):
    logger.info(f'load model {file_path}')
    stream = gzip.open(file_path, "rb")
    model = pickle.load(stream)
    stream.close()
    return model


def save(file_path, model):
    logger.info(f'save model {file_path}')
    stream = gzip.open(file_path, "wb")
    pickle.dump(model, stream)
    stream.close()


def load_model(model_path, text_path):
    """
    load model if model files exist, else create, save it and return
    :param model_path:
    :param text_path:
    :return:
    """
    txt_path = os.path.join(model_path, 'txt')
    labels_path = os.path.join(model_path, 'labels')
    if os.path.exists(txt_path) and os.path.exists(labels_path):
        logger.info(f'model to load at {model_path} exist')
        # load the model
        txt = load(txt_path)
        labels = load(labels_path)
        return txt, labels
    else:
        logger.info(f'model to load at {model_path} not exist')
        df = get_df(text_path)
        txt = df['text'].tolist()
        labels = df['clf'].tolist()
        save(txt_path, txt)
        save(labels_path, labels)
        return txt, labels


def show_figure(data):
    sns.barplot(x=data['clf'].unique(), y=data['clf'].value_counts())
    plt.show()


def print_n_most_informative(vectorizer, clf, N, labels):
    feature_names = vectorizer.get_feature_names()
    for i in range(len(clf.coef_)):
        logger.info(f'label is {labels[i]}')
        coefs_with_fns = sorted(zip(clf.coef_[i], feature_names))
        top_class1 = coefs_with_fns[:N]
        top_class2 = coefs_with_fns[:-(N + 1):-1]
        logger.info("Class 1 best: ")
        for feat in top_class1:
            logger.info(feat)
        logger.info("Class 2 best: ")
        for feat in top_class2:
            logger.info(feat)


def tokenize_text(sample):
    return sample.split()


def get_df(path, show_df_info=False):
    """
    get dataFrame, if show_df_info is True, log the dataFrame head, null value count ands ample data.
    :param path:
    :param show_df_info:
    :return:
    """
    logger.info(f'get data frame from file {path}')

    contents = file_utils.read_line(path, lambda content: (content[0], content[1]), split='\t')

    df = pd.DataFrame(contents, columns=['clf', 'text'])
    if show_df_info:
        logger.info(f'df head is \n {df.head()}')
        logger.info(f'isnull count:\n {df.isnull().sum()}')
        logger.info(f'train sample clf: {df["clf"].iloc[0]}, text: {df["text"].iloc[0]}')
    return df


class CleanTextTransformer(TransformerMixin):
    def transform(self, X, **transform_params):
        return [text for text in X]

    def fit(self, X, y=None, **fit_params):
        return self


if __name__ == '__main__':

    tfidf_vectorizer = TfidfVectorizer(tokenizer=tokenize_text, token_pattern=r'\b\w+\b', ngram_range=(1, 1))
    clf = LinearSVC(C=1)
    # clf = tree.DecisionTreeClassifier(min_samples_split=10, criterion="gini")
    clf = RandomForestClassifier(n_estimators=30, criterion='entropy', min_samples_split=20)
    pipe = Pipeline([('cleanText', CleanTextTransformer()), ('vectorizer', tfidf_vectorizer), ('clf', clf)])

    # base_dir = 'E:/ip_data'
    base_dir = '../../resources'
    text_dir = file_utils.make_dirs(base_dir, 'train')

    train_modle_dir = file_utils.make_dirs(base_dir, 'svc/train')
    train_text_file = os.path.join(text_dir, 'train.txt')
    test_modle_dir = file_utils.make_dirs(base_dir, 'svc/test')
    test_text_file = os.path.join(text_dir, 'val.txt')

    train_txt, train_labels = load_model(train_modle_dir, train_text_file)
    test_txt, test_labels = load_model(test_modle_dir, test_text_file)
    # train
    pipe.fit(train_txt, train_labels)
    # test
    preds = pipe.predict(test_txt)
    logger.info(f'accuracy:{accuracy_score(test_labels, preds)}')
    logger.info("Top 10 features used to predict: ")

    labels = reduce(lambda x, y: x if y in x else x + [y], [[]] + train_labels)
    print(f'labels is {labels}')
    # print_n_most_informative(tfidf_vectorizer, clf, 10, labels)

    pipe = Pipeline([('cleanText', CleanTextTransformer()), ('vectorizer', tfidf_vectorizer)])
    transform = pipe.fit_transform(train_txt, train_labels)
    vocab = tfidf_vectorizer.get_feature_names()
    for i in range(len(train_txt)):
        s = ""
        index_into_vocab = transform.indices[transform.indptr[i]:transform.indptr[i + 1]]
        num_occurences = transform.data[transform.indptr[i]:transform.indptr[i + 1]]
        for idx, num in zip(index_into_vocab, num_occurences):
            s += str((vocab[idx], num))
    logger.info(f"{metrics.classification_report(test_labels, preds, target_names=labels)}")
