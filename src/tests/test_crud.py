import logging

from sqlalchemy.orm import Session

from crud import transactions_by_cards_sql, transactions_by_cards_orm
from data_models import populate
from models import User, Card, CardBalance, Transaction
from schemas import SortField, SortOrder
from utils import QueryCounter


log = logging.getLogger(__name__)


def test_transactions_by_cards(db: Session):
    assert db.query(User).count() == 0
    assert db.query(Card).count() == 0
    assert db.query(CardBalance).count() == 0
    assert db.query(Transaction).count() == 0

    # try with empty db
    result = transactions_by_cards_orm(db, [], SortField.date, SortOrder.desc)
    assert list(result) == []

    with QueryCounter(db) as counter:
        (
            users, cards, card_balances, transactions, num1, num2, num3
        ) = populate(db)

    log.info(("QUERY NUM", counter.count))

    # for no cards given it returns all transactions
    result = transactions_by_cards_orm(db, [])
    assert len(result) == 4

    result = transactions_by_cards_sql(db, [num1, 1233])
    assert len(result) == 1
    result = transactions_by_cards_sql(db, [num1, None])
    assert len(result) == 1
    result = transactions_by_cards_sql(db, [num1, num3])
    assert len(result) == 3

    # order by
    assert result[0][6] > result[1][6] > result[2][6]

    # ORM approach
    result = transactions_by_cards_orm(db, [num1])
    assert len(result) == 1
    result = transactions_by_cards_orm(db, [num1, 1233])
    assert len(result) == 1
    result = transactions_by_cards_orm(db, [num1, None])
    assert len(result) == 1

    # order mapping
    result = transactions_by_cards_orm(db, [num1, num3])
    assert len(result) == 3
    dates = [obj.transaction_date for obj in result]
    assert dates[0] > dates[1] > dates[2]
    result = transactions_by_cards_orm(
        db, [num1, num3], sort_order=SortOrder.asc)
    dates = [obj.transaction_date for obj in result]
    assert dates[0] < dates[1] < dates[2]
