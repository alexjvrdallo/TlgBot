import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("No se encontró el TOKEN en las variables de entorno.")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_cmd(message: Message):
    await message.answer("¡Hola! Bienvenido al bot. Usa /reglas para ver las reglas.")

@dp.message_handler(commands=["reglas"])
async def reglas_cmd(message: Message):
    await message.answer("📌 Reglas del grupo:\n1. Respeto mutuo\n2. No spam\n3. Seguir las normas de Telegram.")

@dp.message_handler()
async def filter_messages(message: Message):
    palabras_prohibidas = ["spam", "estafa", "scam"]
    if any(palabra in message.text.lower() for palabra in palabras_prohibidas):
        await message.delete()
        await message.answer("⚠️ Tu mensaje fue eliminado por contener palabras prohibidas.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)