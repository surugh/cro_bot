from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from functions.public import start_game
from functions.private import check_address
from handlers.help_command import command_help_handler

router = Router()


@router.message(Command(commands=['start']))
async def command_start_handler(message: Message) -> None:
    """
    This handler receive messages with `/start` command
    """
    if message.chat.type != 'private':
        await start_game(message)
    else:
        await command_help_handler(message)
        await check_address(message)
