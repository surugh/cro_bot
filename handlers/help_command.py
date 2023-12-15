from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command(commands=['help']))
async def command_help_handler(message: Message) -> None:
    await message.answer(
        f'Игра в КРОКОДИЛА от криптоэнтузиастов! =)\n\n'
        f' Правила;\n'
        f'1 - Не используя ОДНОКОРЕННЫЕ слова, '
        f'ведущий загадывает полученное от бота слово.\n'
        f'2 - Задача участников отгадать это слово.\n'
        f'3 - Угадавший игрок должен взять роль ведущего и продолжить игру.\n'
        f'4 - Цикл повторить! =) ))\n\n'
        f' Играем в наших чатах:\n'
        f'@virtualquestchat\n'
        f'@crocodilling\n\n'
        f' Доступные команды:\n'
        f'/start - запуск\n'
        f'/help - вызов этой страницы\n'
        f'/stat - статистика\n'
        f'/chat  - группы с игрой (только в лс бота)\n'
        f'(! Ваш общий прогресс будет учитываться при игре в любой из групп)\n\n'
        f' Только для администраторов:\n'
        f'/restart - сброс ведущего\n\n'
        f'Как получать призы?\n'
        f'Получить кошелек у бота @vqr_bot\n'
        f'Или установить последнюю версию с '
        f'<a href="https://github.com/cryptadev/vqr/releases/tag/17.2.5">GitHub</a>\n\n'
        f'Добавляйте бота к себе в чат и играйте с друзьями - @pg_cro_bot\n'
        f'(боту необходимо дать минимальные админ-права '
        f'для доступа к сообщениям в группе)', disable_web_page_preview=True
    )
