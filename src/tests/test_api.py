from sqlalchemy.orm import Session

from models import User


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200


def test_create(db: Session):
    assert db.query(User).count() == 0
    user = User(nickname="Vasya", email="vasya@exm.com")
    db.add(user)
    db.commit()
    db.refresh(user)
    assert user.id
    assert db.query(User).count() == 1


def test_no_data_between_cases(db: Session):
    assert db.query(User).count() == 0


