import os
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from handlers import start_command, restart_command, word_handler, \
    stat_command, help_command, chat_command
from callbacks import start_callback, restart_callback, word_callback, \
    help_callback

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    TOKEN = os.getenv('TOKEN')

logging.basicConfig(
    level=logging.WARNING, filename="cro_log.log",
    format="[%(asctime)s] %(levelname)s %(message)s"
)


def main() -> None:
    bot = Bot(TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    dp.include_router(start_command.router)
    dp.include_router(restart_command.router)
    dp.include_router(stat_command.router)
    dp.include_router(help_command.router)
    dp.include_router(chat_command.router)
    dp.include_router(start_callback.router)
    dp.include_router(restart_callback.router)
    dp.include_router(help_callback.router)
    dp.include_router(word_handler.router)
    dp.include_router(word_callback.router)

    dp.run_polling(bot)


if __name__ == "__main__":
    main()
