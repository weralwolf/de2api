__author__ = 'weralwolf'

from models import MeasurementPoint, Measurement, BasicReorderNACS, BasicReorderWATS
from common.db import db
from common.logger import log
from sqlalchemy.orm import joinedload


def __get_measurement_points(rows, do_search=True):
    def get_unique(original):
        result = []
        for i in original:
            if i not in result:
                result.append(i)
        return result

    def make_from_row(row):
        mp = MeasurementPoint()
        mp.ut = row.date_original_ut
        mp.datetime = row.date_general
        mp.year = row.date_original_year
        mp.day_of_year = row.date_original_year
        mp.orbit = row.orbit
        try:
            mp.alt = row.alt
            mp.lat = row.lat
            mp.long = row.long
            mp.l_sh = row.l_sh
        except AttributeError:
            mp.alt = row.altitude
            mp.lat = row.latitude
            mp.long = row.longitude
            mp.l_sh = row.l
        mp.lst = row.lst
        mp.lmt = row.lmt
        mp.inv_lat = row.inv_lat
        mp.sza = row.sza
        return mp

    def search(source, row):
        for i in source:
            if i.datetime == row.date_general:
                return i
        return make_from_row(row)

    __session = db.session()

    mps = []
    res = []
    if do_search:
        dates = get_unique([row.date_general for row in rows])
        res = __session.query(MeasurementPoint).options(joinedload('data')).\
            filter(MeasurementPoint.datetime.in_(dates)).order_by(MeasurementPoint.datetime).all()

    __session.close()

    log.info("Points to merge %i" % len(res))

    for row in rows:
        mp = search(res, row)
        if isinstance(row, BasicReorderNACS):
            mps.append(__nacs(mp, row))
        elif isinstance(row, BasicReorderWATS):
            mps.append(__wats(mp, row))
        else:
            log.error("Goes wrong with %s" % str(row))

    return mps


def __add_measurement(mp, params, general):
    params.update(general)
    mp.data.append(Measurement(**params))


def __nacs(mp, row):
    """
    @param row: BasicReorderNACS
    @return: MeasurementPoint with measurements belongs to it
    """
    general = {'device': 'nacs'}

    __add_measurement(mp, {
        'type': 'o.density',
        'value': row.o_density,
        'error': row.o_density_err
    }, general)
    __add_measurement(mp, {
        'type': 'n2.density',
        'value': row.n2_density,
        'error': row.n2_density_err
    }, general)
    __add_measurement(mp, {
        'type': 'he.density',
        'value': row.he_density,
        'error': row.he_density_err
    }, general)
    __add_measurement(mp, {
        'type': 'n.density',
        'value': row.n_density,
        'error': row.n_density_err
    }, general)
    __add_measurement(mp, {
        'type': 'ar.density',
        'value': row.ar_density,
        'error': row.ar_density_err
    }, general)

    return mp


def __wats(mp, row):
    """
    @param row: BasicReorderWATS
    @return: MeasurementPoint with measurements belongs to it
    """

    def mode(val):
        if val in (3, 4):
            return 'horizontal'
        elif val in (5, 6):
            return 'vertical'
        else:
            return 'unknown'

    general = {'device': 'wats'}

    __add_measurement(mp, {
        'type': 'mode',
        'value': row.mode,
    }, general)
    __add_measurement(mp, {
        'type': 'slot',
        'value': row.slot,
    }, general)
    __add_measurement(mp, {
        'type': 'outin',
        'value': row.outin,
    }, general)
    __add_measurement(mp, {
        'type': 'mass',
        'value': row.mass,
    }, general)
    __add_measurement(mp, {
        'type': 'density',
        'value': row.density,
    }, general)
    __add_measurement(mp, {
        'type': 'tn',
        'value': row.tn,
        'correction': row.tn_correction
    }, general)
    __add_measurement(mp, {
        'type': 'v_s.%s' % mode(row.mode),
        'value': row.v_s,
    }, general)
    __add_measurement(mp, {
        'type': 'c1',
        'value': row.c1,
    }, general)
    __add_measurement(mp, {
        'type': 'c2',
        'value': row.c2,
    }, general)
    __add_measurement(mp, {
        'type': 't1',
        'value': row.t1,
    }, general)
    __add_measurement(mp, {
        'type': 't2',
        'value': row.t2,
    }, general)
    __add_measurement(mp, {
        'type': 'v_geo.%s' % mode(row.mode),
        'value': row.v_geo,
        'correction': row.v_geo_correction
    }, general)

    return mp


def convert(data, do_search=True):
    if not len(data):
        return None

    return __get_measurement_points(data, do_search)
