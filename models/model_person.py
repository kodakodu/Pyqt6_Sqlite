from sqlalchemy import create_engine, Column, Integer,String
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    surname = Column(String)

def init_db(db_url = 'sqlite:///crud_app.db'):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
