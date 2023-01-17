from databases.cro_db import Database

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from handlers.help_command import command_help_handler
from keyboards.start_keyboard import command_start_keyboard, command_address_keyboard, command_pay_keyboard

router = Router()

db = Database("databases/cro_data.db")


@router.message(Command(commands=['start']))
async def command_start_handler(message: Message) -> None:
    """
    This handler receive messages with `/start` command
    """
    if message.chat.type != 'private':
        if not db.chat_exists(message.chat.id):
            db.add_chat(message.chat.id)
        if not db.get_leader(message.chat.id):
            await message.answer(
                "<b>Хочешь быть ведущим?</b>",
                reply_markup=command_start_keyboard()
            )
        else:
            await message.answer("Ведущий уже выбран /restart ?")
    else:
        await command_help_handler(message)
        address = db.address_exists(message.from_user.id)
        if not address:
            await message.answer(
                "<b>Добавить адрес VQR?</b>",
                reply_markup=command_address_keyboard()
            )

        else:
            score = round(db.get_score(message.from_user.id) * 0.01, 4)
            await message.answer(
                f"{address}\nВы можете запросить {score} VQR",
                reply_markup=command_pay_keyboard()
            )
            # await message.answer(
            #     "тут нужно выплату прикрутить еще!"
            # )

        # if "VQR" in message.text:
            # db.add_address(message.text, message.from_user.id)
        # curr_chat_id = message.chat.id
        # print(curr_chat_id)
        # if not db.chat_exists(curr_chat_id):
        #     db.add_chat(curr_chat_id)
