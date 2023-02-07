from aiogram import Bot
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from functions.public import restart_game

router = Router()


@router.message(Command(commands=['restart']))
async def command_restart_handler(message: Message, bot: Bot) -> None:
    """
    This handler receive messages with `/restart` command
    """
    if message.chat.type != 'private':
        await restart_game(message, bot)
    else:
        await message.answer("Команда доступна только в группах")
