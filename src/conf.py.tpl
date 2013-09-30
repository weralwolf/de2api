__author__ = "weralwolf"
import os.path

db_conf = {
           "driver": "mysql",
           "host": "localhost",
           "user": "",
           "password": "",
           "database": "de2api"
}

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
data_path = PROJECT_DIR + '/../samples/'