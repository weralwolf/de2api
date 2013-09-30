__author__ = 'weralwolf'
from sqlalchemy import Column, Integer, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PlasmaLangNeTe500Ms(Base):

    __tablename__ = 'plasma_lang_Ne_Te_500ms'

    year = Column(Integer(3, unsigned=True), primary_key=True)
    day_of_year = Column(Integer(3, unsigned=True), primary_key=True)
    ut = Column(Integer(11, unsigned=True), primary_key=True)

    orbit = Column(Integer(10, unsigned=True))
    temp = Column(DECIMAL, default=None)
    np = Column(DECIMAL, default=None)
    potential = Column(DECIMAL, default=None)
    altitude = Column(DECIMAL, default=None)
    latitude = Column(DECIMAL, default=None)
    longitude = Column(DECIMAL, default=None)
    lst = Column(DECIMAL, default=None)
    lmt = Column(DECIMAL, default=None)
    l_sh = Column(DECIMAL, default=None)
    inv_lat = Column(DECIMAL, default=None)
    sza = Column(DECIMAL, default=None)

    def __repr__(self):
        return "<lang_500ms_v01: y: %i, d: %i, ut: %i>" % (self.year, self.day_of_year, self.ut)