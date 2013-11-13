__author__ = 'weralwolf'

from models.source_data import NeutralGasWATSnTv2s, SourceFile
from common.logger import log


class NTV2s:
    def __init__(self):
        pass

    @staticmethod
    def parse_line(data_row):
        row = NeutralGasWATSnTv2s()

        """ First data row structure
        (1X,I2)(I3)(I9)(I2)(I1)(I1)(I3)(E12.5)(F7.1)(F7.1)(F8.1)(1X,I5)(I5)(1X,I3)(I3)      |=74
        0:1:3:6:15:17:18:19:22:34:41:48:56:57:62:67:68:71:74
        """
        r0 = data_row[0]
        row.year = int('19' + r0[1:3].strip())
        row.day_of_year = int(r0[3:6].strip())
        row.ut = int(r0[6:15].strip())
        # 3,4 - horizontal; 5,6 - vertical velocity
        row.mode = int(r0[15:17].strip())
        row.mode_horizontal = row.mode in (3, 4)
        # 1,2,3,4; steps from 1 to 4 during each 8-sec. measurement sequence, mode may change at each step.
        row.slot = int(r0[17:18])
        # 1 baffle going out, =0 going in
        row.outin = int(r0[18:19])
        # [AMU] 	Usually 28 or 32 (32 is assume to be mostly atomic oxygen which is recombined in the instrument).
        row.mass = int(r0[19:22].strip())
        row.density = float(r0[22:34].strip())
        row.tn = float(r0[34:41].strip())
        row.tn_correction = float(r0[41:48].strip())
        row.v_s = float(r0[48:56].strip())
        row.c1 = int(r0[57:62].strip())
        row.c2 = int(r0[62:67].strip())
        row.t1 = int(r0[68:71].strip())
        row.t2 = int(r0[71:74].strip())

        """ Second data row structure
        (1X,F8.1)(F8.1)(I6)(F7.1)(F6.1)(F7.1)(F6.2)(F6.2)(F5.2)(F6.1)(F7.1)             |=73
        0:1:9:17:23:30:36:43:49:55:60:66:73
        """
        r1 = data_row[1]
        row.v_geo = float(r1[1:9].strip())
        row.v_geo_correction = float(r1[9:17].strip())
        row.orbit = int(r1[17:23].strip())
        row.altitude = float(r1[23:30].strip())
        row.latitude = float(r1[30:36].strip())
        row.longitude = float(r1[36:43].strip())
        row.lst = float(r1[43:49].strip())
        row.lmt = float(r1[49:55].strip())
        row.l = float(r1[55:60].strip())
        row.inv_lat = float(r1[60:66].strip())
        row.sza = float(r1[66:73].strip())
        return row

    @staticmethod
    def parse(datafile):
        # reading data from current file
        data_lines = open(datafile, 'r').readlines()
        data = []
        for i in range(0, len(data_lines) / 2):
            data.append((data_lines[2 * i], data_lines[2 * i + 1]))

        source = SourceFile(datafile)

        year = source.filename[0:4]
        day_of_year = source.filename[4:7]

        log.debug('<%i> %s' % (len(data), source.filename))
        for data_row in data:
            source.ntv2s_data.append(NTV2s.parse_line(data_row))

        return [source]
