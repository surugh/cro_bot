from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, insert, update

from databases.models.cro_data import Chat, Player

cro_db = create_engine("sqlite:///databases/data/cro_data.db")


def add_address(address: str, player_id: int):
    with Session(cro_db) as session:
        session.execute(
            update(Player).where(
                Player.user_id == player_id
            ).values(
                address=address,
            )
        )
        session.commit()


def address_exists(player_id: int):
    with Session(cro_db) as session:
        result = session.scalars(
            select(Player.address).where(
                Player.user_id == player_id
            )
        ).fetchall()
    return result[0]


def del_score(player_id: int):
    with Session(cro_db) as session:
        session.execute(
            update(Player).where(
                Player.user_id == player_id
            ).values(
                score=0,
            )
        )
        session.commit()


def get_address(player_id: int) -> int:
    with Session(cro_db) as session:
        result = session.scalars(
            select(Player.address).where(
                Player.user_id == player_id
            )
        ).first()
    return result


def add_word(word: str, chat_id: int):
    with Session(cro_db) as session:
        session.execute(
            update(Chat).where(
                Chat.chat_id == chat_id
            ).values(
                hidden_word=word,
            )
        )
        session.commit()


def get_players_data():
    with Session(cro_db) as session:
        result = session.scalars(
            select(Player)
        ).fetchall()
    return result


def add_chat(chat_id: int):
    with Session(cro_db) as session:
        session.execute(
            insert(Chat).values(
                chat_id=chat_id,
                leader_id=None,
                hidden_word=None
            )
        )
        session.commit()


def chat_exists(chat_id: int) -> bool:
    with Session(cro_db) as session:
        result = session.scalars(
            select(Chat.chat_id).where(
                Chat.chat_id == chat_id
            )
        ).fetchall()
    return bool(len(result))


def add_leader(player_id: int, chat_id: int):
    with Session(cro_db) as session:
        session.execute(
            update(Chat).where(
                Chat.chat_id == chat_id
            ).values(
                leader_id=player_id,
            )
        )
        session.commit()


def del_word(chat_id: int):
    with Session(cro_db) as session:
        session.execute(
            update(Chat).where(
                Chat.chat_id == chat_id
            ).values(
                hidden_word=None,
            )
        )
        session.commit()


def del_leader(chat_id: int):
    with Session(cro_db) as session:
        session.execute(
            update(Chat).where(
                Chat.chat_id == chat_id
            ).values(
                leader_id=None,
            )
        )
        session.commit()


def get_score(player_id: int) -> int:
    with Session(cro_db) as session:
        result = session.scalars(
            select(Player.score).where(
                Player.user_id == player_id
            )
        ).first()
    return result


def add_score(player_id: int, multipler=1):
    with Session(cro_db) as session:
        session.execute(
            update(Player).where(
                Player.user_id == player_id
            ).values(
                score=Player.score + multipler,
            )
        )
        session.commit()


def get_leader(chat_id: int) -> int:
    with Session(cro_db) as session:
        result = session.scalars(
            select(Chat.leader_id).where(
                Chat.chat_id == chat_id
            )
        ).first()
    return result


def add_user(player_id: int):
    with Session(cro_db) as session:
        session.execute(
            insert(Player).values(
                user_id=player_id,
                score=0,
                address=None
            )
        )
        session.commit()


def user_exists(player_id: int) -> bool:
    with Session(cro_db) as session:
        result = session.scalars(
            select(Player.user_id).where(
                Player.user_id == player_id
            )
        ).fetchall()
    return bool(len(result))


def get_hidden_word(chat_id: int) -> str:
    with Session(cro_db) as session:
        result = session.scalars(
            select(Chat.hidden_word).where(
                Chat.chat_id == chat_id
            )
        ).first()
    return result


def get_chats_ids():
    with Session(cro_db) as session:
        result = session.scalars(
            select(Chat.chat_id)
        ).fetchall()
    return result
