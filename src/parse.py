#!/usr/bin/python2.7
__author__ = 'weralwolf'

if __name__ == '__main__':
    from common.db import db
    from common.logger import log
    from parsers.plasma_lang import NeTe500Ms
    from parsers.neutral_gas_nacs import NT1s

    from common.walker import walk
    from conf import data_path
    data = []
    log.info('Parsing `plasma lang`')
    data.extend(walk('%s/plasma_lang/Ne_Te_500ms_ascii/' % data_path, 'asc', True, NeTe500Ms))
    log.info('Parsing `neutral gas nacs`')
    data.extend(walk('%s/neutral_gas_nacs/n_T_1s_ascii/data/' % data_path, 'asc', True, NT1s))

    session = db.session()
    for row in data:
        session.add(row)

    session.commit()
    session.close()
