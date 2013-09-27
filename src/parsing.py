'''
Created on Oct 16, 2012

@author: weralwolf
'''

# Common stuff for database developing
from sqlalchemy import Column, Integer, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base();


# Database Connector stuff
# >>>> 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_conf import db_conf

class DBConnection:
    __engine__ = None;
    def __init__(self, user, password, db_name, host='localhost', driver='mysql'):
        if (DBConnection.__engine__ == None):
            DBConnection.__engine__ = create_engine('%s://%s:%s@%s/%s' % (driver, user, password, host, db_name));

    def connection(self):
        return DBConnection.__engine__.connect(); 

    def execute(self, query):
        try:
            return self.connection().execute(query);
        except:
            return None;

    def session(self):
        Session = sessionmaker(bind=self.__engine__);
        return Session();

db = DBConnection(db_conf["user"], db_conf["password"], db_conf["database"], db_conf["host"], db_conf["driver"])

# <<<<

class TABLE_lang_500ms_v01(Base):
    __tablename__ = 'lang_500ms_v01';
    
    orbit = Column(Integer(10, unsigned=True));
    year = Column(Integer(3, unsigned=True), primary_key=True);
    day_of_year = Column(Integer(3, unsigned=True), primary_key=True);
    ut = Column(Integer(11, unsigned=True), primary_key=True);
    temp = Column(DECIMAL, default=None);
    np = Column(DECIMAL, default=None);
    potential = Column(DECIMAL, default=None);
    altitude = Column(DECIMAL, default=None);
    latitude = Column(DECIMAL, default=None);
    longitude = Column(DECIMAL, default=None);
    lst = Column(DECIMAL, default=None);
    lmt = Column(DECIMAL, default=None);
    l_sh = Column(DECIMAL, default=None);
    inv_lat = Column(DECIMAL, default=None);
    sza = Column(DECIMAL, default=None);
    
    def __repr__(self):
        return "<lang_500ms_v01: y: %i, d: %i, ut: %i>" % (self.year, self.day_of_year, self.ut);

"""
 1 - date       (I5)    [yyddd]
 2 - UT         (I9)    [ms]
 3 - Mode       (I2)            =3,4 measuring the horizontal velocity
                                =5,6 measuring the vertical velocity 
 4 - Slot       (I1)            =1,2,3,4; steps from 1 to 4 during each 8-sec 
                                measurement sequence, mode may change at each 
                                step.
 5 - Outin      (I1)            =1 baffle going out, =0 going in
 6 - Mass       (I3)    [AMU]   Usually 28 or 32 (32 is assume to be mostly 
                                atomic oxygen which is recombined in the 
                                instrument).
 7 - Density    (E12.5) [cm-3]  Density of neutrals with mass given in Word 6
                                (negative values should be ignored).
 8 - Tn         (F7.1)  [K]     Neutral temperature of neutral with mass given 
                                in word 6.
 9 - Tn_corr*   (F7.1)  [K]     Neutral temperature after WATSCOR correction. 
10 - V_s/c      (F8.1)  [m/s]   Horizontal (zonal) velocity (of neutrals with 
                                mass given in word 5) if Mode=3,4. Velocity is 
                                given in spacecraft spacecraft coordinates 
                                (positiv in the Z-axis direction).
                                Vertical velocity in s/c coordinates (positive 
                                in the Y axis direction) if Mode=5,6.
11 - C1**       (1X,I5)         (Instrument counts)/8
12 - C2         (I5)            (Counts + background)/8
13 - T1***      (1X,I3) [2s/255] Time when the baffle crosses the first optical 
                                position sensor. 
14 - T2***      (I3)    [2s/255] Time when the baffle crosses the second optical
                                position sensor.
15 - V_geo      (/F8.1) [m/s]   Horizontal/vertical (zonal) velocity in 
                                corotating Earth frame (positive in 
                                the eastward/upward direction) if 
                                mode=3,4/5,6.
16 - V_geo_cor* (F8.1)  [m/s]   Velocity (word 15) after WATSCOR 
                                correction*
17 - Orbit      (I6)            orbit number
18 - Altitude   (F7.1)  [km]
19 - Latitude   (F6.1)  [degree]  geographic latitude
20 - Longitude  (F7.1)  [degree]  geographic latitude
21 - LST        (F6.2)  [hours]   Local Solar Time
22 - LMT        (F6.2)  [hours]   Local Magnetic Time
23 - L          (F5.2)            McIllwain L value
24 - Inv. Lat.  (F6.1)  [degree]  Invariant latitude
25 - SZA        (F7.1)  [degree]  Solar Zenith Angle
"""

def lang_500ms_v01(filename):
    # reading data from currenct file
    data = open(filename, 'r').readlines();
    
    # creating database session for one file
    session = db.session();
    
    # removing 3 descriptive lines in the begining of file
    data.pop(0); data.pop(0); data.pop(0);
    
    for i in data:
        row = TABLE_lang_500ms_v01();
        row.orbit = i[0:6];
        row.year = '19' + i[7:9];
        row.day_of_year = i[9:12];
        row.ut = i[12:21];
        row.temp = i[21:28];
        row.np = i[28:38];
        row.potential = i[38:45];
        row.altitude = i[45:53];
        row.latitude = i[53:61];
        row.longitude = i[61:69];
        row.lst = i[69:75];
        row.lmt = i[75:81];
        row.l_sh = i[81:89];
        row.inv_lat = i[89:97];
        row.sza = i[97:106];
        
        session.add(row);
    
    session.commit();

import os
import re

def checkDir(listDir, fileType, root):
    queue = [];
    for i in listDir:
        if (re.match('.*\.%s$' % (fileType), i, flags=re.IGNORECASE)):
            queue.append("%s/%s" % (root, i));
    return queue;

def runInDir(path, fileType, recursive, parser):
    queue = [];
    if (recursive):
        for root, dirs, files in os.walk(path, True, None, True):
            queue.extend(checkDir(files, fileType, root));
    else:
        files = os.listdir('.');
        queue.extend(checkDir(files, fileType, root));
        
    print "%i files colleected for parsing..." % (len(queue));

    for i in queue:
        print "`%s` file..." % (str(i));
        parser(i);

    return;


if __name__ == '__main__':
    runInDir('/home/weralwolf/Workspace/SRI/de2/plasma_lang', 'asc', True, lang_500ms_v01);