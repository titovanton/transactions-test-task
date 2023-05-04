import logging

from sqlalchemy import text, desc, asc
from sqlalchemy.orm import Session, joinedload

from models import User, Card, CardBalance, Transaction
from schemas import SortField, SortOrder, RootResponse


log = logging.getLogger(__name__)


def transactions_by_cards_sql(
    db: Session,
    cards: list[str] | None = None
) -> list:
    if not cards:
        return []

    query = text(
        """
        SELECT
            u."nickname",
            u."email",
            c."id",
            c."mask_number",
            cb."available",
            t."id",
            t."transaction_date",
            t."transaction_amount",
            t."status"
        FROM "transaction" AS t
        JOIN "card" AS c ON t."card_id"=c."id"
        JOIN "cardbalance" AS cb ON cb."card_id"=c."id"
        JOIN "user" AS u ON c."user_id"=u."id"
        WHERE c."mask_number" IN :cards
        ORDER BY t."transaction_date" DESC
        """
    )
    _cards = tuple([str(i) for i in cards])
    return db.execute(query, {"cards": _cards}).fetchall()


def transactions_by_cards_orm(
    db: Session,
    cards: list[str] = [],
    sort_field: SortField = SortField.date,
    sort_order: SortOrder = SortOrder.desc,
) -> list[RootResponse]:
    _cards = tuple([str(i) for i in cards])
    map_field = {
        SortField.email: User.email,
        SortField.nickname: User.nickname,
        SortField.date: Transaction.transaction_date,
        SortField.status: Transaction.status,
    }
    map_order = {
        SortOrder.asc: asc,
        SortOrder.desc: desc,
    }

    query = db.query(
        Transaction.id,
        Transaction.transaction_date,
        Transaction.transaction_amount,
        Transaction.status,
        Card.id,
        Card.mask_number,
        CardBalance.available,
        User.nickname,
        User.email
    )
    query = query.select_from(Transaction)
    query = query.outerjoin(Card)
    query = query.outerjoin(CardBalance)
    query = query.outerjoin(User)
    query = query.order_by(map_order[sort_order](map_field[sort_field]))

    if cards:
        query = query.filter(Card.mask_number.in_(_cards))

    return [
        RootResponse(
            transaction_id=row[0],
            transaction_date=row[1],
            transaction_amount=row[2],
            transaction_status=row[3],
            card_id=row[4],
            card_mask_number=row[5],
            card_balance=row[6],
            user_nickname=row[7],
            user_email=row[8],
        ) for row in query
    ]
