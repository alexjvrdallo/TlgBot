import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatPermissions
from aiogram.utils import executor
from collections import defaultdict
import re

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("No se encontró el TOKEN en las variables de entorno.")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Diccionario para llevar el conteo de advertencias por usuario
user_warnings = defaultdict(int)

# Palabras clave o patrones que se consideran spam
SPAM_PATTERNS = [
    r"http[s]?://",  # enlaces
    r"t\.me/",
    r"spam",
    r"gratis",
    r"dinero",
    r"oferta",
    r"promoción",
    r"vendo",
    r"compro"
]

async def notificar_admins(chat_id, offender):
    admins = await bot.get_chat_administrators(chat_id)
    mensaje = f"⚠️ El usuario {offender.full_name} (@{offender.username}) recibió 2 advertencias por spam."
    for admin in admins:
        if not admin.user.is_bot:
            try:
                await bot.send_message(admin.user.id, mensaje)
            except:
                pass

def es_spam(texto):
    for patron in SPAM_PATTERNS:
        if re.search(patron, texto, re.IGNORECASE):
            return True
    return False

@dp.message_handler()
async def handle_all_messages(message: types.Message):
    if message.chat.type in ["group", "supergroup", "private"]:
        if message.text and es_spam(message.text):
            user_id = message.from_user.id
            user_warnings[user_id] += 1

            advertencias = user_warnings[user_id]
            await message.reply(f"🚫 Detectado posible spam. Advertencia {advertencias}/3.")

            if advertencias == 2 and message.chat.type != "private":
                await notificar_admins(message.chat.id, message.from_user)

            if advertencias >= 3:
                if message.chat.type != "private":
                    try:
                        await bot.restrict_chat_member(
                            message.chat.id,
                            user_id,
                            ChatPermissions(can_send_messages=False),
                            until_date=types.datetime.datetime.now() + types.timedelta(minutes=5)
                        )
                        await message.reply("🤐 Has sido silenciado por 5 minutos debido a spam reiterado.")
                    except:
                        pass
                user_warnings[user_id] = 0  # Resetear advertencias después de silenciar

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)