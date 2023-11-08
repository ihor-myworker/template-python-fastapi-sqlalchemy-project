import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

DB_CONFIG_COMES_FROM_ENV = os.environ.get("DB_CONFIG_FROM_ENV")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST") or "localhost"
POSTGRES_PORT = os.environ.get("POSTGRES_PORT") or "5432"
POSTGRES_DB = os.environ.get("POSTGRES_DB") or "postgres"
POSTGRES_USER = os.environ.get("POSTGRES_USER") or "postgres"
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD") or "password"
