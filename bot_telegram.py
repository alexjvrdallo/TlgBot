import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start", "hola"])
async def start_command(message: Message):
    texto = f"👋 Bienvenido/a, {message.from_user.full_name}!"
    await message.reply(texto)

@dp.message_handler(commands=["ayuda"])
async def ayuda_command(message: Message):
    texto = f"🚨 Solicitud de ayuda enviada."
    await message.reply(texto)
    await bot.send_message(GROUP_ID, f"📢 El usuario {message.from_user.full_name} ha solicitado ayuda.")

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)