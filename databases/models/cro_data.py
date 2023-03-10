from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = "players"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    score: Mapped[int]
    address: Mapped[str]


class Chat(Base):
    __tablename__ = "chats"

    chat_id: Mapped[int] = mapped_column(primary_key=True)
    leader_id: Mapped[int]
    hidden_word: Mapped[str]
