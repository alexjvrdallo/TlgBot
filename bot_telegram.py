from aiogram import Bot, Dispatcher, types, executor
import logging
import re
import os
from aiogram.types import ChatPermissions

API_TOKEN = os.getenv("API_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

admins = {}

# Lista de palabras prohibidas
bad_words = ["grosería1", "grosería2", "grosería3"]
user_warnings = {}

# Reglas del grupo
reglas_texto = """📌 Reglas del grupo:

1. Prohibido dar precios en Público.
2. Respeto ante todo: no se toleran insultos, lenguaje ofensivo ni discriminación.
3. Nada de spam, promociones o enlaces sin autorización.
4. Evita mensajes repetitivos, cadenas o contenido no relacionado.
5. Las decisiones de los administradores son finales. Si tienes dudas, puedes contactarlos.
"""

bienvenida = """👋 Hola y gracias por unirte a nuestra comunidad. Estamos muy contentos de tenerte aquí.
Antes de comenzar, por favor tómate un momento para leer nuestras reglas para mantener un ambiente respetuoso y productivo para todos:

/reglas - para ver las reglas
/staff - para ver a los administradores del grupo
/ayuda - si necesitas ayuda y quieres notificar a un admin
"""

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer("Bot activo.")

@dp.message_handler(commands=["reglas"])
async def reglas(msg: types.Message):
    await msg.reply(reglas_texto)

@dp.message_handler(commands=["ayuda"])
async def ayuda(msg: types.Message):
    if msg.chat.type in ["group", "supergroup"]:
        for admin in admins.get(msg.chat.id, []):
            await bot.send_message(admin.user.id, f"🆘 {msg.from_user.full_name} (@{msg.from_user.username}) pidió ayuda en el grupo {msg.chat.title}.")
        await msg.reply("✅ Los administradores han sido notificados.")

@dp.message_handler(commands=["staff"])
async def staff(msg: types.Message):
    if msg.chat.type in ["group", "supergroup"]:
        chat_admins = await bot.get_chat_administrators(msg.chat.id)
        texto = "👮 Lista de administradores:\n"
        for admin in chat_admins:
            user = admin.user
            if user.username:
                texto += f"• [{user.full_name}](https://t.me/{user.username})\n"
            else:
                texto += f"• {user.full_name}\n"
        await msg.reply(texto, parse_mode="Markdown")

@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def bienvenida_nuevo(msg: types.Message):
    for user in msg.new_chat_members:
        await msg.reply(f"👋 Bienvenido/a {user.full_name} al grupo.\n\n{bienvenida}")
        admins[msg.chat.id] = await bot.get_chat_administrators(msg.chat.id)

@dp.message_handler()
async def filtro_general(msg: types.Message):
    if msg.chat.type not in ["group", "supergroup"]:
        return

    if any(palabra in msg.text.lower() for palabra in bad_words):
        usuario = msg.from_user.id
        advertencias = user_warnings.get(usuario, 0) + 1
        user_warnings[usuario] = advertencias

        if advertencias == 1:
            await msg.reply("⚠️ Primera advertencia: No uses lenguaje inapropiado.")
        elif advertencias == 2:
            await msg.reply("⚠️ Segunda advertencia. Se notificará a los administradores.")
            for admin in admins.get(msg.chat.id, []):
                await bot.send_message(admin.user.id, f"🚨 {msg.from_user.full_name} fue advertido por lenguaje inapropiado en {msg.chat.title}.")
        elif advertencias >= 3:
            await msg.reply("⛔ Has recibido 3 advertencias. Serás silenciado por 5 minutos.")
            await bot.restrict_chat_member(
                msg.chat.id,
                msg.from_user.id,
                ChatPermissions(can_send_messages=False),
                until_date=msg.date + 300
            )
        await msg.delete()

    if msg.entities:
        for entity in msg.entities:
            if entity.type == "mention":
                username_mencionado = msg.text[entity.offset:entity.offset + entity.length]
                for admin in admins.get(msg.chat.id, []):
                    if admin.user.username and f"@{admin.user.username}".lower() == username_mencionado.lower():
                        await bot.send_message(admin.user.id, f"🔔 Has sido mencionado en el grupo {msg.chat.title} por {msg.from_user.full_name}.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)