__author__ = 'weralwolf'
from models.source_data import PlasmaLangNeTe500Ms


class NeTe500Ms:
    def __init__(self):
        pass

    @staticmethod
    def parse_line(data_row):
        row = PlasmaLangNeTe500Ms()
        row.orbit = data_row[0:6]
        row.year = '19' + data_row[7:9]
        row.day_of_year = data_row[9:12]
        row.ut = data_row[12:21]
        row.temp = data_row[21:28]
        row.np = data_row[28:38]
        row.potential = data_row[38:45]
        row.altitude = data_row[45:53]
        row.latitude = data_row[53:61]
        row.longitude = data_row[61:69]
        row.lst = data_row[69:75]
        row.lmt = data_row[75:81]
        row.l_sh = data_row[81:89]
        row.inv_lat = data_row[89:97]
        row.sza = data_row[97:106]
        return row

    @staticmethod
    def parse(datafile):
        # reading data from current file
        data = open(datafile, 'r').readlines()

        # removing 3 descriptive lines in the begin of file
        data.pop(0)
        data.pop(0)
        data.pop(0)

        data_rows = []

        for data_row in data:
            data_rows.append(NeTe500Ms.parse_line(data_row))

        return data_rows