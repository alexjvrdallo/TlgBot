import os
import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))
ADMINS = os.getenv("ADMINS").split(",")  # Lista de usernames sin @

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    await message.reply("¡Hola! Usa /reglas para ver las reglas.")

@dp.message_handler(commands=['reglas'])
async def reglas_command(message: Message):
    reglas = (
        "📌 Reglas del grupo:
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
    await message.reply(reglas)

@dp.message_handler(commands=['staff'])
async def staff_command(message: Message):
    staff_list = "\n".join([f"👤 @{admin.strip()}" for admin in ADMINS])
    await message.reply(f"👥 Administradores:
{staff_list}")

@dp.message_handler(commands=['ayuda'])
async def ayuda_command(message: Message):
    username = message.from_user.username or message.from_user.full_name
    for admin in ADMINS:
        try:
            await bot.send_message(f"@{admin}", f"🚨 El usuario @{username} ha solicitado ayuda en el grupo.")
        except Exception as e:
            logging.error(f"Error al enviar mensaje a @{admin}: {e}")
    await message.reply("🚨 Solicitud de ayuda enviada. Un administrador se comunicará contigo pronto.")

@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def welcome_new_member(message: Message):
    for new_member in message.new_chat_members:
        await message.reply(f"¡Hola {new_member.full_name}, bienvenido/a! Por favor, revisa las /reglas y recuerda que puedes usar /ayuda si necesitas asistencia.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)