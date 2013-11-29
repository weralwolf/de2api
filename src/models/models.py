__author__ = 'weralwolf'
from sqlalchemy import Table, Column, Integer, Float, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from conf import data_path
from os.path import abspath

Base = declarative_base()


class SourceFile(Base):
    __tablename__ = 'source_files'

    id = Column(Integer(11, unsigned=True), primary_key=True)
    filename = Column(String(256))
    filepath = Column(String(256))
    success = Column(Boolean, default=True)
    ignored = Column(Boolean, default=False)

    def __init__(self, path):
        filename = abspath(path)
        filepath = abspath(path)

        filename = filename.split('/').pop()
        filepath = filepath.replace(data_path, '').replace(filename, '').strip('/')

        self.filename = filename
        self.filepath = filepath

    def clear_data(self):
        self.nete500ms_data = []
        self.nt1s_data = []
        self.ntv2s_data = []


class PlasmaLangNeTe500Ms(Base):

    __tablename__ = 'plasma_lang_Ne_Te_500ms'

    id = Column(Integer(11, unsingned=True), primary_key=True)
    source_id = Column(Integer(11, unsigned=True), ForeignKey('source_files.id'))

    source = relationship('SourceFile', backref=backref('nete500ms_data', order_by=id))

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
        return "<%s: y: %i, d: %i, ut: %i>" % (self.__tablename__, self.year, self.day_of_year, self.ut)


class NeutralGasNACSnT1s(Base):
    __tablename__ = 'neutral_gas_nacs_n_t_1s'

    id = Column(Integer(11, unsigned=True), primary_key=True)
    source_id = Column(Integer(11, unsigned=True), ForeignKey('source_files.id'))
    source = relationship('SourceFile', backref=backref('nt1s_data', order_by=id))

    year = Column(Integer(3, unsigned=True))
    day_of_year = Column(Integer(3, unsigned=True))
    ut = Column(Integer(11, unsigned=True))
    orbit = Column(Integer(10, unsigned=True))
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
    alt = Column(Float, default=None)
    lat = Column(Float, default=None)
    long = Column(Float, default=None)
    lst = Column(Float, default=None)
    lmt = Column(Float, default=None)
    l_sh = Column(Float, default=None)
    inv_lat = Column(Float, default=None)
    sza = Column(Float, default=None)

    def __repr__(self):
        return "<%s: y: %i, d: %i, ut: %i>" % (self.__tablename__, self.year, self.day_of_year, self.ut)


class NeutralGasWATSnTv2s(Base):
    __tablename__ = 'neutral_gas_wats_n_t_v_2s'

    id = Column(Integer(11, unsigned=True), primary_key=True)
    source_id = Column(Integer(11, unsigned=True), ForeignKey('source_files.id'))
    source = relationship('SourceFile', backref=backref('ntv2s_data', order_by=id))

    year = Column(Integer(3, unsigned=True))
    day_of_year = Column(Integer(3, unsigned=True))
    ut = Column(Integer(11, unsigned=True))
    orbit = Column(Integer(10, unsigned=True))
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
    orbit = Column(Integer(10, unsigned=True))
    altitude = Column(Float, default=None)
    latitude = Column(Float, default=None)
    longitude = Column(Float, default=None)
    lst = Column(Float, default=None)
    lmt = Column(Float, default=None)
    l = Column(Float, default=None)
    inv_lat = Column(Float, default=None)
    sza = Column(Float, default=None)

    def __repr__(self):
      return "<%s: y: %i, d: %i, ut: %i>" % (self.__tablename__, self.year, self.day_of_year, self.ut)


class BasicReorderNACS(Base):
    __tablename__ = 'basic_reorder_nacs'

    id = Column(Integer(11, unsigned=True), primary_key=True)
    original_id = Column(Integer(11, unsigned=True))
    source_id = Column(Integer(11, unsigned=True))

    date_general = Column(DateTime())
    date_ms = Column(Integer(11, unsigned=True))
    date_original_year = Column(Integer(3, unsigned=True))
    date_original_day_of_year = Column(Integer(3, unsigned=True))
    date_original_ut = Column(Integer(11, unsigned=True))

    orbit = Column(Integer(10, unsigned=True))
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
    alt = Column(Float, default=None)
    lat = Column(Float, default=None)
    long = Column(Float, default=None)
    lst = Column(Float, default=None)
    lmt = Column(Float, default=None)
    l_sh = Column(Float, default=None)
    inv_lat = Column(Float, default=None)
    sza = Column(Float, default=None)

    def __repr__(self):
        return "<%s: y: %i, d: %i, ut: %i>" % (self.__tablename__, self.year, self.day_of_year, self.ut)


