__author__ = 'weralwolf'
from sqlalchemy import Table, Column, Integer, Float, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship, backref, mapper
from sqlalchemy.ext.declarative import declarative_base
from conf import data_path
from os.path import abspath
from common import cache
from common.db import db

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


def __get_value_types():
    """
    Calculate types of measurements presented in database and preparing this information to be cached.
    """
    def translate(arg):
        return arg.replace('.', '_').replace(':', '__')

    s = db.session()
    query_data = s.query(Measurement.device, Measurement.type).group_by(Measurement.device).\
        group_by(Measurement.type).all()
    return [{'original': (i[0], i[1]), 'id': '%s:%s' % i, 'name': translate('%s:%s' % i)} for i in query_data]


class TimeDiff(Base):
    __tablename__ = 'diff_time'
    id = Column(Integer(11, unsigned=True), primary_key=True)
    id_1 = Column('id_1', Integer(11, unsigned=True), ForeignKey('measurement_points.id'))
    id_2 = Column('id_2', Integer(11, unsigned=True), ForeignKey('measurement_points.id'))
    diff = Column('diff', Float)
    diff_type = 'time'

    def __init__(self):
        pass


def declare_value_diff_tables():
    """
    Diff tables are main point of segments creation.

    Since segments are separated on families by configurations we couldn't calculate all of them in advance. To solve
    this problem we need to have calculated the most unified form of segments to make fast build any of the families
    on a fly.

    To make this process fasted we need to separate diffs measurement types by different tables to simplify lots of
    queries and cut time of query execution since we will have multiple joining.

    @todo: might be we need to create temporary tables before querying? Because even if we distinguish data by different
    tables while joining we would have multiplication of millions of data lines.
    """
    class DiffTable(type):
        def __new__(mcs, table_name, diff_type):
            class_name = str(''.join([i.capitalize() for i in table_name.split('_')]))

            return type(class_name, (Base, ), {
                '__tablename__': table_name,
                'id': Column('id', Integer(11, unsigned=True), primary_key=True),
                'id_1': Column('id_1', Integer(11, unsigned=True), ForeignKey('measurements.id')),
                'id_2': Column('id_2', Integer(11, unsigned=True), ForeignKey('measurements.id')),
                'diff': Column('diff', Float),
                'diff_type': diff_type
            })

    return {value_type['id']: {
        'table': DiffTable('diff_%s' % value_type['name'], value_type['id'])
    } for value_type in cache.get('value_types', __get_value_types)}


class SegmentationConfiguration(Base):
    """
    ``SegmentationConfiguration`` - is a segments family configuration. It represents single configuration for slicing.
    This configurations helps to work with processed sets of segments.
    """
    __tablename__ = 'segments_segmentation_configurations'
    id = Column(Integer(11, unsigned=True), primary_key=True)
    name = Column(String(255))


class SegmentationParameter(Base):
    """
    ``SegmentationParameter`` - is a parameters used by slicing algorithms.
    """
    __tablename__ = 'segments_segmentation_parameters'

    id = Column(Integer(11, unsigned=True), primary_key=True)
    configuration_id = Column(Integer(11, unsigned=True))
    configuration = relationship('SegmentationConfiguration', backref=backref('parameters', order_by=id))

    name = Column(String(60))
    value = Column(Float)

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return '<%s[%i: segment %i]: %s = %10.2f>' % (self.__tablename__, self.id, self.data_segment_id,
                                                      self.name, self.value)


class TimeSegment(Base):
    __tablename__ = "segments_time"

    id = Column(Integer(11, unsigned=True), primary_key=True)
    configuration_id = Column(Integer(11, unsigned=True), ForeignKey('segments_segmentation_configurations.id'))
    configuration = relationship('SegmentationConfiguration', backref=backref('segments', order_by=id))

    start = Column(Integer(11, unsigned=True))
    end = Column(Integer(11, unsigned=True))

    @property
    def segment_type(self):
        return 'time'

    def __init__(self, **kwargs):
        self.start = kwargs.get('start')
        self.end = kwargs.get('end')
        self.type = kwargs.get('type')

    def __repr__(self):
        return "<%s[%s]: (%i, %i)>" % (self.__tablename__, self.type, self.start, self.end)


segments_relation_time = Table('segments_relation_time', Base.metadata,
                               Column('segment_id', Integer, ForeignKey('segments_time.id')),
                               Column('point_id', Integer, ForeignKey('measurement_points.id')))


def declare_value_segments_table():
    class ValueTable(type):
        def __new__(mcs, table_name, value_id):
            class_name = str(''.join([i.capitalize() for i in table_name.split('_')]))

            return type(class_name, (Base, ), {
                '__tablename__': table_name,
                'id': Column('id', Integer(11, unsigned=True), primary_key=True),
                'configuration_id': Column('configuration_id', Integer(11, unsigned=True),
                                           ForeignKey('segments_segmentation_configurations.id')),
                'configuration': relationship('configuration', 'SegmentationConfiguration',
                                              backref=backref(table_name, order_by=id)),
                'start': Column('start', Integer(11, unsigned=True)),
                'end': Column('end', Integer(11, unsigned=True)),
                'segment_type': value_id
            })

    def relation_table(table_name, segments_table_name):
        return Table(table_name, Base.metadata,
                     Column('segment_id', Integer, ForeignKey(segments_table_name)),
                     Column('point_id', Integer, ForeignKey('measurements.id')))

    return {value_type['id']: {
        'table': ValueTable('segments_%s' % value_type['name'], value_type['id']),
        'relation': relation_table('segments_relation_%s' % value_type['name'], 'segments_%s.id' % value_type['name']),
    } for value_type in cache.get('value_types', __get_value_types)}

value_diff = declare_value_diff_tables()
value_segments = declare_value_segments_table()
