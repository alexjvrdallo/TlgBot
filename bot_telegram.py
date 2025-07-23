import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart
import os

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"👋 Bienvenido/a {message.from_user.full_name}!")

@dp.message()
async def reglas(message: Message):
    if "reglas" in message.text.lower():
        await message.answer(
            """📌 Reglas del grupo:

1. Sé respetuoso.
2. No spam.
3. Sigue las normas del administrador.
"""
        )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
