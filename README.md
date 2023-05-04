# Transactions test task

You can read full description in the `Test_task_Anton.TXT`. It's in Russian, so use translater :)

## Stack

- Python v3.11
- FastAPI
- SQLAlchemy
- Alembic
- Pytest
- Faker

## Install

Build `api` service first with the following command

    docker compose build api

Now you need to run `postgres` service, so it take its time to create pgdata folder. That will prevent FastAPI from crashing:

    docker compose up -d postgres

After that - run the rest:

    docker compose up -d

To stop it, use the following:

    docker compose down

All containers will be deleted, but the data shell persist, as long as `pgdata` folder. Next time you don't need to follow the above order, simply run entier project in diamon mode.

## Populate DB

First, you need to apply schema, be sure that you have the project up and running:

    docker compose exec api alembic upgrade head

From now on, you can vizit `http://localhost:8000` to see empty output =), to see something more, you have to fill DB with some data:

    docker compose exec api python data_models.py

Don't run population twice, if you don't want to know more than me (I didn't test it).

## Pytest

Each time you run tests, the engine checks for `tests_db` existence, if it's required - then engine creates schema. Each test case starts with fully blank DB, with only schema in it. 

To run tests use the following, while the project is up

    docker compose exec api pytest

## Access and Docs

As long as it's FastAPI project, you have 2 options:

    http://localhost:8000
    http://localhost:8000/docs

Be wellcome.

## PS

Live long and prosper.

