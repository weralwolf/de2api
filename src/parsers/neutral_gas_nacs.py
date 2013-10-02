__author__ = 'weralwolf'
from models.source_data import NeutralGasNACSnT1s, SourceFile
from common.logger import log


class NT1s:
    def __init__(self):
        pass

    @staticmethod
    def parse_line(data_row, year, day_of_year):
        row = NeutralGasNACSnT1s()
        row.year = year
        row.day_of_year = day_of_year
        row.ut = int(data_row[0:9].strip())
        row.o_density = float(data_row[9:22].strip())
        row.o_density_err = float(data_row[22:29].strip())
        row.n2_density = float(data_row[29:42].strip())
        row.n2_density_err = float(data_row[42:49].strip())
        row.he_density = float(data_row[49:62].strip())
        row.he_density_err = float(data_row[62:69].strip())
        row.n_density = float(data_row[69:82].strip())
        row.n_density_err = float(data_row[82:89].strip())
        row.ar_density = float(data_row[89:102].strip())
        row.ar_density_err = float(data_row[102:109].strip())
        row.orbit = float(data_row[109:115].strip())
        row.alt = float(data_row[115:123].strip())
        row.lat = float(data_row[123:131].strip())
        row.long = float(data_row[131:139].strip())
        row.lst = float(data_row[139:145].strip())
        row.lmt = float(data_row[145:151].strip())
        row.l_sh = float(data_row[151:159].strip())
        row.inv_lat = float(data_row[159:167].strip())
        row.sza = float(data_row[167:].strip())
        return row

    @staticmethod
    def parse(datafile):
        # reading data from current file
        data = open(datafile, 'r').readlines()

        source = SourceFile(datafile)

        # removing 2 descriptive lines in the begin of file
        data.pop(0)
        data.pop(0)

        year = source.filename[0:4]
        day_of_year = source.filename[4:7]

        log.debug('<%i> %s' % (len(data), source.filename))
        for data_row in data:
            source.nt1s_data.append(NT1s.parse_line(data_row, year, day_of_year))

        return [source]
