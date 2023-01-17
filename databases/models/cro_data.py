from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Chat(Base):
    __tablename__ = "chats"

    chat_id: Mapped[int] = mapped_column(primary_key=True)
    leader_id: Mapped[int]
    hidden_word: Mapped[str]