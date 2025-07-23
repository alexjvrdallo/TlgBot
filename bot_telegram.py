import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ChatMemberUpdated
import os

API_TOKEN = os.getenv("API_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# IDs de administradores (reemplaza con los reales)
ADMIN_IDS = [123456789, 987654321]

# Diccionario para advertencias
warnings = {}

# Palabras prohibidas
bad_words = ["grosería1", "grosería2", "spam", "maldición"]

# Mensajes
reglas_texto = """📌 Reglas del grupo:
1. Prohibido dar precios en público.
2. Respeto ante todo: no se toleran insultos, lenguaje ofensivo ni discriminación.
3. Nada de spam, promociones o enlaces sin autorización.
4. Evita mensajes repetitivos, cadenas o contenido no relacionado.
5. Las decisiones de los administradores son finales. Si tienes dudas, puedes contactarlos.
"""

bienvenida_texto = """Hola y gracias por unirte a nuestra comunidad. Estamos muy contentos de tenerte aquí.
Antes de comenzar, por favor tómate un momento para leer nuestras reglas para mantener un ambiente respetuoso y productivo para todos.

Usa /reglas para ver las reglas del grupo.
Usa /staff para saber quiénes son los administradores.
Si necesitas ayuda, puedes usar /ayuda y se notificará a los administradores.
"""

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("¡Hola! Usa /reglas para ver las reglas.")

@dp.message_handler(commands=["reglas"])
async def cmd_reglas(message: types.Message):
    await message.answer(reglas_texto)

@dp.message_handler(commands=["ayuda"])
async def cmd_ayuda(message: types.Message):
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, f"🔔 El usuario @{message.from_user.username} ha solicitado ayuda en el grupo {message.chat.title}.")
        except:
            pass
    await message.reply("Se ha notificado a los administradores. ¡Pronto te ayudarán!")

@dp.message_handler(commands=["staff"])
async def cmd_staff(message: types.Message):
    staff = "\n".join([f"- {admin_id}" for admin_id in ADMIN_IDS])
    await message.reply(f"👮 Lista de administradores:\n{staff}")

@dp.chat_member_handler()
async def welcome_new_member(update: ChatMemberUpdated):
    if update.new_chat_member.status == "member":
        await bot.send_message(update.chat.id, bienvenida_texto)

@dp.message_handler()
async def check_message(message: types.Message):
    if any(word in message.text.lower() for word in bad_words):
        user_id = message.from_user.id
        warnings[user_id] = warnings.get(user_id, 0) + 1
        if warnings[user_id] == 2:
            for admin_id in ADMIN_IDS:
                await bot.send_message(admin_id, f"⚠️ @{message.from_user.username} ha sido advertido por segunda vez.")
        if warnings[user_id] >= 3:
            await message.chat.restrict(user_id, types.ChatPermissions(can_send_messages=False), until_date=300)
            await message.reply("Has sido silenciado por 5 minutos por violar las reglas.")
        else:
            await message.reply(f"Advertencia {warnings[user_id]}/3: tu mensaje contiene contenido no permitido.")
    elif any(str(admin_id) in message.text for admin_id in ADMIN_IDS):
        for admin_id in ADMIN_IDS:
            if str(admin_id) in message.text:
                await bot.send_message(admin_id, f"Fuiste mencionado por @{message.from_user.username} en el grupo {message.chat.title}.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)