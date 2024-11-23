from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from apikeyBot import api
from aiogram.dispatcher.filters.state import State, StatesGroup

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью. Напиши мне "Калории" или "Calories"')


'''Функцию set_age(message):
Оберните её в message_handler, который реагирует на текстовое сообщение 'Calories'.
Эта функция должна выводить в Telegram-бот сообщение 'Введите свой возраст:'.
После ожидать ввода возраста в атрибут UserState.age при помощи метода set.'''


@dp.message_handler(text=['Calories', 'Калории'])
async def set_age(message):
    await message.answer('Введите свой возраст, пожалуйста')
    await UserState.age.set()


'''Функцию set_growth(message, state):
Оберните её в message_handler, который реагирует на переданное состояние UserState.age.
Эта функция должна обновлять данные в состоянии age на message.text (написанное пользователем сообщение).
Используйте метод update_data.
Далее должна выводить в Telegram-бот сообщение 'Введите свой рост:'.
После ожидать ввода роста в атрибут UserState.growth при помощи метода set.'''


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост, пожалуйста')
    await UserState.growth.set()


'''Функцию set_weight(message, state):
Оберните её в message_handler, который реагирует на переданное состояние UserState.growth.
Эта функция должна обновлять данные в состоянии growth на message.text (написанное пользователем сообщение).
Используйте метод update_data.
Далее должна выводить в Telegram-бот сообщение 'Введите свой вес:'.
После ожидать ввода роста(ВЕСА) в атрибут UserState.weight при помощи метода set.'''


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес, пожалуйста')
    await UserState.weight.set()


'''Функцию send_calories(message, state):
Оберните её в message_handler, который реагирует на переданное состояние UserState.weight.
Эта функция должна обновлять данные в состоянии weight на message.text (написанное пользователем сообщение).
Используйте метод update_data.
Далее в функции запомните в переменную data все ранее введённые состояния при помощи state.get_data().
Используйте упрощённую формулу Миффлина - Сан Жеора для подсчёта нормы калорий
(для женщин или мужчин - на ваше усмотрение).
Данные для формулы берите из ранее объявленной переменной data по ключам age, growth и weight соответственно.
Результат вычисления по формуле отправьте ответом пользователю в Telegram-бот.
Финишируйте машину состояний методом finish()'''


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = state.get_data
    try:
        age = int(data['age'])
        weight = int(data['weight'])
        growth = int(data['growth'])
    except:
        await message.answer(f'Не могу конвертировать введенные значения в числа.')
        await state.finish()
        return
    formula = 9.99*weight+6.25*growth-4.92*age-161
    await message.answer(f'Ваша норма калорий в день {formula}')
    await state.finish()


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
