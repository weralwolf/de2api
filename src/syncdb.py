#!/usr/bin/python2.7
__author__ = 'weralwolf'

from common.db import *
from models.source_data import Base as source_data
from models.temporary_models import Base as temporary_models
from models.diffs import Base as diffs


def create_all():
    source_data.metadata.create_all(db.__engine__)
    temporary_models.metadata.create_all(db.__engine__)
    diffs.metadata.create_all(db.__engine__)

if __name__ == '__main__':
    create_all()
