from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

from databases.models.cro_data import Chat

cro_db = create_engine("sqlite:///databases/cro_data.db")


def get_chats_ids():
    with Session(cro_db) as session:
        result = session.scalars(
            select(Chat.chat_id)
        ).fetchall()
    return result
