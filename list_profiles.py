from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Profile

engine = create_engine('sqlite:///goals.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

profiles = session.query(Profile).order_by(Profile.name).all()

for profile in profiles:
  print(profile.name)
