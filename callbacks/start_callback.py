from aiogram import types
from aiogram import Router

from databases.cro_db import Database

from keyboards.start_keyboard import callback_start_keyboard

router = Router()

db = Database("databases/cro_data.db")


@router.callback_query(lambda c: c.data == 'command_start_handler')
async def command_start_callback(callback: types.CallbackQuery):
    db.add_leader(callback.from_user.id, callback.message.chat.id)
    await callback.message.answer(
        f"Ведущий <b>{callback.from_user.full_name}</b> | "
        f"@{callback.from_user.username}",
        # f"{db.get_score(callback.from_user.id)}</b> очков",
        reply_markup=callback_start_keyboard()
    )
    await callback.message.delete()
