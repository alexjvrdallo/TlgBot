import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# /start handler
@dp.message_handler(commands=["start"])
async def send_welcome(message: Message):
    await message.reply(f"👋 Bienvenido/a, {message.from_user.full_name}!")

# /ayuda handler
@dp.message_handler(commands=["ayuda"])
async def ayuda_handler(message: Message):
    texto = "🚨 Solicitud de ayuda enviada."
    await bot.send_message(chat_id=GROUP_ID, text=f"🚨 El usuario @{message.from_user.username} ha solicitado ayuda.")
    await message.reply(texto)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)