from databases import crud

from aiogram import Router, Bot, exceptions
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command(commands=['chat']))
async def command_chat_handler(message: Message, bot: Bot) -> None:
    if message.chat.type == 'private':
        chats = crud.get_chats_ids()
        all_chats = []
        for chat in chats:
            try:
                data = await bot.get_chat(str(chat))
                if data.username:
                    all_chats.append(f"{data.title} - @{data.username}")
            except exceptions.TelegramBadRequest:
                pass
            except exceptions.TelegramForbiddenError:
                pass
        text = '\n'.join(all_chats)
        await message.answer(text)
    else:
        await message.answer(
            "Команда доступна только в личных сообщениях у бота"
        )
