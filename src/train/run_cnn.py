#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import time
from datetime import datetime
from datetime import timedelta

import numpy as np
import tensorflow as tf
from sklearn import metrics

from common import logger_factory
from common import path_config
from train.cnn_model import TCNNConfig, TextCNN
from train.data_loader import read_vocab, read_category, batch_iter, process_file, build_vocab, process_question_file

base_dir = path_config.base_dir
train_txt = path_config.train_txt
test_txt = path_config.test_txt
val_txt = path_config.val_txt
vocab_txt = path_config.vocab_txt

save_path = path_config.save_path  # 最佳验证结果保存路径

seged_clf_path = path_config.seged_clf_path
tensorboard_dir = path_config.tensorboard_dir


def get_time_dif(start_time):
    """获取已使用时间"""
    end_time = time.time()
    time_dif = end_time - start_time
    return timedelta(seconds=int(round(time_dif)))


def feed_data(x_batch, y_batch, keep_prob):
    feed_dict = {
            model.input_x:   x_batch,
            model.input_y:   y_batch,
            model.keep_prob: keep_prob
    }
    return feed_dict


def evaluate(sess, x_, y_):
    """评估在某一数据上的准确率和损失"""
    data_len = len(x_)
    batch_eval = batch_iter(x_, y_, 128)
    total_loss = 0.0
    total_acc = 0.0
    for x_batch, y_batch in batch_eval:
        batch_len = len(x_batch)
        feed_dict = feed_data(x_batch, y_batch, 1.0)
        loss, acc = sess.run([model.loss, model.acc], feed_dict=feed_dict)
        total_loss += loss * batch_len
        total_acc += acc * batch_len

    return total_loss / data_len, total_acc / data_len


def train():
    train_logger.info("Configuring TensorBoard and Saver...")
    # 配置 Tensorboard，重新训练时，请将tensorboard文件夹删除，不然图会覆盖

    if not os.path.exists(tensorboard_dir):
        os.makedirs(tensorboard_dir)

    tf.summary.scalar("loss", model.loss)
    tf.summary.scalar("accuracy", model.acc)
    merged_summary = tf.summary.merge_all()
    writer = tf.summary.FileWriter(tensorboard_dir)

    # 配置 Saver
    saver = tf.train.Saver()

    train_logger.info("Loading training and validation data...")
    # 载入训练集与验证集
    start_time = time.time()
    x_train, y_train = process_file(train_txt, word_to_id, cat_to_id, config.seq_length)
    x_val, y_val = process_file(val_txt, word_to_id, cat_to_id, config.seq_length)
    time_dif = get_time_dif(start_time)
    train_logger.info(f'Time usage:{time_dif}')

    # 创建session
    session = tf.Session()
    session.run(tf.global_variables_initializer())
    writer.add_graph(session.graph)

    train_logger.info('Training and evaluating...')
    start_time = time.time()
    total_batch = 0  # 总批次
    best_acc_val = 0.0  # 最佳验证集准确率
    last_improved = 0  # 记录上一次提升批次
    require_improvement = 1000  # 如果超过1000轮未提升，提前结束训练

    flag = False
    for epoch in range(config.num_epochs):
        train_logger.info(f'Epoch:{epoch + 1}')
        batch_train = batch_iter(x_train, y_train, config.batch_size)
        for x_batch, y_batch in batch_train:
            feed_dict = feed_data(x_batch, y_batch, config.dropout_keep_prob)

            if total_batch % config.save_per_batch == 0:
                # 每多少轮次将训练结果写入tensorboard scalar
                s = session.run(merged_summary, feed_dict=feed_dict)
                writer.add_summary(s, total_batch)

            if total_batch % config.print_per_batch == 0:
                # 每多少轮次输出在训练集和验证集上的性能
                feed_dict[model.keep_prob] = 1.0
                loss_train, acc_train = session.run([model.loss, model.acc], feed_dict=feed_dict)
                loss_val, acc_val = evaluate(session, x_val, y_val)  # todo

                if acc_val > best_acc_val:
                    # 保存最好结果
                    best_acc_val = acc_val
                    last_improved = total_batch
                    saver.save(sess=session, save_path=save_path)
                    improved_str = '*'
                else:
                    improved_str = ''

                time_dif = get_time_dif(start_time)
                msg = 'Iter: {0:>6}, Train Loss: {1:>6.2}, Train Acc: {2:>7.2%},' \
                      + ' Val Loss: {3:>6.2}, Val Acc: {4:>7.2%}, Time: {5} {6}'
                train_logger.info(
                        msg.format(total_batch, loss_train, acc_train, loss_val, acc_val, time_dif, improved_str))

            feed_dict[model.keep_prob] = config.dropout_keep_prob
            session.run(model.optim, feed_dict=feed_dict)  # 运行优化
            total_batch += 1

            if total_batch - last_improved > require_improvement:
                # 验证集正确率长期不提升，提前结束训练
                train_logger.info("No optimization for a long time, auto-stopping...")
                flag = True
                break  # 跳出循环
        if flag:  # 同上
            break


