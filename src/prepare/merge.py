__author__ = 'weralwolf'

from models.models import *
from common.logger import log
from common.db import db


def reorder():
    """
    Reorder data to fit condition if id_1 < id_2 => ut_1 < ut_2
    """
    class SQLCommand:
        def __init__(self, val):
            self.val = val

    def q(field_name):
        try:
            return field_name.val
        except AttributeError:
            return '`%s`' % field_name.replace('.', '`.`')

    def prepare_fields(fields):
        return ', '.join([q(field) for field in fields])

    def filter_before():
        """
        Filter data before reordering to be able merge data
        Prefiltering suppose to expel data_files where we can find same ut time
        """
        log.info("Data prefiltering")
        truncate = "TRUNCATE TABLE %(table_name)s"
        db.execute(truncate % {'table_name': ShortDiffNACS.__tablename__})
        db.execute(truncate % {'table_name': ShortDiffWATS.__tablename__})
        db.execute(truncate % {'table_name': BasicReorderNACS.__tablename__})
        db.execute(truncate % {'table_name': BasicReorderWATS.__tablename__})

    def filter_after():
        """
        Filter data after reordering to be able merge data
        Have no idea what should be done here, but leave it in case
        """

        ## Compute difference between timestamps
        diff_insert = ["first_original_id", "first_source_id", "second_original_id", "second_source_id", "time_diff"]
        diff_select = ["e1.original_id", "e1.source_id", "e2.original_id", "e2.source_id",
                       SQLCommand("TIME_TO_SEC(TIMEDIFF(%s, %s)) * 1000 + %s - %s" %
                       (q("e2.date_general"), q("e1.date_general"), q("e2.date_ms"), q("e1.date_ms")))]

        log.info("Data postfiltering")
        short_diff_maker = "INSERT INTO %(diff_destination)s (%(diff_insert)s) SELECT %(diff_select)s " + \
                           "FROM %(diff_source)s as `e2` JOIN %(diff_source)s as `e1` ON `e1`.`id` = `e2`.`id` - 1 " + \
                           " WHERE `e2`.`id` > 1;"

        db.execute(short_diff_maker % {
            'diff_destination': q(ShortDiffNACS.__tablename__),
            'diff_insert': prepare_fields(diff_insert),
            'diff_select': prepare_fields(diff_select),
            'diff_source': q(BasicReorderNACS.__tablename__)
        })

        db.execute(short_diff_maker % {
            'diff_destination': q(ShortDiffWATS.__tablename__),
            'diff_insert': prepare_fields(diff_insert),
            'diff_select': prepare_fields(diff_select),
            'diff_source': q(BasicReorderWATS.__tablename__)
        })

        ## Select zero-diff elements
        fetcher = "SELECT `first_source_id`, `second_source_id` FROM  %(table_name)s WHERE `time_diff` = 0;"
        source = []
        for i in db.execute(fetcher % {'table_name': ShortDiffNACS.__tablename__}).fetchall():
            source.extend([str(i[0]), str(i[1])])
        for i in db.execute(fetcher % {'table_name': ShortDiffWATS.__tablename__}).fetchall():
            source.extend([str(i[0]), str(i[1])])

        source_ids = []
        for i in source:
            if i not in source_ids:
                source_ids.append(i)

        ## Mark files
        if len(source_ids) > 0:
            db.execute("UPDATE `source_files` SET `ignored`=1 WHERE id IN (%s)" % (', '.join(source_ids)))

    def make_order():
        """
        Making order after prefiltering of data
        """
        ordering_query = 'INSERT INTO `%(destination_table)s` (%(fields_insert)s) SELECT %(fields_select)s FROM ' + \
                         '`%(source_table)s` as `st` JOIN `source_files` as `sf` ON `st`.`source_id`=`sf`.`id` ' + \
                         'WHERE `sf`.`ignored`=0 ORDER BY DATE_ADD(CONCAT(FROM_DAYS(TO_DAYS(CONCAT(`year`, ' + \
                         '"-01-01")) + `day_of_year` - 1), " 00:00:00"), INTERVAL ut/1000 SECOND_MICROSECOND) ASC;'

        nacs_select = ["st.id", "source_id",
                       SQLCommand("DATE_ADD(CONCAT(FROM_DAYS(TO_DAYS(CONCAT(`year`, '-01-01')) + "
                                  "`day_of_year` - 1), ' 00:00:00'), INTERVAL ut/1000 SECOND_MICROSECOND)"),
                       SQLCommand("`ut` %% 1000"),
                       "year", "day_of_year", "ut", "orbit", "o_density", "o_density_err",
                       "n2_density", "n2_density_err", "he_density", "he_density_err", "n_density",
                       "n_density_err", "ar_density", "ar_density_err", "alt", "lat", "long", "lst",
                       "lmt", "l_sh", "inv_lat", "sza"]

        nacs_insert = ["original_id", "source_id", "date_general", "date_ms", "date_original_year",
                       "date_original_day_of_year", "date_original_ut", "orbit", "o_density", "o_density_err",
                       "n2_density", "n2_density_err", "he_density", "he_density_err", "n_density",
                       "n_density_err", "ar_density", "ar_density_err", "alt", "lat", "long", "lst",
                       "lmt", "l_sh", "inv_lat", "sza"]

        wats_select = ["st.id", "source_id",
                       SQLCommand("DATE_ADD(CONCAT(FROM_DAYS(TO_DAYS(CONCAT(`year`, '-01-01')) + "
                                  "`day_of_year` - 1), ' 00:00:00'), INTERVAL ut/1000 SECOND_MICROSECOND)"),
                       SQLCommand("`ut` %% 1000"),
                       "year", "day_of_year", "ut", "mode", "mode_horizontal", "slot",
                       "outin", "mass", "density", "tn", "tn_correction", "v_s", "c1", "c2", "t1", "t2",
                       "v_geo", "v_geo_correction", "orbit", "altitude", "latitude", "longitude", "lst",
                       "lmt", "l", "inv_lat", "sza"]

        wats_insert = ["original_id", "source_id", "date_general", "date_ms", "date_original_year",
                       "date_original_day_of_year", "date_original_ut", "mode", "mode_horizontal", "slot",
                       "outin", "mass", "density", "tn", "tn_correction", "v_s", "c1", "c2", "t1", "t2",
                       "v_geo", "v_geo_correction", "orbit", "altitude", "latitude", "longitude", "lst",
                       "lmt", "l", "inv_lat", "sza"]

        db.execute(ordering_query %
                   {
                       'destination_table': BasicReorderNACS.__tablename__,
                       'source_table': NeutralGasNACSnT1s.__tablename__,
                       'fields_insert': prepare_fields(nacs_insert),
                       'fields_select': prepare_fields(nacs_select)
                   })
        db.execute(ordering_query %
                   {
                       'destination_table': BasicReorderWATS.__tablename__,
                       'source_table': NeutralGasWATSnTv2s.__tablename__,
                       'fields_insert': prepare_fields(wats_insert),
                       'fields_select': prepare_fields(wats_select)
                   })
        log.info("Making order in satellite data")

    filter_before()
    make_order()
    filter_after()
    filter_before()
    make_order()

