from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command

from functions.public import top_players

router = Router()


@router.message(Command(commands=['stat']))
async def command_stat_handler(message: Message, bot: Bot) -> None:
    """
    This handler receive messages with `/stat` command
    """
    if message.chat.type != 'private':
        await top_players(message, bot)
    else:
        await message.answer(f"Статистика доступна только в группах")
