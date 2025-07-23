import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatPermissions
from aiogram.utils import executor
import os
import re
import asyncio
from datetime import timedelta

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("Falta el token en la variable API_TOKEN.")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

warnings = {}
ADMIN_IDS = []

groserias = ["mierda", "puta", "gilipollas", "maldito", "pendejo", "imbécil", "cabron", "estúpido"]
spam_keywords = ["http", "www", "t.me/", "@", ".com"]

def es_spam_o_groseria(texto):
    texto = texto.lower()
    for palabra in spam_keywords + groserias:
        if palabra in texto:
            return True
    return False

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("¡Hola! Usa /reglas para conocer las normas del grupo.")

@dp.message_handler(commands=["reglas"])
async def reglas(message: types.Message):
    texto = (
        """📌 Reglas del grupo:
"
        "1. Prohibido dar precios en público.
"
        "2. Respeto ante todo: no se toleran insultos, lenguaje ofensivo ni discriminación.
"
        "3. Nada de spam, promociones o enlaces sin autorización.
"
        "4. Evita mensajes repetitivos, cadenas o contenido no relacionado.
"
        "5. Las decisiones de los administradores son finales. Si tienes dudas, puedes contactarlos."
    )
    await message.answer(texto)

@dp.message_handler(commands=["staff"])
async def staff(message: types.Message):
    admins = await bot.get_chat_administrators(message.chat.id)
    nombres = [f"• {a.user.full_name}" for a in admins if not a.user.is_bot]
    await message.answer("👥 Administradores del grupo:
" + "
".join(nombres))

@dp.message_handler(commands=["ayuda"])
async def ayuda(message: types.Message):
    admins = await bot.get_chat_administrators(message.chat.id)
    noti = f"📣 El usuario @{message.from_user.username or message.from_user.full_name} (ID: {message.from_user.id}) solicitó ayuda en el grupo {message.chat.title}."
    for admin in admins:
        if not admin.user.is_bot:
            try:
                await bot.send_message(admin.user.id, noti)
            except:
                pass
    await message.reply("✅ Se ha notificado a los administradores. Pronto te ayudarán.")

@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def bienvenida(message: types.Message):
    for user in message.new_chat_members:
        bienvenida = (
            f"👋 Hola {user.full_name}, gracias por unirte a nuestra comunidad.

"
            "Estamos muy contentos de tenerte aquí. Antes de comenzar, por favor tómate un momento para leer nuestras reglas para mantener un ambiente respetuoso y productivo para todos:

"
            "Usa /reglas para conocerlas, /staff para ver a los administradores y /ayuda si necesitas asistencia."
        )
        await message.answer(bienvenida)

@dp.message_handler()
async def controlar_mensajes(message: types.Message):
    if message.chat.type not in ["group", "supergroup"]:
        return

    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text or ""

    if es_spam_o_groseria(text):
        key = (chat_id, user_id)
        warnings[key] = warnings.get(key, 0) + 1
        count = warnings[key]

        if count == 1:
            await message.reply("⚠️ Advertencia 1: Por favor, evita usar lenguaje inapropiado o hacer spam.")
        elif count == 2:
            await message.reply("⚠️ Advertencia 2: Última advertencia. Los administradores han sido notificados.")
            admins = await bot.get_chat_administrators(chat_id)
            for admin in admins:
                if not admin.user.is_bot:
                    try:
                        await bot.send_message(admin.user.id, f"🚨 El usuario @{message.from_user.username or message.from_user.full_name} volvió a infringir las reglas en {message.chat.title}.")
                    except:
                        pass
        elif count >= 3:
            await message.reply("⛔ Has sido silenciado por 5 minutos debido a múltiples infracciones.")
            until_date = message.date + timedelta(minutes=5)
            try:
                await bot.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False), until_date=until_date)
            except:
                pass
            warnings[key] = 0

    # Mención a admin
    if "@" in text:
        admins = await bot.get_chat_administrators(chat_id)
        for admin in admins:
            if admin.user.username and f"@{admin.user.username.lower()}" in text.lower():
                try:
                    await bot.send_message(admin.user.id, f"👀 Te han mencionado en el grupo {message.chat.title} por parte de @{message.from_user.username or message.from_user.full_name}.")
                except:
                    pass

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
