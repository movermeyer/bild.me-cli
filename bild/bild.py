#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from argparse import ArgumentParser
from threading import Thread
from time import sleep
import sys

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
    except Exception as e:
        return {'status': 1, 'message': e}


class ProgressBar(object):
    def __init__(self, list_all):
        self.progress = {}
        self.list_all = list_all

    def run(self):
        f = sys.stdout

        for (k, p) in self.progress.items():
            for x in range(1, 50):
                if p['finish']:
                    x = 50
                s = '{0}: [{1}]'.format(k, ('=' * x + '>').ljust(50, '-'))
                f.write(s)
                f.flush()
                f.write('\r')

                if x != 50:
                    sleep(0.3)
                else:
                    break
            f.write('\n')
            if p['finish']:
                result = p['result']
                if result['status'] == 1:
                    sys.stderr.write(result['message'] + '\n')
                if self.list_all:
                    print('\n\n'.join(result['result']))
                else:
                    print(result['result'][5])


class UploadThread(Thread):
    def __init__(self, img, bar, *args, **kwargs):
        self.img = img
        self.bar = bar
        super(UploadThread, self).__init__(*args, **kwargs)

    def run(self):
        with open(self.img, 'rb') as f:
            self.bar.progress[f.name] = {'finish': False}
            result = upload(f)
            self.bar.progress[f.name]['finish'] = True
            self.bar.progress[f.name]['result'] = result


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
    bar = ProgressBar(list_all)

    for n, img in enumerate(files):
        t = UploadThread(img, bar)
        t.start()

    sleep(0.2)
    bar.run()

if __name__ == '__main__':
    main()
