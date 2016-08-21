#!/usr/bin/env python

""" make dirs and files human readable

scp root@your_phone:/data/data/com.app_name/databases/asdb.db ./
scp -r root@your_phone:/data/data/com.app_name/files/clips/* ./

./renamer.py
"""

import os
import re
import sqlite3
import json
from hashlib import md5


def get_name(node):
    """ returns {md5sum: 'readable_name'}  """

    key = md5(node['name']).hexdigest()
    return {key: node['name']}

CURSOR = sqlite3.connect('asdb.db').cursor()
CURSOR.execute("select response from GetCourseSave")
RESP = CURSOR.fetchall()

names = {}

for (item,) in RESP:
    item = json.loads(item)
    names.update(get_name(item))

    for m in item['modules']:
        names.update(get_name(m))

        for clip in m['clips']:
            names.update(get_name(clip))

PATTERN = re.compile('|'.join(names.keys()))

for root, dirs, files in os.walk('.'):
    for f in files:
        old = os.path.join(root, f)
        new = PATTERN.sub(lambda x: names[x.group()], old)

        if old != new:
            os.renames(old, new)
