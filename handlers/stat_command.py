import aiogram.exceptions

from databases.cro_db import Database

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

db = Database("databases/cro_data.db")


@router.message(Command(commands=['stat']))
async def command_stat_handler(message: Message, bot: Bot) -> None:
    """
    This handler receive messages with `/stat` command
    """
    if message.chat.type != 'private':
        all_players = db.get_players_data()
        chat_players = []
        for player in all_players:
            try:
                chat_player = await bot.get_chat_member(message.chat.id, player[0])
                if chat_player.status != 'left':
                    chat_players.append((chat_player.user.id, int(player[1])))
            except aiogram.exceptions.TelegramBadRequest:
                pass
        sort_players = sorted(chat_players, key=lambda c_player: c_player[1], reverse=True)
        top = []
        x = 0
        for _ in sort_players[0:7]:
            x = x + 1
            p = await bot.get_chat_member(message.chat.id, _[0])
            top.append(f"{x}. {p.user.full_name} - {_[1]}")
        text = '\n'.join(top)
        await message.answer(f"ТОП 7 игроков этой группы:\n{text}")
    else:
        await message.answer(f"Статистика доступна только в группах")
        # private = []
        # x = 0
        # for _ in sorted(all_players, key=lambda i: i[1], reverse=True):
        #     x = x + 1
        #     # p = await bot.get_chat_member(message.chat.id, _[0])
        #     private.append(f"{x}. {_[0]} - {_[1]}")
        # text = '\n'.join(private)
        # await message.answer(f'{text}')
