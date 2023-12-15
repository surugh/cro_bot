from functions import backup_db

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command(commands=['backup']))
async def command_backup_handler(message: Message, bot: Bot) -> None:
    if message.chat.type == 'private':
        await backup_db.send_backup_db(message, bot)
