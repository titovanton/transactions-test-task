import logging
import os
import sys
from typing import Generator, Any

import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import database_exists, create_database

# to make the following modules import possible
sys.path.append('/app')

# for load models to metadata purpose
import models  # noqa: E402, F401
from main import app as main_app  # noqa: E402
from database import get_db, Base  # noqa: E402


log = logging.getLogger(__name__)
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(TEST_DATABASE_URL)

if not database_exists(engine.url):
    create_database(engine.url)

TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def populate() -> Generator[bool, Any, None]:
    """
    Creates db before testcase starts
    and drops after testcase ends.
    """

    Base.metadata.create_all(engine)
    yield True
    Base.metadata.drop_all(engine)


@pytest.fixture
def db(populate: bool) -> Generator[Session, Any, None]:
    """
    Creates a fresh sqlalchemy session for each test that operates in a
    transaction. The transaction is rolled back at the end of each test ensuring
    a clean state.
    """

    # connect to the database
    connection = engine.connect()

    # begin a non-ORM transaction
    transaction = connection.begin()

    # bind an individual Session to the connection
    session = TestSession(bind=connection)

    yield session

    session.close()

    # NOTE: it rolls back transaction in the RAM,
    # changes wasn't commited to actual DB, as long
    # as connection.commit() wasn't called.
    # You will not see changes from psql cli,
    # even if you see them via SQLAlchemy.
    # But if you manually commit the connection -
    # then this rollback won't work.
    transaction.rollback()

    # return connection to the Engine
    connection.close()


@pytest.fixture
def app() -> Generator[FastAPI, Any, None]:
    yield main_app


@pytest.fixture()
def client(app: FastAPI, db: Session) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as client:
        yield client
