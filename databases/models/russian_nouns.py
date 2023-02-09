from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Word(Base):
    __tablename__ = "nouns"

    id: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str]
    definition: Mapped[str]
