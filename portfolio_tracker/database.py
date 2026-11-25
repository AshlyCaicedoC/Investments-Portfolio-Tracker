import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# reads the .env file in the project folder and loads its values as environment variables
load_dotenv()

# URL.create builds the connection address for us, so special characters
# in the password (like ! or @) don't break it
def connect():
    # the code never holds the values; it asks the environment for them
    url = URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME"),
    )
    return create_engine(url)


engine = connect()

# every business operation asks this factory for a new session (a conversation with the database)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


# every SQLAlchemy model inherits from Base, so SQLAlchemy knows which tables exist
class Base(DeclarativeBase):
    pass


@contextmanager
def transaction():

    session = SessionLocal()
    try:
        # hands the session to the code inside the "with" block and waits here until it finishes
        yield session
        # the block finished without errors: keep every change
        session.commit()
    except Exception:
        # something failed (a broken rule or a database error): undo every change
        session.rollback()
        # re-raise the error so the service/CLI still knows what went wrong
        raise
    finally:
        # always give the connection back, whether we committed or rolled back
        session.close()


def init_db():
    # importing the models registers every table on Base before we create them
    import portfolio_tracker.models

    Base.metadata.create_all(engine)