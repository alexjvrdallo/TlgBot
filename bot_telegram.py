
import logging
import re
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BotBlocked, ChatNotFound
import asyncio
import os

API_TOKEN = "8046270772:AAHB7LBn9etmJK2c14fcrSQxZLgyqmY71AU"
GROUP_ID = -1002783169217

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Lista de palabras prohibidas
palabras_prohibidas = ["maldito", "mardito", "estúpido", "idiota", "pendejo", "imbécil"]

# Lista de administradores (esto se actualizará automáticamente al iniciar)
administradores = []

async def actualizar_administradores():
    global administradores
    try:
        miembros_admin = await bot.get_chat_administrators(GROUP_ID)
        administradores = [admin.user.id for admin in miembros_admin if not admin.user.is_bot]
    except Exception as e:
        logging.error(f"Error obteniendo administradores: {e}")

# Comando /start
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("¡Hola! Estoy activo para ayudarte. Usa /ayuda para contactar con los administradores.")

# Comando /ayuda
@dp.message_handler(commands=["ayuda"])
async def ayuda_command(message: types.Message):
    texto = f"🚨 Solicitud de ayuda enviada.
Usuario: @{message.from_user.username or message.from_user.full_name}
ID: {message.from_user.id}"
    for admin_id in administradores:
        try:
            await bot.send_message(admin_id, texto)
        except (BotBlocked, ChatNotFound):
            continue
    await message.reply("Tu solicitud ha sido enviada a los administradores.")

# Monitoreo de menciones y palabras prohibidas
@dp.message_handler()
async def monitorear_mensajes(message: types.Message):
    if any(palabra in message.text.lower() for palabra in palabras_prohibidas):
        texto = f"⚠️ Alerta de lenguaje inadecuado:
Usuario: @{message.from_user.username or message.from_user.full_name}
Mensaje: {message.text}"
        for admin_id in administradores:
            try:
                await bot.send_message(admin_id, texto)
            except (BotBlocked, ChatNotFound):
                continue

    # Notificación si se menciona un administrador
    if message.entities:
        for entity in message.entities:
            if entity.type == "mention":
                username_mencionado = message.text[entity.offset:entity.offset + entity.length]
                for admin_id in administradores:
                    try:
                        await bot.send_message(admin_id, f"📣 Mencionaron a un admin: {username_mencionado}
Mensaje: {message.text}")
                    except (BotBlocked, ChatNotFound):
                        continue

async def on_startup(dp):
    await actualizar_administradores()
    logging.info("Bot iniciado y administradores cargados.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
