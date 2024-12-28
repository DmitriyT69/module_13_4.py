from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters.builtin import Text

import asyncio

token = "0000000000:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()  # возраст
    growth = State()  # рост
    weight = State()  # вес


@dp.message_handler(Text(equals=['Calories'], ignore_case=True))
async def set_age(message):
    await message.answer('Введите свой возраст (лет):')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    try:
        await state.update_data(age=float(message.text))
    except ValueError:
        await message.answer('Введите свой возраст (лет):')
        await UserState.age.set()
    else:
        await message.answer('Введите свой рост (см):')
        await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    try:
        await state.update_data(growth=float(message.text))
    except ValueError:
        await message.answer('Введите свой рост (см):')
        await UserState.growth.set()
    else:
        await message.answer('Введите свой вес (кг):')
        await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    try:
        await state.update_data(weight=float(message.text))
    except ValueError:
        await message.answer('Введите свой вес (кг):')
        await UserState.weight.set()
    else:
        data = await state.get_data()
        # Resting energy expenditure
        REE = 10 * data['weight'] \
            + 6.25 * data['growth'] \
            - 5 * data['age'] + 5
        await message.answer(
            f'Ваша суточная норма {round(REE, 2)} килокалорий')
        await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(
        'Привет! Я бот помогающий вашему здоровью.'
        ' Введите слово Calories, чтобы узнать вашу суточную норму'
        ' потребления калорий')


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)