
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()
engine = create_engine('sqlite:///ice_cream_parlor.db', echo=True)
SessionLocal = sessionmaker(bind=engine)
