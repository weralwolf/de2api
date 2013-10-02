#!/usr/bin/python2.7

__author__ = 'weralwolf'
from parsers.plasma_lang import NeTe500Ms
from parsers.neutral_gas_nacs import NT1s

if __name__ == '__main__':
    from walker import walk
    from conf import data_path
    data = []
    data.extend(walk('%s/plasma_lang/Ne_Te_500ms_ascii/' % data_path, 'asc', True, NeTe500Ms))
    data.extend(walk('%s/neutral_gas_nacs/n_T_1s_ascii/data/' % data_path, 'asc', True, NT1s))

    from db import db
    session = db.session()
    for row in data:
        session.add(row)

    session.commit()
    session.close()
