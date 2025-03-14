from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


DATABASE_URL = 'sqlite:///EasyRoom.db'
engine = create_engine(DATABASE_URL, echo=True)  # echo=True exibe as queries no terminal


SessionLocal = sessionmaker(bind=engine)

def create_session():
    return SessionLocal()
