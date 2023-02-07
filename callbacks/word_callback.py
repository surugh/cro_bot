from aiogram import types, Router
from functions.private import pay
from functions.public import get_new_word, remind_hidden

router = Router()


@router.callback_query(lambda c: c.data == 'new_word')
async def new_word(callback: types.CallbackQuery) -> None:
    await get_new_word(callback)


@router.callback_query(lambda c: c.data == 'remind')
async def remind_word(callback: types.CallbackQuery) -> None:
    await remind_hidden(callback)


@router.callback_query(lambda c: c.data == 'command_address_handler')
async def address_handler(callback: types.CallbackQuery) -> None:
    await callback.answer("Отправьте боту ваш адрес VQR", show_alert=True)


@router.callback_query(lambda c: c.data == 'command_pay_handler')
async def pay_handler(callback: types.CallbackQuery) -> None:
    await pay(callback)
