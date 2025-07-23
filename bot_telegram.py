import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatPermissions
from aiogram.utils import executor
from aiogram.dispatcher.filters import CommandStart, Command
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import os

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("API_TOKEN no está definido.")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

spam_tracker = {}

ADMIN_IDS = []

class SpamMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        if message.chat.type not in ["group", "supergroup", "private"]:
            return

        user_id = message.from_user.id
        chat_id = message.chat.id
        text = message.text or ""

        if chat_id not in spam_tracker:
            spam_tracker[chat_id] = {}

        if user_id not in spam_tracker[chat_id]:
            spam_tracker[chat_id][user_id] = {"count": 0}

        if "http://" in text or "https://" in text or "@gmail" in text or ".com" in text:
            spam_tracker[chat_id][user_id]["count"] += 1
            count = spam_tracker[chat_id][user_id]["count"]

            if count == 1:
                await message.reply("🚫 Advertencia 1: no se permite spam.")
            elif count == 2:
                await message.reply("🚫 Advertencia 2: no insistas o serás silenciado.")
                for admin_id in ADMIN_IDS:
                    try:
                        await bot.send_message(admin_id, f"🚨 Usuario {message.from_user.full_name} (ID: {user_id}) hizo spam por segunda vez en {chat_id}.")
                    except:
                        pass
            elif count >= 3:
                await message.reply("❌ Has sido silenciado por spam (5 min).")
                try:
                    await bot.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False), until_date=message.date + 300)
                except Exception as e:
                    await message.reply("Error al silenciar usuario.")
            raise CancelHandler()

@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.answer("¡Hola! Bienvenido al bot. Usa /reglas para ver las reglas.")

@dp.message_handler(Command("reglas"))
async def reglas(message: types.Message):
    reglas_texto = "📌 Reglas del grupo:
1. Respeto mutuo
2. No spam
3. Seguir las normas de Telegram."
    await message.answer(reglas_texto)

@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def bienvenida(message: types.Message):
    for user in message.new_chat_members:
        await message.reply(f"👋 Bienvenido/a {user.full_name} al grupo.")

async def on_startup(dp):
    dp.middleware.setup(SpamMiddleware())

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, on_startup=on_startup)