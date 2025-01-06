'''
Мой телеграмм-бот
@MyUrbanAndreyBot
Версия aiogram==3.16.0

Результаты работы модуля смотри тут:
https://github.com/Grimbet/telegram/blob/main/calories.png

'''

import asyncio #подключаем библиотеку для асинхронной работы
import config #подключим файл конфигурации, там наш API ключ находится
from aiogram import Bot, Dispatcher,F #подгружаем классы ТГ
from aiogram.types import Message #класс для сообщений
from aiogram.filters import Command #подключаем класс для команд /start, /help и тд
from aiogram.filters.state import State, StatesGroup  #класс состояния юзера, и группа состояний
from aiogram.fsm.context import FSMContext #объект управления состояниями State

# подгружаем переменную TOKEN из config.py
API = config.TOKEN
# присваиваем ключ боту
bot = Bot(token = API)
dp = Dispatcher()

# объявляем класс для хранения данных
class UserState(StatesGroup):
    age = State()       # Возраст
    growth = State()    # Рост
    weight = State()    # Вес


# обработка команды /start
@dp.message(Command('start'))
async def start(message: Message):
    await message.answer(f'Привет! Я бот помогающий твоему здоровью. \n Напиши слово "Calories", если хочешь рассчитать свои калории на день!')

# обработка сообщения <Calories>
@dp.message(F.text == "Calories")
async def set_age(message: Message,state:FSMContext):
    await message.answer(f"Введите свой возраст:(лет)")
    await state.set_state(UserState.age) #меняем состояние на UserState.age

# обработчик состояния ввода возраста
@dp.message(UserState.age)
async def set_growth(message: Message,state:FSMContext):
    await message.answer(f"Введите свой рост:(см)")
    await state.update_data(age = message.text)
    await state.set_state(UserState.growth) #меняем состояние

# обработчик состояния ввода роста
@dp.message(UserState.growth)
async def set_weight(message: Message,state:FSMContext):
    await message.answer(f"Введите свой вес: (кг)")
    await state.update_data(growth=message.text)
    await state.set_state(UserState.weight) #меняем состояние

# обработчик состояния ввода веса
@dp.message(UserState.weight)
async def send_calories(message: Message,state:FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data() #импортируем в data список состояний
    formula = 10*int(data['weight'])+6.25*int(data['growth'])-5*int(data['age'])+5
    await message.answer(f"Ваши данные: вес={data['weight']} кг, рост={data['growth']} см, возраст={data['age']} лет\n"
                         f"Ваша норма калорий на день составляет: {formula} кал")
    await state.clear() #очищаем состояние пользователя

# обработка любых сообщений боту
@dp.message()
async def all_message(message: Message):
    await message.answer(f'Введите команду /start, чтобы начать общение.')

# Эхо-бот. Режим ожидания...
async def main():
    #skip_updates указывает, что нужно пропускать обновления, которые пришли до запуска бота
    await dp.start_polling(bot,skip_updates=True)

#запускаем бота
if __name__ == '__main__':
    asyncio.run(main())