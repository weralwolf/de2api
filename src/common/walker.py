__author__ = 'weralwolf'
import os
import re
from logger import log
from db import db


def check_dir(directory_list, file_type, root):
    queue = []
    for i in directory_list:
        if re.match('.*\.%s$' % file_type, i, flags=re.IGNORECASE):
            queue.append("%s/%s" % (root, i))
    return queue


def write_data_chunk(data, flag):
    try:
        session = db.session()
        log.debug('(%s) Adding `%s`' % (flag, data.filename))
        session.add(data)
        session.commit()
        session.close()

    except:
        log.error('Error adding file `%s`', data.filename)
        data.success = False
        data.clear_data()

        session = db.session()
        session.add(data)
        session.commit()
        session.close()


def walk(path, file_type, recursive, parser):
    queue = []

    if recursive:
        for root, dirs, files in os.walk(path, True, None, True):
            queue.extend(check_dir(files, file_type, root))
    else:
        files = os.listdir('.')
        queue.extend(check_dir(files, file_type, path))

    queue_len = len(queue)
    log.info('%i files collected for parsing...' % queue_len)

    data_index = 0
    for i in queue:
        data_index += 1
        write_data_chunk(parser.parse(i)[0], "%i/%i" % (data_index, queue_len))
