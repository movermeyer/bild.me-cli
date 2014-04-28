#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from argparse import ArgumentParser
import json
from multiprocessing import Pool

import requests

__version__ = '0.1.0'


def parse_html(html):
    return html.splitlines()


def upload(f):
    url = 'http://www.bild.me/index.php'
    data = {
        't': 1,
        'C1': 'ON',
        'upload': 1,
    }
    files = {
        'F1': f
    }
    try:
        html = requests.post(url, data=data, files=files).text
        return {'status': 0, 'result': parse_html(html)}
    except requests.exceptions:
        return {'status': 1, 'message': 'Upload failed!'}


def get_result(args):
    img, list_all = args
    with open(img, 'rb') as f:
        result = upload(f)

        if result['status'] == 1:
            return result['message']
        if list_all:
            return '\n\n'.join(result['result'])
        else:
            return result['result'][5]


def main():
    parser = ArgumentParser(description='CLI tool for bild.me.')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-l', '--list', action='store_true',
                        help='list all result')
    parser.add_argument('-f', '-F', '--file', required=True,
                        nargs='+', help='picture file')
    args = parser.parse_args()
    files = set(args.file)

    # multiprocessing
    pool = Pool()
    results = pool.map(get_result, [(img, args.list) for img in files])
    pool.close()
    pool.join()

    return results

if __name__ == '__main__':
    for s in main():
        print s
