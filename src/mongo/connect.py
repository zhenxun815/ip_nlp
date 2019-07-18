#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: connect.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/18/2019 10:49

from pymongo import MongoClient


class Connect:
    @staticmethod
    def get_connection():
        return MongoClient('mongodb://tqhy:tqhy817@192.168.1.205:27017/?authSource=admin')


def get_db(db_name):
    """
    connect to mongo and get the param specified db
    :param db_name: the db's name
    :return:
    """
    return Connect.get_connection().get_database(db_name)  # same with: client[db_name]


def get_collection(db_name, clc_name):
    """
    connect to mongo and get the param specified db's collection obj
    :param db_name:
    :param clc_name:
    :return:
    """
    db = get_db(db_name)
    return db.get_collection(clc_name)
