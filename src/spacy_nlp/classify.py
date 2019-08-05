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
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from common import logger_factory
from utils import file_utils

logger = logger_factory.get_logger('spacy_nlp')


def show_figure(data):
    # fg = plt.figure(figsize=(8,4))
    sns.barplot(x=data['clf'].unique(), y=data['clf'].value_counts())
    plt.show()


def print_n_most_informative(vectorizer, clf, N):
    feature_names = vectorizer.get_feature_names()
    coefs_with_fns = sorted(zip(clf.coef_[0], feature_names))
    top_class1 = coefs_with_fns[:N]
    top_class2 = coefs_with_fns[:-(N + 1):-1]
    print("Class 1 best: ")
    for feat in top_class1:
        print(feat)
    print("Class 2 best: ")
    for feat in top_class2:
        print(feat)


def tokenize_text(sample):
    return sample.split()


class CleanTextTransformer(TransformerMixin):
    def transform(self, X, **transform_params):
        return [text for text in X]

    def fit(self, X, y=None, **fit_params):
        return self


if __name__ == '__main__':
    path = 'E:/ip_data/train/train.txt'
    contents = file_utils.read_line(path, lambda content: (content[0], content[1]), split='\t')
    df = pd.DataFrame(contents, columns=['clf', 'text'])
    logger.info(f'df head is \n {df.head()}')
    logger.info(f'isnull count:\n {df.isnull().sum()}')
    train, test = train_test_split(df, test_size=0.1, random_state=42)
    # logger.info(f'train sample clf: {train["clf"].iloc[0]}, text: {train["text"].iloc[0]}')
    logger.info(f'train data set shape is: {train.shape}')
    logger.info(f'test data set shape is: {test.shape}')

    # show_figure(train)
    vectorizer = CountVectorizer(tokenizer=tokenize_text, ngram_range=(1, 1))
    clf = LinearSVC()
    pipe = Pipeline([('cleanText', CleanTextTransformer()), ('vectorizer', vectorizer), ('clf', clf)])
    # data
    train1 = train['text'].tolist()
    labelsTrain1 = train['clf'].tolist()
    test1 = test['text'].tolist()
    labelsTest1 = test['clf'].tolist()
    # train
    pipe.fit(train1, labelsTrain1)
    # test
    preds = pipe.predict(test1)
    print("accuracy:", accuracy_score(labelsTest1, preds))
    print("Top 10 features used to predict: ")

    print_n_most_informative(vectorizer, clf, 10)
    pipe = Pipeline([('cleanText', CleanTextTransformer()), ('vectorizer', vectorizer)])
    transform = pipe.fit_transform(train1, labelsTrain1)
    vocab = vectorizer.get_feature_names()
    for i in range(len(train1)):
        s = ""
        indexIntoVocab = transform.indices[transform.indptr[i]:transform.indptr[i + 1]]
        numOccurences = transform.data[transform.indptr[i]:transform.indptr[i + 1]]
        for idx, num in zip(indexIntoVocab, numOccurences):
            s += str((vocab[idx], num))

    print(metrics.classification_report(labelsTest1, preds, target_names=df['clf'].unique()))
