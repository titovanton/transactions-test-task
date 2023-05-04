import enum

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy import String, Float, Enum
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, nullable=True, default='')
    email = Column(String, unique=True, index=True, nullable=False)

    cards = relationship("Card", back_populates="user")


class Card(Base):
    __tablename__ = "card"

    id = Column(Integer, primary_key=True, index=True)
    mask_number = Column(String)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=True, default=None)

    user = relationship("User", back_populates="cards", uselist=False)
    transactions = relationship("Transaction", back_populates="card")
    balance = relationship("CardBalance", back_populates="card", uselist=False, cascade="all,delete")


class CardBalance(Base):
    __tablename__ = "cardbalance"

    id = Column(Integer, primary_key=True, index=True)
    available = Column(Float, nullable=False, default=0)

    card_id = Column(Integer, ForeignKey("card.id"))

    card = relationship("Card", back_populates="balance")


class Transaction(Base):
    __tablename__ = "transaction"

    class StatusChoices(enum.Enum):
        success = 1
        faild = 2
        pending = 3

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(StatusChoices), nullable=False)
    transaction_amount = Column(Float, nullable=False, default=0)
    transaction_date = Column(String, nullable=False)

    card_id = Column(Integer, ForeignKey("card.id"), index=True)

    card = relationship("Card", back_populates="transactions")
