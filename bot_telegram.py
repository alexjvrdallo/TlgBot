import logging
import re
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ChatPermissions
from aiogram.utils.exceptions import BadRequest

API_TOKEN = "AQUI_VA_TU_TOKEN"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Lista de malas palabras (puedes ampliar esta lista)
bad_words = [r"maldito", r"mardito", r"idiota", r"estúpido", r"imbécil"]

# Seguimiento de advertencias por usuario
warnings = {}

# Obtener lista de administradores
async def get_admins_names(message: types.Message):
    chat_admins = await message.chat.get_administrators()
    text = "* Lista de administradores:\n"
    for admin in chat_admins:
        if admin.user.username:
            text += f"- [{admin.user.full_name}](tg://user?id={admin.user.id})\n"
        else:
            text += f"- {admin.user.full_name}\n"
    await message.reply(text, parse_mode="Markdown")

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    welcome_text = (
        "Hola y gracias por unirte a nuestra comunidad. Estamos muy contentos de tenerte aquí.\n\n"
        "Antes de comenzar, por favor tómate un momento para leer nuestras reglas para mantener un ambiente respetuoso y productivo para todos:\n\n"
        "*Reglas del grupo:*\n"
        "- Prohibido dar precios en Público.\n"
        "- Respeto ante todo: no se toleran insultos, lenguaje ofensivo ni discriminación.\n"
        "- Nada de spam, promociones o enlaces sin autorización.\n"
        "- Evita mensajes repetitivos, cadenas o contenido no relacionado.\n"
        "- Las decisiones de los administradores son finales. Si tienes dudas, puedes contactarlos.\n\n"
        "Si necesitas ayuda, puedes escribir /ayuda y se notificará a los administradores.\n"
        "Para ver a los administradores disponibles, puedes usar /staff"
    )
    await message.answer(welcome_text, parse_mode="Markdown")

@dp.message_handler(commands=["staff"])
async def list_admins(message: types.Message):
    await get_admins_names(message)

@dp.message_handler(commands=["ayuda"])
async def ayuda_handler(message: types.Message):
    chat_admins = await message.chat.get_administrators()
    for admin in chat_admins:
        if not admin.user.is_bot:
            try:
                await bot.send_message(admin.user.id, f"🚨 El usuario [{message.from_user.full_name}](tg://user?id={message.from_user.id}) solicitó ayuda en el grupo: {message.chat.title}"),
            except:
                pass
    await message.reply("📨 Se ha notificado a los administradores. Pronto te ayudarán.")

@dp.message_handler()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text.lower()

    # Menciones a admins
    if message.entities:
        for entity in message.entities:
            if entity.type == "mention":
                admins = await message.chat.get_administrators()
                for admin in admins:
                    if admin.user.username and f"@{admin.user.username.lower()}" in text:
                        try:
                            await bot.send_message(admin.user.id, f"👤 Fuiste mencionado por {message.from_user.full_name} en {message.chat.title}")
                        except:
                            pass

    # Filtro de groserías
    for pattern in bad_words:
        if re.search(pattern, text):
            warnings[user_id] = warnings.get(user_id, 0) + 1
            if warnings[user_id] == 2:
                chat_admins = await message.chat.get_administrators()
                for admin in chat_admins:
                    if not admin.user.is_bot:
                        try:
                            await bot.send_message(admin.user.id, f"⚠️ El usuario [{message.from_user.full_name}](tg://user?id={user_id}) fue advertido por lenguaje inapropiado en {message.chat.title}. (2da advertencia)")
                        except:
                            pass
            elif warnings[user_id] >= 3:
                try:
                    await bot.restrict_chat_member(message.chat.id, user_id, ChatPermissions(can_send_messages=False), until_date=message.date.timestamp() + 300)
                    await message.reply(f"⛔ Has sido silenciado por 5 minutos por incumplir las reglas.")
                except BadRequest:
                    pass
            else:
                await message.reply(f"⚠️ Advertencia {warnings[user_id]}/3: lenguaje inapropiado no está permitido.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)