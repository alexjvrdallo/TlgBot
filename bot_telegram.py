import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from aiogram.dispatcher.filters import CommandStart, Command

from aiogram.utils.exceptions import ChatNotFound

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
ADMIN_IDS = [int(admin_id) for admin_id in os.getenv("ADMIN_IDS", "").split(",")]
WELCOME_MESSAGE = "¡Hola! Usa /reglas para ver las reglas."

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(CommandStart())
async def start(message: Message):
    await message.reply(WELCOME_MESSAGE)

@dp.message_handler(commands=["reglas"])
async def reglas(message: Message):
    await message.reply("""📌 Reglas del grupo:
1. Prohibido dar precios en público.
2. Respeto ante todo: no se toleran insultos, lenguaje ofensivo ni discriminación.
3. Nada de spam, promociones o enlaces sin autorización.
4. Evita mensajes repetitivos, cadenas o contenido no relacionado.
5. Las decisiones de los administradores son finales. Si tienes dudas, puedes contactarlos.""")

@dp.message_handler(commands=["staff"])
async def staff(message: Message):
    await message.reply("👨‍💼 Lista de administradores:

🔹 Alexander – @AlexanderEjemplo
🔹 Tribal – @TribalEjemplo")

@dp.message_handler(commands=["ayuda"])
async def ayuda(message: Message):
    username = message.from_user.username or message.from_user.full_name
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, f"🚨 El usuario @{username} ha solicitado ayuda en el grupo.")
        except ChatNotFound:
            logging.warning(f"No se pudo enviar mensaje privado al admin {admin_id}")
    await message.reply("🚨 Solicitud de ayuda enviada.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
