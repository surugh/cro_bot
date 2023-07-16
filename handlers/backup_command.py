from functions import backup_db

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command(commands=['backup']))
async def command_backup_handler(message: Message, bot: Bot) -> None:
    if message.from_user.id == 510208922:
        await backup_db.send_backup_db(message, bot)
    else:
        await message.answer("Вы не администратор")
