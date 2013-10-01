__author__ = 'weralwolf'
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from conf import PROJECT_DIR, data_path

from os.path import abspath

Base = declarative_base()


class SourceFile(Base):
    __tablename__ = 'source_files'

    id = Column(Integer(11, unsigned=True), primary_key=True)
    filename = Column(String(256))
    filepath = Column(String(256))

    def __init__(self, path):
        filename = abspath(path)
        filepath = abspath(path)

        filename = filename.split('/').pop()
        filepath = filepath.replace(data_path, '').replace(filename, '').strip('/')

        self.filename = filename
        self.filepath = filepath


class PlasmaLangNeTe500Ms(Base):

    __tablename__ = 'plasma_lang_Ne_Te_500ms'

    id = Column(Integer(11, unsingned=True), primary_key=True)
    source_id = Column(Integer(11, unsigned=True), ForeignKey('source_files.id'))

    source = relationship('SourceFile', backref=backref('data', order_by=id))

    year = Column(Integer(3, unsigned=True))
    day_of_year = Column(Integer(3, unsigned=True))
    ut = Column(Integer(11, unsigned=True))
    orbit = Column(Integer(10, unsigned=True))
    temp = Column(Float, default=None)
    np = Column(Float, default=None)
    potential = Column(Float, default=None)
    altitude = Column(Float, default=None)
    latitude = Column(Float, default=None)
    longitude = Column(Float, default=None)
    lst = Column(Float, default=None)
    lmt = Column(Float, default=None)
    l_sh = Column(Float, default=None)
    inv_lat = Column(Float, default=None)
    sza = Column(Float, default=None)

    def __repr__(self):
        return "<lang_500ms_v01: y: %i, d: %i, ut: %i>" % (self.year, self.day_of_year, self.ut)