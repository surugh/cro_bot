import pydantic.error_wrappers
from aiogram import Router, F
from aiogram.types import Message

from databases.cro_db import Database
from private_functions import validate_address
from databases.cro_wordlist import word_definition
from handlers.start_command import command_start_handler
from keyboards.start_keyboard import command_pay_keyboard

router = Router()

db = Database("databases/cro_data.db")


@router.message(F.text)
async def word_handler(message: Message) -> None:
    """
    Handler will check messages fo hidden word

    """
    first_symbol = message.text[0]
    if first_symbol == "?":
        try:
            await message.answer(
                f"<b>{message.text[1:].capitalize()}</b> это:\n"
                f"{word_definition(message.text[1:].lower())}"
            )
        except pydantic.error_wrappers.ValidationError:
            await message.answer(
                "Слово отсутствует в словаре!\nИспользуйте синтаксис\n?слово"
            )
    if message.chat.type != 'private':
        hidden_word = db.get_word(message.chat.id)
        if hidden_word:
            word_lower = hidden_word.lower()
            word_replace = word_lower.replace('ё', 'е')
            message_lower = message.text.lower()
            message_replace = message_lower.replace('ё', 'е')
            if word_replace in message_replace:
                player_id = message.from_user.id
                if not db.user_exists(player_id):
                    db.add_user(player_id)
                if db.get_leader(message.chat.id) != player_id:
                    db.add_score(player_id)
                    await message.answer(
                        f"<b>{message.from_user.full_name}</b> | "
                        f"<b>{db.get_score(message.from_user.id)}</b> очков\n"
                        f"Угадал слово: <b>{db.get_word(message.chat.id)}</b>"
                    )
                else:
                    await message.answer(
                        f"<b>{message.from_user.full_name}</b> | "
                        f"<b>Больше не ведущий!</b>\n"
                        f"Раскрыл слово: <b>{db.get_word(message.chat.id)}</b>"
                    )
                db.del_leader(message.chat.id)
                db.del_word(message.chat.id)
                await command_start_handler(message)
    else:
        if "VQR" in message.text:
            if len(validate_address(message.text)) == 23:
                await message.answer(
                    "Адрес не валиден!\nПроверьте правильность введенных данных"
                )
            else:
                db.add_address(message.text, message.from_user.id)
                await message.answer(
                    f"{message.text}\n"
                    f"ваш текущий адрес для получения выплат успешно добавлен"
                )
                address = db.address_exists(message.from_user.id)
                score = round(db.get_score(message.from_user.id) * 0.01, 4)
                await message.answer(
                    f"{address}\nВы можете запросить {score} VQR",
                    reply_markup=command_pay_keyboard()
                )
