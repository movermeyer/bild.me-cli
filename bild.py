#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import json

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


def main():
    parser = ArgumentParser(description='CLI tool for bild.me.')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-l', '--list', action='store_true',
                        help='list all result')
    parser.add_argument('-f', '-F', '--file', required=True,
                        nargs='+', help='picture file')
    args = parser.parse_args()
    files = args.file

    for img in files:
        with open(img, 'rb') as f:
            result = upload(f)

            if result['status'] == 1:
                yield result['message']

            if args.list:
                yield '\n\n'.join(result['result'])
            else:
                yield result['result'][5]

if __name__ == '__main__':
    for s in main():
        print s
