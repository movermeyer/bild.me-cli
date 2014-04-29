#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from argparse import ArgumentParser
from threading import Thread

import requests

from . import __version__


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


class UploadThread(Thread):
    def __init__(self, img, list_all, *args, **kwargs):
        self.img = img
        self.list_all = list_all
        super(UploadThread, self).__init__(*args, **kwargs)

    def run(self):
        with open(self.img, 'rb') as f:
            result = upload(f)

            if result['status'] == 1:
                print(result['message'])
            if self.list_all:
                print('\n\n'.join(result['result']))
            else:
                print(result['result'][5])


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
    list_all = args.list

    threads = []
    for img in files:
        t = UploadThread(img, list_all)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

if __name__ == '__main__':
    main()
