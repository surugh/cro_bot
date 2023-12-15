from aiogram import Router
from aiogram.types import CallbackQuery
from functions.public import new_round
router = Router()


@router.callback_query(lambda c: c.data == 'command_start_handler')
async def command_start_callback(callback: CallbackQuery) -> None:
    await new_round(callback)
