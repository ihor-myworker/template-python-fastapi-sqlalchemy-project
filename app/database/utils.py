import configparser
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from app.config import ROOT_DIR


def get_db_config_from_file():
    config = configparser.ConfigParser()
    path_to_cfg = os.path.join(ROOT_DIR, "config.ini")
    config.read(path_to_cfg)
    return {
        "host": config.get("database", "host"),
        "port": config.get("database", "port"),
        "name": config.get("database", "database_name"),
        "user": config.get("database", "username"),
        "password": config.get("database", "password"),
    }


def get_engine(user, password, host, port, db):
    """
    Get SQLalchemy engine using credentials.
    Input:
        db: database name
        user: Username
        host: Hostname of the database server
        port: Port number
        passwd: Password for the database
    Returns:
        Database engine
    """

    url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    if not database_exists(url):
        create_database(url)

    engine = create_engine(url, pool_size=50, echo=True)
    return engine


def get_engine_from_config():
    """
    Get SQLalchemy engine using credentials form config file.
    """
    cfg = get_db_config_from_file()
    return get_engine(
        user=cfg["user"],
        password=cfg["password"],
        host=cfg["host"],
        port=cfg["port"],
        db=cfg["name"],
    )


def get_session():
    """
    Return sessionmaker for a database from config.
    """
    engine = get_engine_from_config()
    Session = sessionmaker(bind=engine)
    return Session


SessionLocal = get_session()
Base = declarative_base()


def get_db_for_api():
    """
    Get session instance which will be created on each request and automatically closed.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
