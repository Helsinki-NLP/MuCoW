# -*- coding: utf-8 -*-
# Code from the ContraWSD project: https://github.com/a-rios/ContraWSD

from __future__ import unicode_literals

import sys
import io
import json

infile = sys.argv[1]
srcpath = sys.argv[2]
target = sys.argv[3]

data = json.load(open(infile))

src = io.open(srcpath, 'w', encoding='UTF-8')
target = io.open(target, 'w', encoding='UTF-8')

for sentence in data:
    src.write(sentence['source'] + '\n')
    target.write(sentence['reference'] + '\n')

    for error in sentence['errors']:
        src.write(sentence['source'] + '\n')
        target.write(error['contrastive'] + '\n')
