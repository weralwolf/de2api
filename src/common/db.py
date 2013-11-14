#!/usr/bin/python2.7

__author__ = 'weralwolf'
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from conf import db_conf
from common.logger import log


class DBConnection:
    __engine__ = None

    def __init__(self, user, password, db_name, host='localhost', driver='mysql'):
        if not DBConnection.__engine__:
            DBConnection.__engine__ = create_engine('%s://%s:%s@%s/%s' % (driver, user, password, host, db_name))

    @staticmethod
    def connection():
        return DBConnection.__engine__.connect()

    @staticmethod
    def execute(query):
        try:
            log.info("Execute query: %s" % (str(query)))
            return DBConnection.connection().execute(query)
        except Exception, exc:
            log.error("db.execute: %(error)s" % {'error': exc.message})
            return None

    @staticmethod
    def session():
        Session = sessionmaker(bind=DBConnection.__engine__)
        return Session()

db = DBConnection(db_conf["user"], db_conf["password"], db_conf["database"], db_conf["host"], db_conf["driver"])
