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


def write_data_chunk(data):
    log.debug("Writing %i models..." % len(data))
    session = db.session()
    for row in data:
        try:
            log.debug('Adding `%s`' % row.filename)
            session.add(row)

        except:
            log.error('Error adding file `%s`', row.filename)
            row.success = False
            row.clear_data()

            #session = db.session()
            session.add(row)
            #session.commit()
            #session.close()
    log.debug("Commit short session...")
    session.commit()
    session.close()
    log.debug("Session commited.")


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

    parsed_data = []

    data_index = 0
    for i in queue:
        if len(parsed_data) > 5:
            log.debug("%i/%i files done" % (data_index, queue_len))
            write_data_chunk(parsed_data)
            del parsed_data
            parsed_data = []

        parsed_data.extend(parser.parse(i))
        data_index += 1

    if len(parsed_data):
        write_data_chunk(parsed_data)

