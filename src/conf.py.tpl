__author__ = 'weralwolf'
from os.path import abspath, dirname
import logging

db_conf = {
           'driver': 'mysql',
           'host': 'localhost',
           'user': '',
           'password': '',
           'database': 'de2api'
}

PROJECT_DIR = abspath(dirname(__file__))
data_path = abspath(PROJECT_DIR + '/../samples/')
cache_path = abspath(PROJECT_DIR + '/../cache/')

logger = {
    'file': {
        'enable': True,
        'level': logging.DEBUG,
        'formatter': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',

        'path': abspath(PROJECT_DIR + '/../logs/'),
        'filename': 'de2api.log',
    },

    'console': {
        'enable': True,
        'level': logging.DEBUG, #logging.ERROR,
        'formatter': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    },

    'level': logging.DEBUG,

}