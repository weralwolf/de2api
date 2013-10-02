__author__ = 'weralwolf'

if __name__ == '__main__':
    from common.db import *
    from models.source_data import *
    Base.metadata.create_all(db.__engine__)