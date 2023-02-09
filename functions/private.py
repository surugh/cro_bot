import os
import time

from databases import crud
from keyboards.start_keyboard import command_pay_keyboard, \
    command_address_keyboard


def send_funds(address, quantity):
    os.system("cd")
    time.sleep(1)
    cmd = f"/home/ubuntu/./vqr-cli sendtoaddress {address} {quantity}"
    send = os.popen(cmd).read()
    return send


def validate_address(address):
    os.system("cd")
    time.sleep(1)
    cmd = f"/home/ubuntu/./vqr-cli validateaddress {address}"
    send = os.popen(cmd).read()
    return send


async def pay(callback):
    address = crud.get_address(callback.from_user.id)
    score = round(crud.get_score(callback.from_user.id) * 0.01, 4)
    if score >= 0.01:
        pay_hash = send_funds(address, score)
        await callback.message.answer(f"Выплата:\n{address}\n{score}\nHASH:")
        await callback.message.answer(f"{pay_hash}")
        crud.del_score(callback.from_user.id)
    else:
        await callback.message.answer("Выплаты доступны от 0,01 VQR")


async def propose_pay(message):
    address = crud.get_address(message.from_user.id)
    score = round(crud.get_score(message.from_user.id) * 0.01, 4)
    await message.answer(
        f"Вы можете запросить {score} VQR\n"
        f"на ваш текущий адрес для выплат\n\n{address}\n\n"
        f"Для смены адреса отправьте боту сообщением новый адрес",
        reply_markup=command_pay_keyboard()
    )


async def check_address(message):
    address = crud.address_exists(message.from_user.id)
    if not address:
        await message.answer(
            "<b>Добавить адрес VQR?</b>",
            reply_markup=command_address_keyboard()
        )

    else:
        await propose_pay(message)


async def add_user_address(message):
    if "VQR" in message.text:
        validation = validate_address(message.text)
        if len(validation) == 0:
            await message.answer(
                "Невозможно проверить адрес!\n"
                "vqr-cli не найден"
            )
        else:
            if len(validation) == 23:
                await message.answer(
                    "Адрес не валиден!\n"
                    "Проверьте правильность введенных данных"
                )
            else:
                crud.add_address(message.text, message.from_user.id)
                await message.answer(
                    f"Ваш новый адрес\n\n{message.text}\n\nуспешно добавлен"
                )
                await propose_pay(message)
