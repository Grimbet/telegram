'''
Мой телеграмм-бот
@MyUrbanAndreyBot
Версия aiogram==3.16.0
Результат работы модуля смотри тут:
https://github.com/Grimbet/telegram/blob/main/user.png
'''

import asyncio #подключаем библиотеку для асинхронной работы
import config #подключим файл конфигурации, там наш API ключ находится
from aiogram import Bot, Dispatcher,F #подгружаем классы ТГ
from aiogram.types import Message,CallbackQuery,FSInputFile #класс для сообщений
from aiogram.filters import Command #подключаем класс для команд /start, /help и тд
from aiogram.filters.state import State, StatesGroup  #класс состояния юзера, и группа состояний
from aiogram.fsm.context import FSMContext #объект управления состояниями State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup #клавиатура и кнопки клавиатуры
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton # inline - клавиатура, кнопки прямо в тексте
import crud_functions


# подгружаем переменную TOKEN из config.py
API = config.TOKEN
# присваиваем ключ боту
bot = Bot(token = API)
dp = Dispatcher()

# подключаем БД
conn = crud_functions.connect_db()

#добавляем внешнюю клавиатуру с двумя кнопками
kb = ReplyKeyboardMarkup(keyboard=[
[KeyboardButton(text='Рассчитать'),KeyboardButton(text='Информация')],
[KeyboardButton(text='Купить'),KeyboardButton(text='Регистрация')],
],resize_keyboard=True)

#добавляем внутреннюю клавиатуру с двумя кнопками
km = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Расчет калорий',callback_data='calories'),
     InlineKeyboardButton(text='Формула расчёта',callback_data='formulas')]
    ])

#добавляем внутреннюю клавиатуру Product
km_product = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Продукт1',callback_data='product_buying'),
     InlineKeyboardButton(text='Продукт2',callback_data='product_buying'),
     InlineKeyboardButton(text='Продукт3',callback_data='product_buying'),
     InlineKeyboardButton(text='Продукт4',callback_data='product_buying')]
    ])


# объявляем класс для хранения данных
class UserState(StatesGroup):
    age = State()       # Возраст
    growth = State()    # Рост
    weight = State()    # Вес

# объявляем класс для хранения данных
class RegistrationState(StatesGroup):
    username = State()      # имя
    email= State()          # email
    age = State()           # Возраст


# обработка команды /start
@dp.message(Command('start'))
async def start(message: Message):
    await message.answer(f'Привет! Я бот помогающий твоему здоровью!',reply_markup=kb)

# обработка кнопки "Информация"
@dp.message(F.text =='Информация')
async def info(message: Message):
    await message.answer(f'Я бот для Вашего здоровья. \nНажмите кнопку "Рассчитать", чтобы начать работу!')

# обработка кнопки "Рассчитать"
@dp.message(F.text == "Рассчитать")
async def main_menu(message: Message):
    await message.answer(f'Выберите опцию:',reply_markup=km)

# обработка кнопки "Купить"
@dp.message(F.text == "Купить")
async def get_buying_list(message: Message):
    products = crud_functions.get_all_products(conn) # подключаем БД продуктов
    for product in products:
        with open(f'product{product[0]}.png','rb'):
            photo = FSInputFile(path=f'product{product[0]}.png')
            await message.answer_photo(photo ,f'Название: {product[1]}\nОписание: {product[2]}\nЦена: {product[3]}')
    await message.answer("Выберите продукт для покупки:",reply_markup=km_product)

# обработка инлайн-кнопки "Продукт1...4"
@dp.callback_query(F.data=="product_buying")
async def send_confirm_message(call:CallbackQuery):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer() #отжатие кнопки

# обработка инлайн-кнопки "Формула расчёта"
@dp.callback_query(F.data=="formulas")
async def get_formulas(call:CallbackQuery):
    await call.message.answer('Формула расчета для мужчин: \n10 х вес(кг) + 6,25 x рост(см) – 5 х возраст(г) + 5')
    await call.answer() #отжатие кнопки

# обработка инлайн-кнопки "Расчет калорий"
@dp.callback_query(F.data=="calories")
async def set_age(call:CallbackQuery,state:FSMContext):
    await call.message.answer(f"Введите свой возраст:(лет)")
    await state.set_state(UserState.age) #меняем состояние на UserState.age
    await call.answer() #отжатие кнопки

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

# обработка кнопки "Регистрация"
@dp.message(F.text == "Регистрация")
async def sing_up(message: Message, state:FSMContext):
    await message.answer(f'Введите имя пользователя (только латинский алфавит):')
    await state.set_state(RegistrationState.username) #меняем состояние

# обработчик состояния username
@dp.message(RegistrationState.username)
async def set_username(message: Message,state:FSMContext):
    await state.update_data(username=message.text)
    if crud_functions.is_included(conn,message.text):
        await message.answer(f"Пользователь существует, введите другое имя")
    else:
        await message.answer(f"Введите свой email:")
        await state.set_state(RegistrationState.email) #меняем состояние

# обработчик состояния email
@dp.message(RegistrationState.email)
async def set_email(message: Message,state:FSMContext):
    await message.answer(f"Введите свой возраст:")
    await state.update_data(email=message.text)
    await state.set_state(RegistrationState.age) #меняем состояние

# обработчик состояния age
@dp.message(RegistrationState.age)
async def set_age(message: Message,state:FSMContext):
    await state.update_data(age=message.text)
    data = await state.get_data()  # импортируем в data список состояний
    crud_functions.add_user(conn,data['username'],data['email'],data['age'])
    await message.answer(f"Регистрация успешно завершена...\n"
                         f"User: {data['username']}| Email: {data['email']} | Age: {data['age']}")
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