import asyncio
import aiogram
import os
from aiogram import Bot, Dispatcher, types, enums
from aiogram.types import Message, Video, Audio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from project.backend.message_handler import MessageHandler

token = '5577625193:AAGBtQsZAaBKJk9nUSUUJGfwuMZDfk89Gv8'
bot = Bot(token)
dp = Dispatcher()
user_db = dict()


@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    user = message.from_user.full_name
    user_id = await MessageHandler.new_user()
    user_db[message.chat.id] = user_id
    await message.answer(f'привет я бот')


@dp.message()
async def message_handler(message: Message) -> None:
    await bot_handler(message)


async def bot_handler(message: Message) -> None:
    b = []
    b.append([InlineKeyboardButton(text="Оценить", callback_data=f"estimate")])
    b.append([InlineKeyboardButton(text="Начать новую тему", callback_data=f"new_chat")])
    markup = InlineKeyboardMarkup(inline_keyboard=b)
    user = message.from_user.full_name
    user_id = user_db[message.chat.id]
    text = await MessageHandler.new_message(user_id, message.text)
    await bot.send_message(chat_id=message.chat.id,
                           text=str(text).replace(',', '\n'),
                           reply_markup=markup)


@dp.callback_query(lambda c: c.data == "estimate")
async def estimate_handler(callback_query: types.CallbackQuery):
    b = []
    b.append([InlineKeyboardButton(text="Поставьте оценку", callback_data=f"grade 0")])
    b1 = InlineKeyboardButton(text="1", callback_data=f"grade 1")
    b2 = InlineKeyboardButton(text="2", callback_data=f"grade 2")
    b3 = InlineKeyboardButton(text="3", callback_data=f"grade 3")
    b4 = InlineKeyboardButton(text="4", callback_data=f"grade 4")
    b5 = InlineKeyboardButton(text="5", callback_data=f"grade 5")
    b.append([b1, b2, b3])
    b.append([b4, b5])
    markup = InlineKeyboardMarkup(inline_keyboard=b)
    await bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=markup)


@dp.callback_query(lambda c: c.data == "new_chat")
async def new_chat_handler(callback_query: types.CallbackQuery):
    user_id = user_db[callback_query.message.chat.id]
    mes = await MessageHandler.new_chat(user_id)
    await bot.send_message(chat_id=callback_query.message.chat.id,
                           text=str(mes))


@dp.callback_query(lambda c: int(list(c.data.split())[1]) > 0)
async def grade_handler(callback_query: types.CallbackQuery):
    b = []
    b.append([InlineKeyboardButton(text="Спасибо", callback_data=f"grade 0")])
    markup = InlineKeyboardMarkup(inline_keyboard=b)
    await bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=markup)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
