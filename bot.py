import logging
import datetime
import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, enums, types
from aiogram import F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.client.bot import DefaultBotProperties
from logging.handlers import RotatingFileHandler
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.markdown import hbold
from main import Declaration
from certificate import Certificate

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = RotatingFileHandler('bot.log', maxBytes=1000000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',)
handler.setFormatter(formatter)

logger.addHandler(handler)


bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=enums.ParseMode.HTML))
dp = Dispatcher()


class FindInfo(StatesGroup):
    decl_num = State()
    decl_find = State()
    sert_num = State()
    sert_find = State()


@dp.message(CommandStart())
async def start(message: Message):
    # await message.answer('Введите номер декларации')
    kb = [
            [
                types.KeyboardButton(text="Декларации"),
                types.KeyboardButton(text="Сертификаты")
            ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.answer('Выберите реестр', reply_markup=keyboard)


@dp.message(F.text.lower() == "декларации")
async def get_answer(message: Message, state: FSMContext):
    await message.answer("Введите номер декларации")
    await state.set_state(FindInfo.decl_num)


@dp.message(F.text.lower() == "сертификаты")
async def get_answer2(message: Message, state: FSMContext):
    await message.answer("Введите номер сертификата")
    await state.set_state(FindInfo.sert_num)


@dp.message(FindInfo.decl_num)
async def get_info(message: Message, state: FSMContext):
    await message.answer("Нужно подождать.....")
    await state.set_state(FindInfo.decl_find)
    user_status = await bot.get_chat_member(chat_id=message.chat.id,
                                            user_id=message.from_user.id)
    with open("users.log", "a") as file:
        date = datetime.datetime.now()
        file.write(str(date) + ':' + str(user_status) + '\n')

    dec = Declaration(message.text)
    result = dec.get_declaration()

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
                        f"{hbold('Схема: ')} {i.get('Scheme')}\n" \
                        f"{hbold('Статус: ')} {i.get('Status')}\n" \
                        f"{hbold('Ссылка: ')} https://pub.fsa.gov.ru/rds/declaration/view/{i.get('id')}/common\n" \
                        f"{hbold('============================')}\n"
                    await message.answer(info)
        if result is None:
            await message.answer('''Сайт Федеральной службы по аккредетации не
                                доступен, попробуйте позже''')
        if result is False:
            await message.answer("Нет информации")
    except Exception:
        await message.answer("Попробуйте позже")
    await message.answer('Выберите реестр')
    await state.clear()


@dp.message(FindInfo.sert_num)
async def get_info2(message: Message, state: FSMContext):
    await message.answer("Нужно подождать.....")
    await state.set_state(FindInfo.sert_find)
    user_status = await bot.get_chat_member(chat_id=message.chat.id,
                                            user_id=message.from_user.id)
    with open("users.log", "a") as file:
        date = datetime.datetime.now()
        file.write(str(date) + ':' + str(user_status) + '\n')

    dec = Certificate(message.text)
    result = dec.get_certificate()

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
                        f"{hbold('Схема: ')} {i.get('Scheme')}\n" \
                        f"{hbold('Статус: ')} {i.get('Status')}\n" \
                        f"{hbold('Ссылка: ')} https://pub.fsa.gov.ru/rss/certificate/view/{i.get('id')}/baseInfo\n" \
                        f"{hbold('============================')}\n"
                    await message.answer(info)
                    
        if result is None:
            await message.answer('''Сайт Федеральной службы по аккредетации не
                                доступен, попробуйте позже''')
        if result is False:
            await message.answer("Нет информации")
    except Exception:
        await message.answer("Попробуйте позже")
    await message.answer('Выберите реестр')
    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
