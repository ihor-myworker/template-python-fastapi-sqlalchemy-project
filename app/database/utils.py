import configparser
import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

import app.config as app_config

SYNC_DB_API = "psycopg2"
ASYNC_DB_API = "asyncpg"

_SYNC_ENGINE: Engine | None = None


def get_db_config_from_file():
    config = configparser.ConfigParser()
    path_to_cfg = os.path.join(app_config.ROOT_DIR, "config.ini")
    config.read(path_to_cfg)
    return {
        "host": config.get("database", "host"),
        "port": config.get("database", "port"),
        "name": config.get("database", "database_name"),
        "user": config.get("database", "username"),
        "password": config.get("database", "password"),
    }


def get_db_config_from_env():
    return {
        "host": app_config.POSTGRES_HOST,
        "port": app_config.POSTGRES_PORT,
        "name": app_config.POSTGRES_DB,
        "user": app_config.POSTGRES_USER,
        "password": app_config.POSTGRES_PASSWORD,
    }


def build_connection_string(
    *,
    db_api: str = ASYNC_DB_API,
    user: str = app_config.POSTGRES_USER,
    password: str = app_config.POSTGRES_PASSWORD,
    host: str = app_config.POSTGRES_HOST,
    port: str = app_config.POSTGRES_PORT,
    db: str = app_config.POSTGRES_DB,
) -> str:
    return f"postgresql+{db_api}://{user}:{password}@{host}:{port}/{db}"


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
    url = build_connection_string(
        db_api=SYNC_DB_API, user=user, password=password, host=host, port=port, db=db
    )
    if not database_exists(url):
        create_database(url)

    global _SYNC_ENGINE
    if _SYNC_ENGINE is None:
        connection_string = build_connection_string(db_api=SYNC_DB_API)
        _SYNC_ENGINE = create_engine(connection_string)
    return _SYNC_ENGINE


def get_engine_from_config():
    """
    Get SQLalchemy engine using credentials form config file.
    """
    config_from_env = app_config.DB_CONFIG_COMES_FROM_ENV
    cfg = get_db_config_from_env() if config_from_env else get_db_config_from_file()
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
