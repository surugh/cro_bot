from aiogram import Router, types

router = Router()


@router.callback_query(lambda c: c.data == 'command_help_handler')
async def command_help_callback(callback: types.CallbackQuery):
    await callback.message.answer(
        f'Игра в КРОКОДИЛА от криптоэнтузиастов! =)\n\n'
        f'Доступные команды:\n'
        f'/start - запуск\n'
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
