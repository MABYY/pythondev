from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:P24182512!@localhost/dbfastapi'

from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


engine = create_engine(SQLALCHEMY_DATABASE_URL) # connects sqlalchemy to the postgres

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() # define base class

# Create session and start database if it is not in postgres
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Tutorial: https://www.youtube.com/watch?v=0sOvCWFmrtA 
# https://fastapi.tiangolo.com/tutorial/sql-databases/

# SQLALCHEMY_DATABASE_URL = 'sqlite:///test.db', , echo=True
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()