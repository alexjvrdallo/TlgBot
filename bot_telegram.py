import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatPermissions
from aiogram.utils import executor
from aiogram.dispatcher.filters import CommandStart, Command
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime, timedelta

API_TOKEN = os.getenv("API_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Diccionario para advertencias de spam
user_warnings = {}

# ID de administradores (puedes personalizar si gustas)
ADMINS = []

# Reglas
REGLAS = "📌 Reglas del grupo:\n1. Respeto mutuo\n2. No spam\n3. Seguir las normas de Telegram."

@dp.message_handler(CommandStart())
async def send_welcome(message: types.Message):
    await message.answer("¡Hola! Bienvenido al bot. Usa /reglas para ver las reglas.")

@dp.message_handler(commands=["reglas"])
async def reglas(message: types.Message):
    await message.answer(REGLAS)

@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def welcome_user(message: types.Message):
    for user in message.new_chat_members:
        await message.reply(f"👋 Bienvenido/a {user.full_name} al grupo.")

@dp.message_handler()
async def detect_spam(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Detectar enlaces como spam
    if "http://" in message.text or "https://" in message.text:
        warnings = user_warnings.get(user_id, 0) + 1
        user_warnings[user_id] = warnings

        if warnings == 1:
            await message.reply("⚠️ Primera advertencia por spam.")
        elif warnings == 2:
            await message.reply("⚠️ Segunda advertencia por spam. Se notificó a los administradores.")
            for admin in ADMINS:
                try:
                    await bot.send_message(admin, f"⚠️ Usuario {message.from_user.full_name} ha cometido 2 infracciones de spam en el grupo {chat_id}")
                except:
                    pass
        elif warnings >= 3:
            await message.reply("🚫 Has sido silenciado por 5 minutos por exceder el límite de advertencias.")
            until_date = datetime.now() + timedelta(minutes=5)
            await bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=ChatPermissions(can_send_messages=False),
                until_date=until_date
            )
            user_warnings[user_id] = 0  # Reiniciar advertencias
