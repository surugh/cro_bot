from aiogram import Router
from aiogram.types import CallbackQuery
from functions.public import refused_game

router = Router()


@router.callback_query(lambda c: c.data == 'restart')
async def command_restart_callback(callback: CallbackQuery) -> None:
    await refused_game(callback)
