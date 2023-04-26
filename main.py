import asyncio

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
import time
import schedule
from datetime import datetime
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ParseMode
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import random
import aiogram.utils.markdown as md
import random
import schedule
import time

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton
from settings import TOKEN



bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

quotes = []
with open('Quotes.txt') as f:
    for i in range(30):
        quotes.append(f.readline().replace('\n',''))
print('Готово')
print(quotes)



@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    kb = [[
        types.KeyboardButton(text='Изм. время увед.'),
        types.KeyboardButton(text='Получить цитату сейчас')
    ]]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Стартовые действия',
        one_time_keyboard = True,

    )
    if datetime.now().minute > 1:
        min = datetime.now().minute
    else:
        min = '0' + str(datetime.now().minute)
    await msg.answer(
        f"Привет! 😊\nТеперь в {datetime.now().hour}.{min} бот будет отправлять тебе Цитату великих людей!",reply_markup=keyboard)


@dp.message_handler(Text('Изм. время увед.'))
async def change_time(msg: types.Message):

    kb = [
        [
            types.KeyboardButton(text='7.00'),
            types.KeyboardButton(text='8.00'),
            types.KeyboardButton(text='9.00'),
            types.KeyboardButton(text='10.00'),
        ],
        [
            types.KeyboardButton(text='11.00'),
            types.KeyboardButton(text='12.00'),
            types.KeyboardButton(text='13.00'),
            types.KeyboardButton(text='14.00'),
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Выбор времени',
        one_time_keyboard=True,
    )
    await msg.answer('Выберите время, удобное вам',reply_markup=keyboard)

async def send_random_message():
    message = random.choice(quotes)
    await bot.send_message(chat_id='1900247997',text=message)

async def start_scheduler_for_seven():
    schedule.every().day.at("07:00").do(lambda: asyncio.create_task(send_random_message()))
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

@dp.message_handler(Text('7.00'))
async def time_seven(msg: types.Message):
    await msg.answer("Сообщения будут отправляться каждый день в 19:00.")
    # запускаем задачу по расписанию
    asyncio.create_task(start_scheduler_for_seven())







@dp.message_handler(Text('Получить цитату сейчас'))
async def give_quo(msg: types.Message):

    kb = [[
        types.KeyboardButton(text='Назад в меню'),
        types.KeyboardButton(text='Получить цитату сейчас')
    ]]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Получение цитаты',
        one_time_keyboard=True,

    )
    with open('Quotes.txt') as f:
        quo = []
        for i in range(78):
            quo.append(f.readline())
        rand_quo = quo[random.randint(30,78)]
    await msg.answer(rand_quo, reply_markup=keyboard)



@dp.message_handler(Text('Назад в меню'))
async def main_menu(msg: types.Message):

    kb = [[
        types.KeyboardButton(text='Изм. время увед.'),
        types.KeyboardButton(text='Получить цитату сейчас')
    ]]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Главное меню',
        one_time_keyboard=True,
    )

    await msg.answer('Вы вернулись в главное меню', reply_markup=keyboard)

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Этот бот используется для каждодневной рассылки мотивации")



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(start_scheduler_for_seven())
    executor.start_polling(dp,skip_updates=True)