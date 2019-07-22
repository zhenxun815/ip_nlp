#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description: 
# @File: cnki_translation_words.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/22/2019 11:37

import os
import sys

ROOT_PATH = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(ROOT_PATH)

import requests
from bs4 import BeautifulSoup

from utils import file_utils

base_url = 'http://dict.cnki.net/'
max_page_num = 9999999
fail_pages = []


def get_html(url):
    try:
        print('get html url is {}'.format(url))
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        print('get html {} exception...'.format(url))
        fail_pages.append(url)
        return None


def get_word(html_page):
    if html_page:
        soup = BeautifulSoup(html_page, features='lxml')
        input_value = soup.find(id='txt2').attrs['value']
        print('input value is {}'.format(input_value))
        return input_value
    return None


def grab_words(max_page_num):
    for page_num in range(max_page_num):
        page_url = 'http://dict.cnki.net/h_%d000.html' % (page_num + 1)
        print('page num: {}'.format(page_num))
        html_page = get_html(page_url)
        word = get_word(html_page)
        if word:
            yield word


def grab_failed_page():
    while len(fail_pages) > 0:
        for fail_page_url in fail_pages[:]:
            fail_page_html = get_html(fail_page_url)
            word = get_word(fail_page_html)
            if word:
                fail_pages.remove(fail_page_url)
                yield word


def test():
    # html_page = get_html(base_url + 'h_5286500000.html')
    html_page = get_html('http://dict.cnki.net/h_9999999000.html')
    print('html page is:')
    print(html_page)
    soup = BeautifulSoup(html_page, features='lxml')
    input_value = soup.find(id='txt2').attrs['value']
    print('input value is {}'.format(len(input_value)))


if __name__ == '__main__':
    words = grab_words(max_page_num)
    file_utils.list2file(words, 'F:/temp/ip_nlp/cnki_trans.txt')

    if len(fail_pages) > 0:
        supply_words = grab_failed_page()
        file_utils.list2file(words, 'F:/temp/ip_nlp/cnki_trans.txt')
