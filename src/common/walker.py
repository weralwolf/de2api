__author__ = 'weralwolf'
import os
import re
from logger import log


def check_dir(directory_list, file_type, root):
    queue = []
    for i in directory_list:
        if re.match('.*\.%s$' % file_type, i, flags=re.IGNORECASE):
            queue.append("%s/%s" % (root, i))
    return queue


def walk(path, file_type, recursive, parser):
    queue = []

    if recursive:
        for root, dirs, files in os.walk(path, True, None, True):
            queue.extend(check_dir(files, file_type, root))
    else:
        files = os.listdir('.')
        queue.extend(check_dir(files, file_type, path))

    log.info('%i files collected for parsing...' % (len(queue)))

    parsed_data = []

    for i in queue:
        parsed_data.extend(parser.parse(i))

    return parsed_data
