from sqlalchemy import create_engine
from model import Base

engine = create_engine('sqlite:///goals.db')

Base.metadata.create_all(engine)
