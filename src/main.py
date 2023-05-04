import logging

from typing import Annotated

from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from schemas import SortField, SortOrder, RootResponse
from crud import transactions_by_cards_orm


log = logging.getLogger(__name__)
app = FastAPI()


@app.get("/", response_model=list[RootResponse])
def root(
    db: Session = Depends(get_db),
    cards: Annotated[list[str] | None, Query(description="Users card numbers")] = [],
    sort_field: Annotated[SortField | None, Query()] = SortField.date,
    sort_order: Annotated[SortOrder | None, Query()] = SortOrder.desc,
):
    result = transactions_by_cards_orm(db, cards, sort_field, sort_order)
    return result
