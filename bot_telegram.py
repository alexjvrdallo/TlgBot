
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import Message
import os

API_TOKEN = os.getenv("API_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Lista de administradores
admin_usernames = ["admin1", "admin2"]  # Reemplaza con los usernames reales sin @

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply(f"👋 Bienvenido/a, {message.from_user.full_name}!")

@dp.message_handler(commands=["ayuda"])
async def help_command(message: types.Message):
    await bot.send_message(GROUP_ID, "/ayudaatlgbot")
    await message.reply("✅ Solicitud de ayuda enviada.")

@dp.message_handler()
async def detect_admin_mention(message: Message):
    if message.entities:
        for entity in message.entities:
            if entity.type == "mention":
                mention = message.text[entity.offset:entity.offset + entity.length]
                if mention[1:] in admin_usernames:
                    texto = "📋 Lista de administradores:"
                    await bot.send_message(GROUP_ID, f"{texto}
➡️ {mention} ha sido mencionado por @{message.from_user.username}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
