from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


POSTGRES_LOGIN = "postgres"
POSTGRES_PASSWORD = "postgres"
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_LOGIN}:{POSTGRES_PASSWORD}@db/db_memes"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
