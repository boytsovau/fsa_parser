from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold
from proxy_data import TOKEN
from main import get_declaration
# import json

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer('Введи номер декларации')


@dp.message_handler()
async def get_info(message: types.Message):
    await message.answer("Нужно подождать.....")

    result = get_declaration(message.text)

    if result:

        # with open("data/result_dec.json") as file:
        #     data = json.load(file)

        for item in result.values():
            for i in item:
                info = f"{hbold('Номер: ')} {i.get('number')}\n" \
                    f"{hbold('Дата регистрации: ')} {i.get('Register Date')}\n" \
                    f"{hbold('Заявитель: ')} {i.get('Applicant')}\n" \
                    f"{hbold('Производитель: ')} {i.get('Manufacturer')}\n" \
                    f"{hbold('Продукция: ')} {i.get('Production')}\n" \
                    f"{hbold('Схема: ')} {i.get('Схема')}\n" \
                    f"{hbold('Статус: ')} {i.get('Статус')}\n" \
                    f"{hbold('Ссылка: ')} https://pub.fsa.gov.ru/rds/declaration/view/{i.get('id')}/common\n" \
                    f"{hbold('============================')}\n"
                await message.answer(info)
    if result is None:
        await message.answer("Сервис не доступен, попробуйте позже")
    if not result:
        await message.answer("Нет информации")


def main():
    executor.start_polling(dp)


if __name__ == "__main__":
    main()
