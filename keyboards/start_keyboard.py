from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def command_start_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="ЖМИ", callback_data="command_start_handler")
    )
    return builder.as_markup()


def callback_start_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Выбрать \ Сменить слово",
                             callback_data="new_word")
    )
    builder.row(
        InlineKeyboardButton(text="Отказаться", callback_data='restart'),
        InlineKeyboardButton(text="Напомнить", callback_data="remind")
    )
    return builder.as_markup()


def command_address_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Добавить адрес",
            callback_data="command_address_handler"
        )
    )
    return builder.as_markup()


def command_pay_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Получить выплату",
            callback_data="command_pay_handler"
        )
    )
    return builder.as_markup()
