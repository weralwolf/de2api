#!/usr/bin/python2.7

__author__ = 'weralwolf'
from parsers.plasma_lang import NeTe500Ms

if __name__ == '__main__':
    from walker import walk
    from conf import data_path
    data = walk('%s/plasma_lang/Ne_Te_500ms_ascii/' % data_path, 'asc', True, NeTe500Ms)

    from db import db
    session = db.session()
    for row in data:
        session.add(row)

    session.commit()
    session.close()
