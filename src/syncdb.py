__author__ = 'weralwolf'
from common.db import *
from models.source_data import *

def create_all():
    Base.metadata.create_all(db.__engine__)

if __name__ == '__main__':
    create_all()