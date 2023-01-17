import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.cursor.executescript("""
        CREATE TABLE IF NOT EXISTS players (
            user_id,
            score,
            address
        );
        CREATE TABLE IF NOT EXISTS chats (
            chat_id,
            leader_id,
            hidden_word
        );
        """)
        self.connection.commit()

    def add_user(self, user_id: int) -> None:
        self.cursor.execute(
            "INSERT INTO players VALUES(?, ?, ?);", (user_id, 0, None))
        self.connection.commit()

    def user_exists(self, user_id: int) -> bool:
        result = self.cursor.execute(
            "SELECT user_id FROM players WHERE user_id = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_players_data(self) -> list:
        result = self.cursor.execute(
            "SELECT * FROM players")
        return result.fetchall()  # fetchmany(7)

    def add_score(self, user_id: int) -> None:
        self.cursor.execute(
            "UPDATE players SET score = score+1 WHERE user_id = ?", (user_id,))
        self.connection.commit()

    def get_score(self, user_id: int) -> int:
        result = self.cursor.execute(
            "SELECT score FROM players WHERE user_id = ?", (user_id,))
        return result.fetchone()[0]

    def del_score(self, user_id: int) -> None:
        self.cursor.execute(
            "UPDATE players SET score = 0 WHERE user_id = ?", (user_id,))
        self.connection.commit()

    def chat_exists(self, chat_id: int) -> bool:
        result = self.cursor.execute(
            "SELECT chat_id FROM chats WHERE chat_id = ?", (chat_id,))
        return bool(len(result.fetchall()))

    def add_chat(self, chat_id: int) -> None:
        self.cursor.execute(
            "INSERT INTO chats VALUES(?, ?, ?);", (chat_id, None, None))
        self.connection.commit()

    def add_leader(self, user_id: int, chat_id: int) -> None:
        self.cursor.execute(
            "UPDATE chats SET leader_id = ? WHERE chat_id = ?", (user_id, chat_id))
        self.connection.commit()

    def get_leader(self, chat_id: int) -> int:
        result = self.cursor.execute(
            "SELECT leader_id FROM chats WHERE chat_id = ?", (chat_id,))
        return result.fetchone()[0]

    def del_leader(self, chat_id: int) -> None:
        self.cursor.execute(
            "UPDATE chats SET leader_id = ? WHERE chat_id = ?", (None, chat_id))
        self.connection.commit()

    def add_word(self, word: str, chat_id: int) -> None:
        self.cursor.execute(
            "UPDATE chats SET hidden_word = ? WHERE chat_id = ?", (word, chat_id))
        self.connection.commit()

    def get_word(self, chat_id: int) -> str:
        result = self.cursor.execute(
            "SELECT hidden_word FROM chats WHERE chat_id = ?", (chat_id,))
        return result.fetchone()[0]

    def del_word(self, chat_id: int) -> None:
        self.cursor.execute(
            "UPDATE chats SET hidden_word = ? WHERE chat_id = ?", (None, chat_id))
        self.connection.commit()

    def address_exists(self, user_id: int) -> bool:
        result = self.cursor.execute(
            "SELECT address FROM players WHERE user_id = ?", (user_id,))
        return bool(len(result.fetchall()))

    def add_address(self, address: str, user_id: int) -> None:
        self.cursor.execute(
            "UPDATE players SET address = ? WHERE user_id = ?", (address, user_id))
        self.connection.commit()

    def get_address(self, user_id: int) -> str:
        result = self.cursor.execute(
            "SELECT address FROM players WHERE user_id = ?", (user_id,))
        return result.fetchone()[0]
