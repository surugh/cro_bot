from aiogram import types
from aiogram import Router

from databases.cro_db import Database
from private_functions import send_funds
from databases.cro_wordlist import word_choice

router = Router()

db = Database("databases/cro_data.db")


@router.callback_query(lambda c: c.data == 'new_word')
async def new_word(callback: types.CallbackQuery) -> None:
    hidden_word = word_choice()
    db.add_word(hidden_word.capitalize(), callback.message.chat.id)
    if db.get_leader(callback.message.chat.id) == callback.from_user.id:
        await callback.answer(f"{hidden_word.capitalize()}", show_alert=True)
    else:
        await callback.answer("Вы не ведущий", show_alert=True)


@router.callback_query(lambda c: c.data == 'remind')
async def remind_word(callback: types.CallbackQuery) -> None:
    remind = db.get_word(callback.message.chat.id)
    if db.get_leader(callback.message.chat.id) == callback.from_user.id:
        if remind:
            await callback.answer(f"{remind.capitalize()}", show_alert=True)
        else:
            await callback.answer("Слово еще не выбрано")
    else:
        await callback.answer("Вы не ведущий", show_alert=True)


@router.callback_query(lambda c: c.data == 'command_address_handler')
async def address_handler(callback: types.CallbackQuery) -> None:
    await callback.answer("Отправьте боту ваш адрес VQR", show_alert=True)


@router.callback_query(lambda c: c.data == 'command_pay_handler')
async def pay_handler(callback: types.CallbackQuery) -> None:
    address = db.get_address(callback.from_user.id)
    score = round(db.get_score(callback.from_user.id) * 0.01, 4)
    if score >= 0.01:
        pay_hash = send_funds(address, score)
        await callback.message.answer(f"Выплата:\n{address}\n{score}\nHASH:")
        await callback.message.answer(f"{pay_hash}")
        db.del_score(callback.from_user.id)
    else:
        await callback.message.answer("Выплаты доступны от 0,01 VQR")
