#!/usr/bin/python2.7
__author__ = 'weralwolf'

from common.db import *
from models.source_data import *
from models.temporary_models import *

def create_all():
    Base.metadata.create_all(db.__engine__)

if __name__ == '__main__':
    create_all()