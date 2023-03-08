import telebot
from telebot import types

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import random


token = "5373817318:AAF4tHynVvmWuQUBBcb10r7JPlAVBsU2u9I"

#bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
bot = Bot(token=token)
dp = Dispatcher(bot)

async def start_bot(_):
     print("Bot is alive!")
# bot.send_message(1059208615, "123")
# print(2)
# 1059208615
@dp.message_handler(commands=["start", "help"])
async def start(message: types.Message):
    try:
        #await bot.send_message(message.from_user.id, "Добро пожаловать")
        print(message)
        print(message.from_user.id)
        await bot.send_message(message.from_user.id, "Хай, Кекся!")
        await message.delete()
    except Exception as ex:
        print(ex)
        await message.reply("Что-то не так...возможно стоит добавить бота!")

@dp.message_handler()
async def input_text(message: types.Message):
    #await message.reply("123") # пересылает входящее сообщение и отвечает
    #await message.answer("123") # отвечает
    await bot.send_message(message.from_user.id, "123") # сообщение в личку пользователя


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=start_bot)

# text = 123
# BOT_TOKEN = "5373817318:AAF4tHynVvmWuQUBBcb10r7JPlAVBsU2u9I"
# admin_id = 1059208615
# API_link = "https://api.telegram.org/bot" + BOT_TOKEN
# requests.get(API_link + f"/sendMessage?chat_id={admin_id}&text={text}")

print("Work is out")