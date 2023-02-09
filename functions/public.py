from aiogram import exceptions
import pydantic.error_wrappers

from databases import crud
from databases.cro_wordlist import word_choice, word_definition
from keyboards.start_keyboard import command_start_keyboard, \
    callback_start_keyboard


async def remind_hidden(callback):
    remind = crud.get_hidden_word(callback.message.chat.id)
    if crud.get_leader(callback.message.chat.id) == callback.from_user.id:
        if remind:
            await callback.answer(f"{remind.capitalize()}", show_alert=True)
        else:
            await callback.answer("Слово еще не выбрано")
    else:
        await callback.answer("Вы не ведущий", show_alert=True)


async def get_new_word(callback):
    if crud.get_leader(callback.message.chat.id) == callback.from_user.id:
        hidden_word = word_choice()
        crud.add_word(hidden_word.capitalize(), callback.message.chat.id)
        await callback.answer(f"{hidden_word.capitalize()}", show_alert=True)
    else:
        await callback.answer("Вы не ведущий", show_alert=True)


async def top_players(message, bot):
    all_players = crud.get_players_data()
    chat_players = []
    for player in all_players:
        print(player.user_id)
        try:
            chat_player = await bot.get_chat_member(
                message.chat.id, player.user_id
            )
            if chat_player.status != 'left':
                chat_players.append((chat_player.user.id, int(player.score)))
        except exceptions.TelegramBadRequest:
            pass
    sort_players = sorted(
        chat_players, key=lambda c_player: c_player[1], reverse=True
    )
    top = []
    x = 0
    for _ in sort_players[0:7]:
        x = x + 1
        p = await bot.get_chat_member(message.chat.id, _[0])
        top.append(f"{x}. {p.user.full_name} - {_[1]}")
    text = '\n'.join(top)
    await message.answer(f"ТОП 7 игроков этой группы:\n{text}")


async def start_game(message):
    if not crud.chat_exists(message.chat.id):
        crud.add_chat(message.chat.id)
    if not crud.get_leader(message.chat.id):
        await message.answer(
            "<b>Хочешь быть ведущим?</b>",
            reply_markup=command_start_keyboard()
        )
    else:
        await message.answer("Ведущий уже выбран /restart ?")


async def new_round(callback):
    crud.add_leader(callback.from_user.id, callback.message.chat.id)
    await callback.message.answer(
        f"Ведущий <b>{callback.from_user.full_name}</b> | "
        f"@{callback.from_user.username}",
        # f"{db.get_score(callback.from_user.id)}</b> очков",
        reply_markup=callback_start_keyboard()
    )
    try:
        await callback.message.delete()
    except exceptions.TelegramBadRequest:
        pass


async def refused_game(callback):
    if callback.from_user.id == crud.get_leader(callback.message.chat.id):
        crud.del_leader(callback.message.chat.id)
        crud.del_word(callback.message.chat.id)
        await callback.message.answer(
            f"{callback.from_user.full_name} отказался быть ведущим"
        )
        await start_game(callback.message)
    else:
        await callback.answer("Вы не ведущий", show_alert=True)
    await callback.answer()


async def restart_game(message, bot):
    admins = await bot.get_chat_administrators(message.chat.id)
    admins_id_list = []
    for admin in admins:
        if not admin.user.is_bot:
            admins_id_list.append(admin.user.id)
    if message.from_user.id in admins_id_list:
        crud.del_leader(message.chat.id)
        crud.del_word(message.chat.id)
        await message.answer(
            f"{message.from_user.full_name} перезапустил игру"
        )
        await start_game(message)
    else:
        await message.answer(
            f"{message.from_user.full_name} Вы не администратор"
        )


async def word_catcher(message):
    # hidden_word = db.get_word(message.chat.id)
    hidden_word = crud.get_hidden_word(message.chat.id)
    if hidden_word:
        word_lower = hidden_word.lower()
        word_replace = word_lower.replace('ё', 'е')
        message_lower = message.text.lower()
        message_replace = message_lower.replace('ё', 'е')
        if word_replace in message_replace:
            player_id = message.from_user.id
            if not crud.user_exists(player_id):
                crud.add_user(player_id)
            if crud.get_leader(message.chat.id) != player_id:
                crud.add_score(player_id)
                await message.answer(
                    f"<b>{message.from_user.full_name}</b> | "
                    f"<b>{crud.get_score(message.from_user.id)}</b> очков\n"
                    f"Угадал слово: <b>{hidden_word}</b>"
                )
            else:
                await message.answer(
                    f"<b>{message.from_user.full_name}</b> | "
                    f"<b>Больше не ведущий!</b>\n"
                    f"Раскрыл слово: <b>{hidden_word}</b>"
                )
            crud.del_leader(message.chat.id)
            crud.del_word(message.chat.id)
            await start_game(message)


async def public_word_definition(message):
    first_symbol = message.text[0]
    if first_symbol == "?":
        try:
            await message.answer(
                f"<b>{message.text[1:].capitalize()}</b> это:\n"
                f"{word_definition(message.text[1:].lower().strip())}"
            )
        except pydantic.error_wrappers.ValidationError:
            await message.answer(
                "Слово отсутствует в словаре!\nИспользуйте синтаксис\n?слово"
            )
