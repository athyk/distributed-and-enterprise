from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy.sql import text

import os

DATABASE_NAME = os.environ.get('AUTHENTICATION_DB_NAME') or 'authorisation_db'

DATABASE_USERNAME = os.environ.get('DATABASE_USERNAME') or 'unihub'
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD') or 'hVvBgjrKY5wx9dv56Zadbi4AKbFK'

DATABASE_HOST = os.environ.get('DATABASE_HOST') or '127.0.0.1'
DATABASE_PORT = os.environ.get('DATABASE_PORT') or '5432'

GENERAL_DATABASE_URL = f'postgresql+psycopg2://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}'

AUTHORISATION_DATABASE_URL = GENERAL_DATABASE_URL + f'/{DATABASE_NAME}'
POSTGRES_DATABASE_URL = GENERAL_DATABASE_URL + '/postgres'

# Create engine
engine = create_engine(AUTHORISATION_DATABASE_URL, pool_pre_ping=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Dependency to get DB session
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def confirm_database_exists(database_name=DATABASE_NAME):
    checking_engine = create_engine(POSTGRES_DATABASE_URL, isolation_level="AUTOCOMMIT")

    print(f'Checking If Database ({database_name}) Exists')

    with checking_engine.connect() as conn:
        result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{database_name}'"))
        exists = result.scalar() is not None

        if not exists:
            conn.execute(text(f"CREATE DATABASE {database_name}"))
            print(f'Database ({database_name}) Previously Not Existing Now Created')
        else:
            print(f'Database ({database_name}) Exists')
