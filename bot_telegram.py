import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

ADMIN_IDS = [123456789]  # Reemplaza con los IDs reales de los administradores

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.reply("¡Hola! Usa /reglas para ver las reglas.")

@dp.message(Command("reglas"))
async def cmd_reglas(message: Message):
    reglas = (
        "📌 <b>Reglas del grupo:</b>
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

@dp.message(Command("staff"))
async def cmd_staff(message: Message):
    await message.reply("👨‍💼 <b>Administradores:</b>
• Alexander - @AlexanderUser
• Support - @SupportUser")

@dp.message(Command("ayuda"))
async def cmd_ayuda(message: Message):
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, f"🚨 El usuario @{message.from_user.username} ha solicitado ayuda.")
        except:
            pass
    await message.reply("🚨 Solicitud de ayuda enviada.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
