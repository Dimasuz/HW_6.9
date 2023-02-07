from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String,
                        func)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from config import PG_DSN_ASYNC


def get_engine():
    return create_async_engine(PG_DSN_ASYNC)


def get_session_maker():
    return sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


engine = get_engine()

Session = get_session_maker()

Base = declarative_base()


class Users(Base):
    __tablename__ = "ads_users"

    id = Column(Integer, primary_key=True)
    name = Column(String(60), unique=True)
    email = Column(String(60), unique=True)
    password = Column(String(60), nullable=False)


class Adv(Base):
    __tablename__ = "advertisements"

    id = Column(Integer(), primary_key=True)
    title = Column(String(50), nullable=False)
    descr = Column(String(200), nullable=False)
    creat_time = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("ads_users.id", ondelete="CASCADE"))
    user = relationship("Users", lazy="joined")
