'''
Мой телеграмм-бот
@MyUrbanAndreyBot

Версия aiogram==3.16.0

Результат работы данного модуля можно посмотреть тут:
https://github.com/Grimbet/telegram/blob/main/test_bot.png

'''

import asyncio #подключаем библиотеку для асинхронной работы
import config #подключим файл конфигурации, там наш API ключ находится
from aiogram import Bot, Dispatcher, types #подгружаем классы ТГ
from aiogram.filters import Command #подключаем команды ТГ

#подгружаем переменную TOKEN из config.py
API = config.TOKEN
#присваиваем ключ боту
bot = Bot(token = API)
dp = Dispatcher()

#эта команда /start
@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer(f'Привет! Я бот помогающий твоему здоровью.')

#это функция обработки любых сообщений
@dp.message()
async def all_message(message: types.Message):
        await message.answer(f'Введите команду /start, чтобы начать общение.')

#эхо-бот. функция в режиме ожидания...
async def main():
    #skip_updates указывает, что нужно пропускать обновления, которые пришли до запуска бота
    await dp.start_polling(bot,skip_updates=True)

#запускаем
if __name__ == '__main__':
    asyncio.run(main())