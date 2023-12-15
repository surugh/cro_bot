import random
import secrets
import time

from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest

from pydantic.error_wrappers import ValidationError

from databases import crud
from databases.cro_wordlist import word_choice, word_definition
from functions.private import send_funds
from keyboards.start_keyboard import command_start_keyboard, \
    callback_start_keyboard


async def remind_hidden(callback: CallbackQuery) -> None:
    remind = crud.get_hidden_word(callback.message.chat.id)
    if crud.get_leader(callback.message.chat.id) == callback.from_user.id:
        if remind:
            await callback.answer(f"{remind.capitalize()}", show_alert=True)
        else:
            await callback.answer("Слово еще не выбрано")
    else:
        await callback.answer("Вы не ведущий", show_alert=True)


async def get_new_word(callback: CallbackQuery) -> None:
    if crud.get_leader(callback.message.chat.id) == callback.from_user.id:
        hidden_word = word_choice()
        crud.add_word(hidden_word.capitalize(), callback.message.chat.id)
        await callback.answer(f"{hidden_word.capitalize()}", show_alert=True)
    else:
        await callback.answer("Вы не ведущий", show_alert=True)


async def top_players(message: Message, bot: Bot) -> None:
    all_players = crud.get_players_data()
    chat_players = []
    for player in all_players:
        # print(player.user_id)
        try:
            chat_player = await bot.get_chat_member(
                message.chat.id, player.user_id
            )
            if chat_player.status != 'left':
                chat_players.append((chat_player.user.id, int(player.score)))
        except TelegramBadRequest:
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


async def start_game(message: Message) -> None:
    if not crud.chat_exists(message.chat.id):
        crud.add_chat(message.chat.id)
    if not crud.get_leader(message.chat.id):
        await message.answer(
            "<b>Хочешь быть ведущим?</b>",
            reply_markup=command_start_keyboard()
        )
    else:
        await message.answer("Ведущий уже выбран /restart ?")


async def new_round(callback: CallbackQuery) -> None:
    crud.add_leader(callback.from_user.id, callback.message.chat.id)
    await callback.message.answer(
        f"Ведущий <b>{callback.from_user.full_name}</b> | "
        f"@{callback.from_user.username}",
        # f"{db.get_score(callback.from_user.id)}</b> очков",
        reply_markup=callback_start_keyboard()
    )
    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass


async def refused_game(callback: CallbackQuery) -> None:
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


async def restart_game(message: Message, bot: Bot) -> None:
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


def word_similar(message: Message, hidden_word: str) -> bool:
    if hidden_word:
        word_lower = hidden_word.lower()
        word_replace = word_lower.replace('ё', 'е')
        message_lower = message.text.lower()
        message_replace = message_lower.replace('ё', 'е')
        if word_replace in message_replace:
            return True


async def delete_msg(bot: Bot, chat_id: int, message_id: int) -> None:
    time.sleep(10)
    await bot.delete_message(chat_id, message_id)


async def word_catcher(message: Message) -> None:
    hidden_word = crud.get_hidden_word(message.chat.id)
    if word_similar(message, hidden_word):
        if not crud.user_exists(message.from_user.id):
            crud.add_user(message.from_user.id)
        if crud.get_leader(message.chat.id) != message.from_user.id:
            dice = [3, 5, 7, 9, 13, 125]
            weights = [100, 50, 25, 10, 5, 2]
            seq = random.choices(dice, weights, k=6)
            multipler = secrets.choice(seq)
            if multipler == 125:
                await message.answer("BIG WIN")
            if multipler == 13:
                await message.answer("GREAT")
            crud.add_score(message.from_user.id, multipler=multipler)
            score = crud.get_score(message.from_user.id)
            if score >= 1000:
                address = crud.address_exists(message.from_user.id)
                if not address:
                    await message.answer(
                        f'@{message.from_user.username} '
                        f'Ваш адрес VQR не найден'
                    )
                else:
                    amount = round(score * 0.01, 4)
                    pay_hash = send_funds(address[0], amount)
                    href = f"https://masternode.vqr.quest/tx.php?hash=" \
                           f"{pay_hash}"
                    await message.answer(
                        f"Выплата:\n{address}\n"
                        f"<a href={href}>Txid:</a> {amount} VQR",
                        disable_web_page_preview=True
                    )
                    # await message.answer(f"{pay_hash}")
                    crud.del_score(message.from_user.id)
            if message.from_user.id == 2091369970:
                await message.answer("blacklisted user, ignored")
                crud.del_score(message.from_user.id)
            else:
                await message.answer(
                    f"<b>{message.from_user.full_name}</b> | "
                    f"<b>{score}</b> очков\n"
                    f"Угадал слово: <b>{hidden_word}</b> | x{multipler}"
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


async def definition(message: Message) -> None:
    try:
        word = message.text[1:]
        if word_definition(word):
            await message.answer(
                f"<b>{word.capitalize()}</b> это:\n"
                f"{word_definition(word.lower().strip())}"
            )
        else:
            if " " in word:
                await message.answer(
                    f"https://google.com/search?q="
                    f"{word.replace(' ', '+')}"
                )
            else:
                await message.answer(
                    f"https://google.com/search?q=слово+{word}"
                )
    except ValidationError:
        await message.answer(
            "Слово не найдено!\nИспользуйте синтаксис\n?слово"
        )


async def public_word_definition(message: Message) -> None:
    first_symbol = message.text[0]
    symbols = ["?", "*"]
    for symbol in symbols:
        if first_symbol == symbol:
            if len(message.text) > 1:
                if message.chat.id == -1001228658207:  # Vqroom
                    if first_symbol == "?":
                        await message.answer(
                            "Пожалуйста, используйте * вместо ? в этом чате"
                        )
                    else:
                        await definition(message)
                else:
                    await definition(message)
