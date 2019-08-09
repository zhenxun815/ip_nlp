#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: classify.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 8/5/2019 10:27

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn import metrics
from sklearn.base import TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from common import logger_factory
from utils import file_utils

logger = logger_factory.get_logger('spacy_nlp')


def show_figure(data):
    sns.barplot(x=data['clf'].unique(), y=data['clf'].value_counts())
    plt.show()


def print_n_most_informative(vectorizer, clf, N):
    feature_names = vectorizer.get_feature_names()
    coefs_with_fns = sorted(zip(clf.coef_[0], feature_names))
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
    train_dada_path = 'E:/ip_data/train/train.txt'
    test_dada_path = 'E:/ip_data/train/test.txt'
    train_df = get_df(train_dada_path)
    test_df = get_df(train_dada_path)
    logger.info(f'train data set shape is: {train_df.shape}')
    logger.info(f'test data set shape is: {test_df.shape}')

    # show_figure(train)
    vectorizer = CountVectorizer(tokenizer=tokenize_text, ngram_range=(1, 1))
    tfidf_vectorizer = TfidfVectorizer(vectorizer)
    clf = LinearSVC()
    pipe = Pipeline([('cleanText', CleanTextTransformer()), ('vectorizer', tfidf_vectorizer), ('clf', clf)])
    # data
    train_txt = train_df['text'].tolist()
    train_labels = train_df['clf'].tolist()
    test_txt = test_df['text'].tolist()
    test_labels = test_df['clf'].tolist()
    # train
    pipe.fit(train_txt, train_labels)
    # test
    preds = pipe.predict(test_txt)
    logger.info(f'accuracy:{accuracy_score(test_labels, preds)}')
    logger.info("Top 10 features used to predict: ")

    print_n_most_informative(tfidf_vectorizer, clf, 10)
    pipe = Pipeline([('cleanText', CleanTextTransformer()), ('vectorizer', tfidf_vectorizer)])
    transform = pipe.fit_transform(train_txt, train_labels)
    vocab = tfidf_vectorizer.get_feature_names()
    for i in range(len(train_txt)):
        s = ""
        indexIntoVocab = transform.indices[transform.indptr[i]:transform.indptr[i + 1]]
        numOccurences = transform.data[transform.indptr[i]:transform.indptr[i + 1]]
        for idx, num in zip(indexIntoVocab, numOccurences):
            s += str((vocab[idx], num))

    logger.info(metrics.classification_report(test_labels, preds, target_names=train_df['clf'].unique()))
