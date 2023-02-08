import time

import bcrypt
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import PG_DSN
from models import Adv, Base, Users

engine = create_engine(PG_DSN)

Session = sessionmaker(bind=engine)


def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


@pytest.fixture(scope="session", autouse=True)
def init_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    engine.dispose()


@pytest.fixture()
def create_user():
    name = f"name{time.time()}"
    email = f"email{time.time()}@email.email"
    password = "password"
    with Session() as session:
        user = Users(name=name, email=email, password=hash_password(password))
        session.add(user)
        session.commit()
        return {
            f"id": user.id,
            f"name": user.name,
            f"email": user.email,
            f"password": user.password,
        }


@pytest.fixture()
def create_adv(
    title: str = None, descr: str = None, user_id: int = None, password: str = None
):
    title = title or "title_def"
    descr = descr or "descr_def"
    user_id = user_id or "1"
    password = password or "password"
    with Session() as session:
        new_adv = Adv(title=title, descr=descr, user_id=user_id)
        session.add(new_adv)
        session.commit()
        return {
            "id": new_adv.id,
            "title": new_adv.title,
            "descr": new_adv.descr,
            "user_id": new_adv.user_id,
            "password": password,
        }
