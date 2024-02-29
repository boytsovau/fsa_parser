import logging
import datetime
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold
from main import get_declaration

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG, filename="bot.log")

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer('Введи номер декларации')


@dp.message_handler()
async def get_info(message: types.Message):
    await message.answer("Нужно подождать.....")
    user_status = await bot.get_chat_member(chat_id=message.chat.id,
                                            user_id=message.from_user.id)
    with open("users.log", "a") as file:
        date = datetime.datetime.now()
        file.write(str(date) + ':' + str(user_status) + '\n')

    result = get_declaration(message.text)

    try:
        if result:
            for item in result.values():
                for i in item:
                    info = f"{hbold('Номер: ')} {i.get('number')}\n" \
                        f"{hbold('Дата регистрации: ')} {i.get('Register Date')}\n" \
                        f"{hbold('Дата окончания: ')} {i.get('Issue Date')}\n" \
                        f"{hbold('Заявитель: ')} {i.get('Applicant')}\n" \
                        f"{hbold('Производитель: ')} {i.get('Manufacturer')}\n" \
                        f"{hbold('Продукция: ')} {i.get('Production')}\n" \
                        f"{hbold('Схема: ')} {i.get('Схема')}\n" \
                        f"{hbold('Статус: ')} {i.get('Статус')}\n" \
                        f"{hbold('Ссылка: ')} https://pub.fsa.gov.ru/rds/declaration/view/{i.get('id')}/common\n" \
                        f"{hbold('============================')}\n"
                    await message.answer(info)
        if result is None:
            await message.answer("Сайт Федеральной службы по аккредетации не \
                                доступен, попробуйте позже")
        if result is False:
            await message.answer("Нет информации")
    except Exception:
        await message.answer("Попробуйте позже")


def main():
    executor.start_polling(dp)


if __name__ == "__main__":
    main()
