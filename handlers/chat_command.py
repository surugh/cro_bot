from databases import crud

from aiogram import Router, Bot, exceptions
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command(commands=['chat']))
async def command_chat_handler(message: Message, bot: Bot) -> None:
    chats = crud.get_chats_ids()
    for chat in chats:
        try:
            data = await bot.get_chat(str(chat))
            if chat == -1001228658207:
                text = "Игра с множителями!"
                await message.answer(f"{data.title}\n@{data.username}\n{text}")
            else:
                if data.username:
                    await message.answer(f"{data.title}\n@{data.username}")
        except exceptions.TelegramBadRequest:
            pass
        except exceptions.TelegramForbiddenError:
            pass

