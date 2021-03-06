#!/usr/bin/python2.7
__author__ = 'weralwolf'

from conf import data_path

from common.db import db
from common.logger import log
from common.walker import walk

from parsers.plasma_lang import NeTe500Ms
from parsers.neutral_gas_nacs import NT1s
from parsers.neutral_gas_wats import NTV2s


def parse_all():
    log.info('Parsing `plasma lang`')
    walk('%s/plasma_lang/Ne_Te_500ms_ascii/' % data_path, 'asc', True, NeTe500Ms)
    log.info('Parsing `neutral gas nacs`')
    walk('%s/neutral_gas_nacs/n_T_1s_ascii/data/' % data_path, 'asc', True, NT1s)
    log.info('Parsing `neutral gas wats`')
    walk('%s/neutral_gas_wats/n_T_v_2s_ascii/' % data_path, 'asc', True, NTV2s)
    log.info('DONE')

if __name__ == '__main__':
    from syncdb import create_all

    create_all()
    parse_all()