import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
import os

API_TOKEN = os.getenv("API_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

ADMIN_IDS = [123456789, 987654321]  # Reemplazar con los IDs reales de administradores

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    texto = f"👋 Bienvenido/a, {message.from_user.full_name}!"
    await bot.send_message(GROUP_ID, texto)

@dp.message_handler(commands=['ayuda'])
async def cmd_ayuda(message: Message):
    texto = "📩 Solicitud de ayuda enviada."
    await message.reply(texto)
    await bot.send_message(GROUP_ID, f"{texto}")

@dp.message_handler(lambda message: any(user.id in ADMIN_IDS for user in message.entities if isinstance(user, types.MessageEntity) and user.type == 'mention'))
async def notify_admins(message: types.Message):
    texto = f"📣 Un miembro ha mencionado a un administrador.

Mensaje:
{message.text}"
    await bot.send_message(GROUP_ID, texto)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
