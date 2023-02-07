from aiogram import types, Router
from functions.public import refused_game

router = Router()


@router.callback_query(lambda c: c.data == 'restart')
async def command_restart_callback(callback: types.CallbackQuery):
    await refused_game(callback)
