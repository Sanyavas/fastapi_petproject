import configparser
import pathlib

from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker


file_config = pathlib.Path(__file__).parent.parent.joinpath('conf/config.ini')
config = configparser.ConfigParser()
config.read(file_config)

username = config.get('DEV', 'POSTGRES_USER')
password = config.get('DEV', 'POSTGRES_PASSWORD')
db_name = config.get('DEV', 'POSTGRES_DB_NAME')
domain = config.get('DEV', 'POSTGRES_DOMAIN')
port = config.get('DEV', 'POSTGRES_PORT')

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{username}:{password}@{domain}:{port}/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo_pool=True)
DBSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = DBSession()
    try:
        yield db
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()




