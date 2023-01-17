from databases.cro_db import Database

from aiogram import Bot
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from handlers.start_command import command_start_handler

router = Router()

db = Database("databases/cro_data.db")


@router.message(Command(commands=['restart']))
async def command_restart_handler(message: Message, bot: Bot) -> None:
    """
    This handler receive messages with `/restart` command
    """
    if message.chat.type != 'private':
        admins = await bot.get_chat_administrators(message.chat.id)
        admins_id_list = []
        for admin in admins:
            if not admin.user.is_bot:
                admins_id_list.append(admin.user.id)
        if message.from_user.id in admins_id_list:
            db.del_leader(message.chat.id)
            db.del_word(message.chat.id)
            await message.answer(
                f"{message.from_user.full_name} перезапустил игру"
            )
            await command_start_handler(message)
        else:
            await message.answer(
                f"{message.from_user.full_name} Вы не администратор"
            )
    else:
        await message.answer("Команда доступна только в группах")
    # await message.delete()
