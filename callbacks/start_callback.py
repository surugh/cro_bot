from aiogram import types, Router
from functions.public import new_round
router = Router()


@router.callback_query(lambda c: c.data == 'command_start_handler')
async def command_start_callback(callback: types.CallbackQuery):
    await new_round(callback)
