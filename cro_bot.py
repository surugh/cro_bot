import logging

from aiogram import Bot, Dispatcher

from handlers import start_command, restart_command, word_handler, \
    stat_command, help_command, chat_command
from callbacks import start_callback, restart_callback, word_callback, \
    help_callback

# CroBot
TOKEN = ""

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# handler = logging.FileHandler(f"{__name__}.log", mode='w')
# formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.info(f"Testing the custom logger for module {__name__}...")
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
