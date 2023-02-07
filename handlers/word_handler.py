from aiogram import Router, F
from aiogram.types import Message

from functions.private import add_user_address
from functions.public import public_word_definition, word_catcher

router = Router()


@router.message(F.text)
async def word_handler(message: Message) -> None:
    """
    Handler will check messages fo hidden word

    """
    await public_word_definition(message)
    if message.chat.type != 'private':
        await word_catcher(message)
    else:
        await add_user_address(message)