class BasicReorderWATS(Base):
    __tablename__ = 'basic_reorder_wats'

    id = Column(Integer(11, unsigned=True), primary_key=True)
    original_id = Column(Integer(11, unsigned=True))
    source_id = Column(Integer(11, unsigned=True))

    date_general = Column(DateTime())
    date_ms = Column(Integer(11, unsigned=True))
    date_original_year = Column(Integer(3, unsigned=True))
    date_original_day_of_year = Column(Integer(3, unsigned=True))
    date_original_ut = Column(Integer(11, unsigned=True))

    orbit = Column(Integer(10, unsigned=True))
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
    orbit = Column(Integer(10, unsigned=True))
    altitude = Column(Float, default=None)
    latitude = Column(Float, default=None)
    longitude = Column(Float, default=None)
    lst = Column(Float, default=None)
    lmt = Column(Float, default=None)
    l = Column(Float, default=None)
    inv_lat = Column(Float, default=None)
    sza = Column(Float, default=None)

    def __repr__(self):
      return "<%s: y: %i, d: %i, ut: %i>" % (self.__tablename__, self.year, self.day_of_year, self.ut)


class ShortDiffNACS(Base):
    __tablename__ = "short_diff_nacs"

    id = Column(Integer(11, unsigned=True), primary_key=True)

    first_original_id = Column(Integer(11, unsigned=True))
    first_source_id = Column(Integer(11, unsigned=True))

    second_original_id = Column(Integer(11, unsigned=True))
    second_source_id = Column(Integer(11, unsigned=True))

    time_diff = Column(Integer(11))


class ShortDiffWATS(Base):
    __tablename__ = "short_diff_wats"

    id = Column(Integer(11, unsigned=True), primary_key=True)

    first_original_id = Column(Integer(11, unsigned=True))
    first_source_id = Column(Integer(11, unsigned=True))

    second_original_id = Column(Integer(11, unsigned=True))
    second_source_id = Column(Integer(11, unsigned=True))

    time_diff = Column(Integer(11))

class MeasurementPoint(Base):
    """
    @QUESTION: what if alt, lat, etc. is different for nacs and wats?
    """
    __tablename__ = 'measurement_points'

    id = Column(Integer(11, unsigned=True), primary_key=True)
    datetime = Column(DateTime)

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

    def __repr__(self):
        return "<%s: date:%s, ut:%s>" % (self.__tablename__, str(self.datetime), str(self.ut))


class Measurement(Base):
    """
    @TODO: add units
    """
    __tablename__ = 'measurements'

    id = Column(Integer(11, unsigned=True), primary_key=True)
    measurement_point_id = Column(Integer(11, unsigned=True), ForeignKey('measurement_points.id'))
    measurement_point = relationship('MeasurementPoint', backref=backref('data', order_by=id))

    device = Column(String(255)) # here is suppose to be 3 values: nacs, wats, lang
    type = Column(String(255)) # here is a name on measurement: o.density, n2.density, etc.
    level = Column(Integer(2))

    value = Column(Float, default=None)
    error = Column(Float, default=None)
    correction = Column(Float, default=None)

    def __init__(self, *args, **kwargs):
        def from_kwargs(me, **kwargs):
            me.device = kwargs['device']
            me.type = kwargs['type']
            me.value = kwargs['value']
            me.error = kwargs.get('error', 0.)
            me.correction = kwargs.get('correction', 0.)
            me.level = kwargs.get('level', 1)

        def from_object(me, obj):
            me.device = obj.device
            me.type = obj.type
            me.value = obj.value
            me.error = obj.error
            me.correction = obj.correction
            me.level = obj.level

        if len(args):
            if isinstance(args[0], Measurement):
                from_object(self, args[0])
            else:
                raise ValueError
        else:
            from_kwargs(self, **kwargs)

    def __repr__(self):
        return "<%s: type:`%s`, value:%10.2f>" % (self.__tablename__, self.type, self.value)
