from aiogram import Router
from aiogram.filters import Command

router = Router()


@router.message(Command(commands=['help']))
async def command_help_handler(message):
    await message.answer(
        f'Игра в КРОКОДИЛА от криптоэнтузиастов! =)\n\n'
        f'Доступные команды:\n'
        f'/start - запуск\n'
        f'/chat - группы с игрой\n'
        f'/help - вызов этой страницы\n'
        f'/stat - статистика\n'
        f'Только для администраторов:\n'
        f'/restart - сброс ведущего\n\n'
        f'Играем в нашем чате и выигрываем криптовалюту! - '
        f'https://t.me/virtualquestchat\n'
        f'А призы в Наших событиях вы можете получить используя кошелек - '
        f'https://t.me/vqr_bot\n'
        f'Добавляйте бота к себе в чат и играйте с друзьями - '
        f'https://t.me/pg_cro_bot\n\n'
    )
    await message.answer(
        f'В вашей группе нет активности?\n'
        f'А вы не знаете где поиграть?\n'
        f'выполните команду /chat\n'
        f'для поиска групп с играми\n\n'
        f' ! Ваш общий прогресс будет учитываться при игре в любой из групп '
    )
