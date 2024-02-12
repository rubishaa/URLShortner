from datetime import datetime

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

from livecode.config import DATABASE_URI

engine = create_engine(DATABASE_URI)
engine=engine.connect()

Base = declarative_base()

class ShortUrls(Base):
    __tablename__ = 'testurl'
    id = Column(Integer, primary_key=True)
    longurl = Column(String(500), nullable=False)
    shorturl = Column(String(20), nullable=False, unique=True)
    #created_at = db.Column(db.DateTime(), default=datetime.now(), nullable=False)

Base.metadata.create_all(engine)
print("Table 'URLs' created successfully.")
Session = sessionmaker(engine)


def insert_shorturl(url,short):
    session = Session()
    new_link = ShortUrls(
        longurl=url, shorturl=short)
    session.add(new_link)
    session.commit()

def get_url(shorturl):
  try:
    session = Session()
    link = session.query(ShortUrls).filter(ShortUrls.shorturl == shorturl).first()
    return link
  except Exception as e:
    return None