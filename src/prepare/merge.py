__author__ = 'weralwolf'

from models.temporary_models import BasicReorderWATS, BasicReorderNACS
from models.source_data import NeutralGasWATSnTv2s, NeutralGasNACSnT1s
from common.logger import log
from common.db import db

def reorder():
    """
    Reorder data to fit condition if id_1 < id_2 => ut_1 < ut_2
    """

    def filter_before():
        """
        Filter data before reordering to be able merge data
        Prefiltering suppose to expel data_files where we can find same ut time
        """
        log.info("Data prefiltering")

    def filter_after():
        """
        Filter data after reordering to be able merge data
        Have no idea what should be done here, but leave it in case
        """
        log.info("Data postfiltering")

    def make_order():
        """
        Making order after prefiltering of data
        """
        def prepare_fields(fields):
            return ', '.join(["`%s`" % field for field in fields])

        ordering_query = 'INSERT INTO `%(destination_table)s` (%(fields_insert)s) SELECT %(fields_select)s FROM ' +\
                         '`%(source_table)s` ORDER BY CONCAT(FROM_DAYS(TO_DAYS(CONCAT(`year`, "-01-01")) +' +\
                         ' `day_of_year` - 1), " ",  SEC_TO_TIME(`ut`/1000)) ASC;'

        nacs_select = ["id", "year", "day_of_year", "ut", "orbit", "o_density", "o_density_err",
                       "n2_density", "n2_density_err", "he_density", "he_density_err", "n_density",
                       "n_density_err", "ar_density", "ar_density_err", "alt", "lat", "long", "lst",
                       "lmt", "l_sh", "inv_lat", "sza"]

        nacs_insert = ["original_id", "year", "day_of_year", "ut", "orbit", "o_density", "o_density_err",
                       "n2_density", "n2_density_err", "he_density", "he_density_err", "n_density",
                       "n_density_err", "ar_density", "ar_density_err", "alt", "lat", "long", "lst",
                       "lmt", "l_sh", "inv_lat", "sza"]

        wats_select = ["id", "year", "day_of_year", "ut", "mode", "mode_horizontal", "slot",
                       "outin", "mass", "density", "tn", "tn_correction", "v_s", "c1", "c2", "t1", "t2",
                       "v_geo", "v_geo_correction", "orbit", "altitude", "latitude", "longitude", "lst",
                       "lmt", "l", "inv_lat", "sza"]

        wats_insert = ["original_id", "year", "day_of_year", "ut", "mode", "mode_horizontal", "slot",
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
    pass


def merge():
    """
    Merge data NACS and WATS together
    Question is about fitting NACS(with 1s resolution) to WATS(with 2s resolution) data
    """

    log.info("Merging data")