import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatPermissions
from aiogram.utils import executor
from collections import defaultdict
import re
from datetime import datetime, timedelta

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("No se encontró el TOKEN en las variables de entorno.")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
user_warnings = defaultdict(int)

SPAM_PATTERNS = [
    r"http[s]?://",
    r"t\.me/",
    r"spam",
    r"gratis",
    r"dinero",
    r"oferta",
    r"promoción",
    r"vendo",
    r"compro"
]

def es_spam(texto):
    for patron in SPAM_PATTERNS:
        if re.search(patron, texto, re.IGNORECASE):
            return True
    return False

async def notificar_admins(chat_id, offender):
    admins = await bot.get_chat_administrators(chat_id)
    mensaje = f"⚠️ El usuario {offender.full_name} (@{offender.username}) recibió 2 advertencias por spam."
    for admin in admins:
        if not admin.user.is_bot:
            try:
                await bot.send_message(admin.user.id, mensaje)
            except:
                pass

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("👋 ¡Hola! Soy el bot del grupo. Usa /reglas para conocer las normas.")

@dp.message_handler(commands=["reglas"])
async def reglas(message: types.Message):
    await message.answer(
        "📌 *REGLAS DEL GRUPO* 📌\n\n"
        "1️⃣ No decir malas palabras\n"
        "2️⃣ No Spam (de ningún tipo)\n"
        "3️⃣ No hablar de precios en ningún grupo.\n",
        parse_mode="Markdown"
    )

@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def welcome(message: types.Message):
    for user in message.new_chat_members:
        await message.reply(
            f"👋 Bienvenido/a {user.full_name} al grupo.

📌 *REGLAS DEL GRUPO* 📌
"
            "1️⃣ No decir malas palabras
"
            "2️⃣ No Spam (de ningún tipo)
"
            "3️⃣ No hablar de precios en ningún grupo.",
            parse_mode="Markdown"
        )

@dp.message_handler()
async def handle_messages(message: types.Message):
    if message.text and es_spam(message.text):
        user_id = message.from_user.id
        user_warnings[user_id] += 1
        count = user_warnings[user_id]

        await message.reply(f"🚫 Detectado posible spam. Advertencia {count}/3.")

        if count == 2 and message.chat.type != "private":
            await notificar_admins(message.chat.id, message.from_user)

        if count >= 3:
            if message.chat.type != "private":
                try:
                    until = datetime.utcnow() + timedelta(minutes=5)
                    await bot.restrict_chat_member(
                        message.chat.id,
                        user_id,
                        ChatPermissions(can_send_messages=False),
                        until_date=until
                    )
                    await message.reply("🤐 Has sido silenciado por 5 minutos debido a spam reiterado.")
                except:
                    pass
            user_warnings[user_id] = 0

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)