def write_answer_str(y_test, y_pred, answer_file):
    with open(answer_file, 'a', encoding='utf-8') as f:
        for index, y_pred_cls_item in enumerate(y_pred):
            str2write = f'{y_test[index]}:{categories[y_pred_cls_item]}'
            print(str2write)
            f.write(f'{str2write}\n')


def answer(question_file, answer_file):
    train_logger.info("Loading test data...")
    start_time = time.time()
    x_test, y_test = process_question_file(question_file, word_to_id, config.seq_length)
    session = tf.Session()
    session.run(tf.global_variables_initializer())
    saver = tf.train.Saver()
    saver.restore(sess=session, save_path=save_path)  # 读取保存的模型

    train_logger.info('Testing...')

    batch_size = 128
    data_len = len(x_test)
    num_batch = int((data_len - 1) / batch_size) + 1

    y_pred_cls = np.zeros(shape=len(x_test), dtype=np.int32)  # 保存预测结果
    for i in range(num_batch):  # 逐批次处理
        start_id = i * batch_size
        end_id = min((i + 1) * batch_size, data_len)
        feed_dict = {
                model.input_x:   x_test[start_id:end_id],
                model.keep_prob: 1.0
        }
        y_pred_cls[start_id:end_id] = session.run(model.y_pred_cls, feed_dict=feed_dict)

    # 评估

    write_answer_str(y_test, y_pred_cls, answer_file)
    time_dif = get_time_dif(start_time)
    train_logger.info(f'Time usage: {time_dif.total_seconds() / 60} min')


def test():
    train_logger.info("Loading test data...")
    start_time = time.time()
    x_test, y_test = process_file(test_txt, word_to_id, cat_to_id, config.seq_length)

    session = tf.Session()
    session.run(tf.global_variables_initializer())
    saver = tf.train.Saver()
    saver.restore(sess=session, save_path=save_path)  # 读取保存的模型

    train_logger.info('Testing...')
    loss_test, acc_test = evaluate(session, x_test, y_test)
    msg = 'Test Loss: {0:>6.2}, Test Acc: {1:>7.2%}'
    train_logger.info(msg.format(loss_test, acc_test))

    batch_size = 128
    data_len = len(x_test)
    num_batch = int((data_len - 1) / batch_size) + 1

    y_test_cls = np.argmax(y_test, 1)

    y_pred_cls = np.zeros(shape=len(x_test), dtype=np.int32)  # 保存预测结果
    for i in range(num_batch):  # 逐批次处理
        start_id = i * batch_size
        end_id = min((i + 1) * batch_size, data_len)
        feed_dict = {
                model.input_x:   x_test[start_id:end_id],
                model.keep_prob: 1.0
        }
        y_pred_cls[start_id:end_id] = session.run(model.y_pred_cls, feed_dict=feed_dict)

    # 评估
    train_logger.info("Precision, Recall and F1-Score...")
    train_logger.info(metrics.classification_report(y_test_cls, y_pred_cls, target_names=categories))

    for index, y_pred_cls_item in enumerate(y_pred_cls):
        print(f' index is {index}, y_pred_cls_item is {y_pred_cls_item}, cat name is {categories[y_pred_cls_item]}')

    # 混淆矩阵
    train_logger.info("Confusion Matrix...")
    cm = metrics.confusion_matrix(y_test_cls, y_pred_cls)
    train_logger.info(cm)

    time_dif = get_time_dif(start_time)
    train_logger.info(f'Time usage: {time_dif.total_seconds() / 60} min')


def print_config_params(config):
    train_logger.info('config params :')
    train_logger.info(f'embedding_dim: {config.embedding_dim}')
    train_logger.info(f'seq_length: {config.seq_length}')
    train_logger.info(f'num_classes: {config.num_classes}')
    train_logger.info(f'num_filters: {config.num_filters}')
    train_logger.info(f'kernel_size: {config.kernel_size}')
    train_logger.info(f'kernel_size: {config.kernel_size}')
    train_logger.info(f'vocab_size: {config.vocab_size}')
    train_logger.info(f'batch_size: {config.batch_size}')
    train_logger.info(f'dropout_keep_prob: {config.dropout_keep_prob}')
    train_logger.info('########################################################')


if __name__ == '__main__':
    # if len(sys.argv) != 2 or sys.argv[1] not in ['train', 'test']:
    # raise ValueError("""usage: python run_cnn.py [train / test]""")

    train_logger = logger_factory.get_logger('train', True)
    train_logger.info('train time: {}'.format(datetime.now()))

    train_logger.info('Configuring CNN model...')
    config = TCNNConfig()
    print_config_params(config)
    if not os.path.exists(vocab_txt):  # 如果不存在词汇表，重建
        build_vocab(train_txt, vocab_txt, config.vocab_size)
    categories, cat_to_id = read_category(seged_clf_path)
    words, word_to_id = read_vocab(vocab_txt)
    config.vocab_size = len(words)
    model = TextCNN(config)
    # test()
    answer('/home/tqhy/ip_nlp/resources/questions/光电.txt', '/home/tqhy/ip_nlp/resources/answers/光电.txt')
    # answer('E:/ip_data/train/limit2500/test.txt')
    """if sys.argv[1] == 'train':
        train()
    else:
        test()"""
