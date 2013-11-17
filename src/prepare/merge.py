__author__ = 'weralwolf'

from models.temporary_models import BasicReorderWATS, BasicReorderNACS
from models.source_data import NeutralGasWATSnTv2s, NeutralGasNACSnT1s
from models.diffs import ShortDiffNACS, ShortDiffWATS
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
                         'WHERE `sf`.`ignored`=0 ORDER BY CONCAT(FROM_DAYS(TO_DAYS(CONCAT(`year`, "-01-01")) + ' + \
                         '`day_of_year` - 1), " ",  SEC_TO_TIME(`ut`/1000)) ASC;'

        nacs_select = ["st.id", "source_id",
                       SQLCommand("CONCAT(FROM_DAYS(TO_DAYS(CONCAT(`year`, '-01-01')) + `day_of_year` - 1), ' '" +
                                  ",  SEC_TO_TIME(`ut`/ 1000))"), SQLCommand("`ut` %% 1000"),
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
                       SQLCommand("CONCAT(FROM_DAYS(TO_DAYS(CONCAT(`year`, '-01-01')) + `day_of_year` - 1), ' '" +
                                  ",  SEC_TO_TIME(`ut`/ 1000))"), SQLCommand("`ut` %% 1000"),
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


def merge():
    """
    Merge data NACS and WATS together
    Question is about fitting NACS(with 1s resolution) to WATS(with 2s resolution) data
    """

    log.info("Merging data")