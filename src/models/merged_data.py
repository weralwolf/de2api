__author__ = 'weralwolf'

from sqlalchemy import Column, Integer, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

"""
Questions I need to find answer:
1. What data is a main data, support data
2. What calculations on a date I need to do
"""


class MeasurementPoint(Base):
    __tablename__ = 'measurement_point'

    id = Column(Integer(11, unsigned=True), primary_key=True)

    year = Column(Integer(3, unsigned=True))
    day_of_year = Column(Integer(3, unsigned=True))
    ut = Column(Integer(11, unsigned=True))
    orbit = Column(Integer(10, unsigned=True))
    alt = Column(Float, default=None)
    lat = Column(Float, default=None)
    long = Column(Float, default=None)
    lst = Column(Float, default=None)
    lmt = Column(Float, default=None)
    l_sh = Column(Float, default=None)
    inv_lat = Column(Float, default=None)
    sza = Column(Float, default=None)


class NACS(Base):
    __tablename__ = 'neutral_gas_nacs_n_t_1s'

    id = Column(Integer(11, unsigned=True), primary_key=True)

    o_density = Column(Float, default=None)
    o_density_err = Column(Float, default=None)
    n2_density = Column(Float, default=None)
    n2_density_err = Column(Float, default=None)
    he_density = Column(Float, default=None)
    he_density_err = Column(Float, default=None)
    n_density = Column(Float, default=None)
    n_density_err = Column(Float, default=None)
    ar_density = Column(Float, default=None)
    ar_density_err = Column(Float, default=None)

    def __repr__(self):
      return "<%s: y: %i, d: %i, ut: %i>" % (self.__tablename__, self.year, self.day_of_year, self.ut)


class WATS(Base):
    __tablename__ = 'merged_wats'

    id = Column(Integer(11, unsigned=True), primary_key=True)

    mode = Column(Integer(1, unsigned=True))
    mode_horizontal = Column(Boolean())
    slot = Column(Integer(3, unsigned=True))
    outin = Column(Integer(3, unsigned=True))
    mass = Column(Integer(5, unsigned=True))
    density = Column(Float, default=None)
    tn = Column(Float, default=None)
    tn_correction = Column(Float, default=None)
    v_s = Column(Float, default=None)
    c1 = Column(Integer(10, unsigned=True))
    c2 = Column(Integer(10, unsigned=True))
    t1 = Column(Integer(10, unsigned=True))
    t2 = Column(Integer(10, unsigned=True))
    v_geo = Column(Float, default=None)
    v_geo_correction = Column(Float, default=None)

    def __repr__(self):
      return "<%s: y: %i, d: %i, ut: %i>" % (self.__tablename__, self.year, self.day_of_year, self.ut)