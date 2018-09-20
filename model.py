from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()

class Profile(Base):
  __tablename__ = 'profile'

  id = Column(Integer, primary_key=True)
  name = Column(String, unique=True)
  created_date = Column(String)
  modified_date = Column(String)
  goals = relationship('Goal', back_populates='profile')

class Goal(Base):
  __tablename__ = 'goal'

  id = Column(Integer, primary_key=True)
  profile_id = Column(Integer, ForeignKey('profile.id'))
  profile = relationship('Profile', back_populates='goals')
  start_date = Column(String)
  end_date = Column(String)
  _words = Column(String)
  period = Column(String)
  number = Column(Integer)
  checkins = relationship('Checkin', back_populates='goal')

  @hybrid_property
  def words(self):
    return self._words.split(',')
  @words.setter
  def words(self, words):
    self._words = ','.join(words)

class Checkin(Base):
  __tablename__ = 'checkin'

  id = Column(Integer, primary_key=True)
  goal_id = Column(Integer, ForeignKey('goal.id'))
  goal = relationship('Goal', back_populates='checkins')
  date = Column(String)
  number = Column(Integer)
  __table_args__ = (UniqueConstraint('goal_id', 'date'),)
