import os
import time

from dotenv import load_dotenv

from aiogram import Bot
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    # CREATOR = os.getenv('CREATOR')
    # ADMIN = os.getenv('ADMIN')


async def send_backup_db(message: Message, bot: Bot) -> None:
    if message.from_user.id == os.getenv('CREATOR') or os.getenv('ADMIN'):
        os.system("cd")
        time.sleep(1)
        path = "/home/ubuntu/cro_bot/databases/data/"
        cmd = f"/usr/bin/zip {path}backup_cro_data {path}cro_data.db"
        os.popen(cmd)
        try:
            file = f'{path}backup_cro_data.zip'
            await bot.send_document(message.from_user.id, FSInputFile(file))
            time.sleep(1)
            os.remove(file)
        except FileNotFoundError:
            await message.answer("Файл не найден!")
    else:
        await message.answer("Вы не администратор")