
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatPermissions
from aiogram.utils import executor
from aiogram.dispatcher.filters import CommandStart
import asyncio
import os

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_warnings = {}

WELCOME_MESSAGE = "👋 Bienvenido/a {name} al grupo."
RULES_TEXT = "📌 Reglas del grupo:\n1. Respeto mutuo.\n2. No spam.\n3. Seguir las normas de Telegram."
ADMINS = []

SPAM_KEYWORDS = ["http", "www", ".com", "t.me/", "joinchat", "@", "#"]

@dp.message_handler(CommandStart(), chat_type=types.ChatType.PRIVATE)
async def start_private(message: types.Message):
    await message.reply("¡Hola! Bienvenido al bot. Usa /reglas para ver las reglas.")

@dp.message_handler(commands=["reglas"], chat_type=types.ChatType.PRIVATE)
@dp.message_handler(commands=["reglas"], chat_type=types.ChatType.GROUP)
async def reglas_command(message: types.Message):
    await message.reply(RULES_TEXT)

@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def welcome_user(message: types.Message):
    for user in message.new_chat_members:
        await message.reply(WELCOME_MESSAGE.format(name=user.full_name))

@dp.message_handler()
async def check_spam(message: types.Message):
    if message.chat.type not in ["group", "supergroup", "private"]:
        return

    user_id = message.from_user.id
    text = message.text.lower()
    is_spam = any(word in text for word in SPAM_KEYWORDS)

    if is_spam:
        user_warnings[user_id] = user_warnings.get(user_id, 0) + 1
        warnings = user_warnings[user_id]

        if warnings == 1:
            await message.reply("⚠️ Advertencia 1: No envíes spam.")
        elif warnings == 2:
            await message.reply("⚠️ Advertencia 2: Último aviso. Serás notificado a los administradores.")
            try:
                chat_admins = await bot.get_chat_administrators(message.chat.id)
                for admin in chat_admins:
                    if admin.user.is_bot:
                        continue
                    await bot.send_message(admin.user.id, f"🔔 Usuario {message.from_user.full_name} está enviando spam.")
            except:
                pass
        elif warnings >= 3:
            await message.reply("⛔ Has sido silenciado por enviar spam reiteradamente (5 minutos).")
            until_date = message.date + asyncio.timedelta(minutes=5)
            try:
                await bot.restrict_chat_member(
                    message.chat.id,
                    message.from_user.id,
                    ChatPermissions(can_send_messages=False),
                    until_date=until_date
                )
            except:
                await message.reply("⚠️ No tengo permisos suficientes para silenciar.")
