__author__ = 'weralwolf'

from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


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