from models.convert import convert


def merge():
    """
    Merge data NACS and WATS together
    Question is about fitting NACS(with 1s resolution) to WATS(with 2s resolution) data
    """
    def make_conversion(data_type, chunk_size):
        s = db.session()
        count = s.query(data_type).count()
        log.info("%i elements to be converted" % count)
        iterations = count / chunk_size
        if count % chunk_size:
            iterations += 1
        for i in range(0, iterations):
            for row in s.query(data_type).slice(i * chunk_size, (i + 1) * chunk_size - 1).all():
                s.add(convert(row))
            s.commit()
        s.close()

    chunk_size = 100
    make_conversion(BasicReorderNACS, chunk_size)
    make_conversion(BasicReorderWATS, chunk_size)

    log.info("Merging data")


def resampling():
    """
    NACS data resampling from 1s to 2s due to wats data.
    Might be it's more logical would be to find out wats
    """
    def get_new(mp1, mp2=None):
        def find_model(mp, type, level=1, device='nacs'):
            for i in mp.data:
                if i.type==type and i.type==level and i.device==device:
                    return i
            return None

        update = []

        if not mp2 or (mp1.datetime.python_type() - mp2.datetime.python_type()).seconds > 3:
            if not mp2:
                log.debug("[wats:%i:%s] edge point does not exists" % (mp1.id, str(mp1.datetime)))
            else:
                log.debug("[wats:%i:%s]&[wats:%i:%s] is to fas in time dimension" %
                          (mp1.id, str(mp1.datetime), mp2.id, str(mp2.datetime)))
            for measurement in mp1.data:
                if measurement.device == 'nacs':
                    nm = Measurement(measurement)
                    nm.level = 2
                    update.append(nm)
        else:
            log.debug("[wats:%i:%s]&[wats:%i:%s] is goes to be resampled" %
                      (mp1.id, str(mp1.datetime), mp2.id, str(mp2.datetime)))
            for measurement in mp1.data:
                ms = find_model(mp2, mp1.type)
                nm = Measurement(measurement)
                nm.level = 2
                nm.value = (nm.value + ms.value) / 2
                nm.error = (nm.error + ms.error) / 2
                nm.correction = (nm.correction + ms.correction) / 2
                update.append(nm)
        mp1.data.extend(update)
        return mp1


    s = db.session()
    ids_ = s.query(Measurement.measurement_point_id).filter(Measurement.device=='wats').all()
    ids = []
    for i in ids_:
        if i[0] not in ids:
            ids.append(i[0])
    chunk_size = 100
    iterations = [ids[i*chunk_size:(i+1)*chunk_size] for i in range(0, len(ids)/chunk_size)]
    log.info("WATS data in %i elements going to be processed in %i iterations" % (len(ids), len(iterations)))
    for points in iterations:
        log.info("Processing ids in range %s" % str(points))
        extended_points = points
        extended_points.extend([j-1 for j in points])
        data = s.query(MeasurementPoint).join(Measurement).\
            filter(Measurement.type=='nacs').filter(MeasurementPoint.id.in_(extended_points)).\
            order_by(Measurement.measurement_point_id).order_by(Measurement.type).all()
        data = {row.id: row for row in data}
        for key, row in data:
            if key in points:
                s.add(get_new(row, data.get(key-1, None)))
        s.commit()

