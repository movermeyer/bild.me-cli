#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from scripttest import TestFileEnvironment

current_dir = os.path.dirname(__file__)


def test_cli():
    env = TestFileEnvironment('./test-output')
    img1 = os.path.join(current_dir, 'test1.png')
    img2 = os.path.join(current_dir, 'test2.png')

    res = env.run('bild', '-f', img1)
    assert re.findall(r'http://s1.bild.me/bilder/\d+/\d+.*', res.stdout)

    res = env.run('bild', '-f', img1, img2)
    assert len(re.findall(r'http://s1.bild.me/bilder/\d+/\d+.*', res.stdout)) == 2

    res = env.run('bild', '-lf', img1)
    assert re.findall(r'http://s1.bild.me/bilder/\d+/\d+.*', res.stdout)
    assert '[URL=http://www.bild.me][IMG]' in res.stdout

    res = env.run('bild', '-lf', img1, img2)
    assert re.findall(r'http://s1.bild.me/bilder/\d+/\d+.*', res.stdout)
    assert len(re.findall(r'\[URL=http://www.bild.me\]\[IMG\]', res.stdout)) == 2
