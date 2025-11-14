from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os, datetime
DATABASE_URL = os.getenv('DATABASE_URL','sqlite:///mehroz_professional.db')
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False} if 'sqlite' in DATABASE_URL else {})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
class User(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, unique=True, index=True)
    name = Column(String)
    lang = Column(String, default='en')
    gender = Column(String)
    birth_date = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
class Broadcast(Base):
    __tablename__='broadcasts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
def init_db():
    Base.metadata.create_all(bind=engine)
