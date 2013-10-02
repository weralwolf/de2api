__author__ = 'weralwolf'
from models.source_data import PlasmaLangNeTe500Ms, SourceFile
from common.logger import log


class NeTe500Ms:
    def __init__(self):
        pass

    @staticmethod
    def parse_line(data_row):
        row = PlasmaLangNeTe500Ms()
        row.orbit = int(data_row[0:7].strip())
        row.year = int('19' + data_row[7:9].strip())
        row.day_of_year = int(data_row[9:12].strip())
        row.ut = int(data_row[12:21].strip())
        row.temp = float(data_row[21:28].strip())
        row.np = float(data_row[28:38].strip())
        row.potential = float(data_row[38:45].strip())
        row.altitude = float(data_row[45:53].strip())
        row.latitude = float(data_row[53:61].strip())
        row.longitude = float(data_row[61:69].strip())
        row.lst = float(data_row[69:75].strip())
        row.lmt = float(data_row[75:81].strip())
        row.l_sh = float(data_row[81:89].strip())
        row.inv_lat = float(data_row[89:97].strip())
        row.sza = float(data_row[97:].strip())
        return row

    @staticmethod
    def parse(datafile):
        # reading data from current file
        data = open(datafile, 'r').readlines()

        source = SourceFile(datafile)

        # removing 3 descriptive lines in the begin of file
        data.pop(0)
        data.pop(0)
        data.pop(0)

        log.debug('<%i> %s' % (len(data), source.filename))
        for data_row in data:
            source.nete500ms_data.append(NeTe500Ms.parse_line(data_row))

        return [source]
