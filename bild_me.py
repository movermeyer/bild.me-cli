#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from pprint import pprint
import requests


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
    f = open('test.jpg', 'rb')
    pprint(upload(f))

if __name__ == '__main__':
    main()
