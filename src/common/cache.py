__author__ = 'weralwolf'

from common.logger import log
from conf import cache_path
import json


def get(cache_name, cache_renew):
    json_cache = '%s/%s.json' % (cache_path, cache_name)
    try:
        return json.load(open(json_cache, 'r'))
    except (IOError, ValueError) as e:
        log.error("Unpacking 'value_types.json' raise exception:\n %s" % str(e))

        value_names = cache_renew()
        json.dump(value_names, open(json_cache, 'w'))
        return value_names
