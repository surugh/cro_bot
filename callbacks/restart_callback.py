from aiogram import Router
from aiogram import types  # , Bot

from databases.cro_db import Database

from handlers.start_command import command_start_handler

router = Router()

db = Database("databases/cro_data.db")


@router.callback_query(lambda c: c.data == 'restart')
async def command_restart_callback(callback: types.CallbackQuery):  # bot: Bot
    # admins_list = await bot.get_chat_administrators(callback.message.chat.id)
    # for admin in admins_list:
    #     if not admin.user.is_bot:
    #         if admin.user.id == db.get_leader(callback.message.chat.id):
    #             if callback.from_user.id == admin.user.id:
    #                 db.del_leader(callback.message.chat.id)
    #                 db.del_word(callback.message.chat.id)
    #                 await command_start_handler(callback.message)
    #             else:
    #                 await callback.answer("Вы не администратор")
    if callback.from_user.id == db.get_leader(callback.message.chat.id):
        db.del_leader(callback.message.chat.id)
        db.del_word(callback.message.chat.id)
        await callback.message.answer(
            f"{callback.from_user.full_name} отказался быть ведущим"
        )
        await command_start_handler(callback.message)
    else:
        await callback.answer("Вы не ведущий", show_alert=True)
    await callback.answer()
    # await callback.message.delete()
