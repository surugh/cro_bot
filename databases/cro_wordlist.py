from random import randint

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from databases.models.russian_nouns import Word

engine = create_engine("sqlite:///databases/russian_nouns.db")


def word_choice() -> str:
    with Session(engine) as session:
        word = session.scalars(
            select(Word.word).where(
                Word.id == randint(1, 55871)
            )
        ).first()
    return word


def word_definition(word) -> str:
    with Session(engine) as session:
        definition = session.scalars(
            select(Word.definition).where(
                Word.word == word
            )
        ).first()
    return definition
