__author__ = 'weralwolf'

import logging
from conf import logger as conf

log = logging.getLogger('de2api')
log.setLevel(conf['level'])

if conf['file']['enable']:
    # create file handler which logs even debug messages
    fh = logging.FileHandler('%s/%s' % (conf['file']['path'], conf['file']['filename']))
    fh.setLevel(conf['file']['level'])

    # create formatter and add it to the handlers
    fh.setFormatter(logging.Formatter(conf['file']['formatter']))
    log.addHandler(fh)


if conf['console']['enable']:
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(conf['console']['level'])

    # create formatter and add it to the handlers
    ch.setFormatter(logging.Formatter(conf['console']['formatter']))
    # add the handlers to the logger
    log.addHandler(ch)
