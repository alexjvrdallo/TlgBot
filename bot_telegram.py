import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatPermissions
from aiogram.utils import executor
import asyncio
import re
import os

API_TOKEN = os.getenv("API_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Diccionario para rastrear advertencias por usuario
warnings = {}

# Reglas del grupo
reglas_texto = """📌 Reglas del grupo:
1. Respeto mutuo
2. No spam
3. Seguir las normas de Telegram."""

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.answer("¡Hola! Bienvenido al bot. Usa /reglas para ver las reglas.")

@dp.message_handler(commands=["reglas"])
async def send_rules(message: types.Message):
    await message.answer(reglas_texto)

@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def welcome_new_member(message: types.Message):
    for user in message.new_chat_members:
        await message.reply(f"👋 Bienvenido/a {user.full_name} al grupo.")

# Detectar spam
spam_keywords = ['http', 'www', 't.me/', '@', '.com']
spam_pattern = re.compile(r"|".join(map(re.escape, spam_keywords)), re.IGNORECASE)

async def check_spam(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text or ""

    if spam_pattern.search(text):
        count = warnings.get((chat_id, user_id), 0) + 1
        warnings[(chat_id, user_id)] = count

        if count == 1:
            await message.reply("⚠️ Advertencia 1: No se permite hacer spam.")
        elif count == 2:
            await message.reply("⚠️ Advertencia 2: Último aviso. El usuario ha sido notificado a los administradores.")
            admins = await bot.get_chat_administrators(chat_id)
            admin_mentions = ", ".join([f"@{admin.user.username}" for admin in admins if admin.user.username])
            if admin_mentions:
                await message.answer(f"🚨 Atención administradores: {message.from_user.full_name} está enviando spam. {admin_mentions}")
        elif count >= 3:
            await message.reply("⛔ Has sido silenciado por 5 minutos debido a spam.")
            until_date = message.date + asyncio.timedelta(minutes=5)
            await bot.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False), until_date=until_date)
            warnings[(chat_id, user_id)] = 0

@dp.message_handler(lambda message: message.chat.type in ["group", "supergroup", "private"])
async def handle_messages(message: types.Message):
    await check_spam(message)

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
