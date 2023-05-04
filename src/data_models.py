"""
This module contains data model to populate the DB
for presentation purpose. The same model is going
to be used for tests.
"""

from faker import Faker
from sqlalchemy.orm import Session

from models import User, Card, CardBalance, Transaction


def populate(db: Session):
    fake = Faker()
    Faker.seed(20)

    users = [
        ("bob", "bob@eml.com"),
        ("anna", "anna@eml.com"),
    ]
    num1 = fake.credit_card_number()
    num2 = fake.credit_card_number()
    num3 = fake.credit_card_number()
    cards = [
        ("bob", num1),
        ("bob", num2),
        ("anna", num3),
    ]
    card_balances = [
        (num1, 10),
        (num2, 20.4),
        (num3, 105),
    ]
    StatusChoices = Transaction.StatusChoices
    transactions = [
        (num1, fake.date_time(), 5, StatusChoices.success),
        (num2, fake.date_time(), 6, StatusChoices.success),
        (num3, fake.date_time(), 7, StatusChoices.success),
        (num3, fake.date_time(), 8, StatusChoices.faild),
    ]

    name_to_user = {}
    for nickname, email in users:
        user = User(nickname=nickname, email=email)
        db.add(user)
        name_to_user[nickname] = user
    db.commit()

    num_to_card = {}
    for nickname, num in cards:
        user = name_to_user[nickname]
        card = Card(mask_number=num, user_id=user.id)
        db.add(card)
        num_to_card[num] = card
    db.commit()

    for num, avail in card_balances:
        card = num_to_card[num]
        card_bal = CardBalance(available=avail, card_id=card.id)
        db.add(card_bal)

    for num, dt, amount, status in transactions:
        card = num_to_card[num]
        trans = Transaction(
            status=status,
            transaction_amount=amount,
            transaction_date=dt,
            card_id=card.id
        )
        db.add(trans)

    db.commit()

    # smocky test
    assert db.query(User).count() == 2
    assert db.query(Card).count() == 3
    assert db.query(CardBalance).count() == 3
    assert db.query(Transaction).count() == 4

    return (users, cards, card_balances, transactions, num1, num2, num3)


if __name__ == "__main__":
    # sorry PEP8, I love you, but this time I'm lazy...
    from database import SessionLocal

    populate(SessionLocal())
