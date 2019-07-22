#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Description:
# @File: cnki_dict_words.py
# @Project: ip_nlp
# @Author: Yiheng
# @Email: GuoYiheng89@gmail.com
# @Time: 7/22/2019 9:27
import re

import requests
from bs4 import BeautifulSoup

from utils import file_utils

base_url = 'http://dict.cnki.net/'
catalogue_url = 'http://dict.cnki.net/dict_sub.aspx'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/71.0.3578.98 Safari/537.36'}


def get_html(url):
    try:
        print('get html url is {}'.format(url))
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        print('get html {} exception...'.format(url))
        return None


def get_categories_uri(html_text):
    soup = BeautifulSoup(html_text, features='lxml')
    filter_attrs = {'title': re.compile('.'),
                    'href':  re.compile('html$')}

    a_tags = soup.find_all('a', attrs=filter_attrs)
    hrefs = [a_tag['href'] for a_tag in a_tags]
    # for href in hrefs:
    #    print('href is {}'.format(href))
    return hrefs


def get_words_from_ctg(ctg_uris):
    for ctg_uri in ctg_uris:
        print('ctg uri is {}'.format(ctg_uri))
        ctg_pg0 = get_html(base_url + ctg_uri)

        page_count = get_page_count(ctg_pg0)
        for page_num in range(page_count):
            splits = ctg_uri.split('.')
            jump_uri = '%s_%d.html' % (splits[0], page_num + 1)
            ctg_page_uri = base_url + jump_uri
            ctg_page = get_html(ctg_page_uri)
            if ctg_page:
                yield get_words_from_ctg_page(ctg_page)


def get_page_count(ctg_pg0):
    soup = BeautifulSoup(ctg_pg0, features='lxml')
    page_info = soup.find('span', text=re.compile('^共.*')).text
    print('page info is {}'.format(page_info))
    # 共16页  共[306]词汇
    matcher = re.search('[0-9]+', page_info)

    return int(matcher.group(0)) if matcher else 0


def get_words_from_ctg_page(ctg_pg):
    soup = BeautifulSoup(ctg_pg, features='lxml')
    tr_tags = soup.find(id='lblcon').find_all('tr')
    words = [tr_tag.find_all('td')[1].a.text for tr_tag in tr_tags if not tr_tag.has_attr('class')]
    return words


if __name__ == '__main__':
    html = get_html(catalogue_url)
    # print('text {}'.format(html))
    ctg_uris = get_categories_uri(html)
    words = get_words_from_ctg(ctg_uris)
    dict_cnki_path = 'F:/temp/ip_nlp/cnki_dict.txt'
    for word in words:
        # print(word)
        file_utils.list2file(word, dict_cnki_path)
    print('all task complete...')
