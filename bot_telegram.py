import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

ADMIN_IDS = [123456789, 987654321]  # Reemplaza con los IDs reales de los administradores

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply(
        "¡Hola y gracias por unirte a nuestra comunidad. Estamos muy contentos de tenerte aquí. "
        "Antes de comenzar, por favor tómate un momento para leer nuestras reglas para mantener "
        "un ambiente respetuoso y productivo para todos:\n
"
        "Usa /reglas para ver las reglas y /ayuda si necesitas contactar al staff."
    )

@dp.message_handler(commands=["reglas"])
async def reglas_handler(message: types.Message):
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

@dp.message_handler(commands=["staff"])
async def staff_handler(message: types.Message):
    staff_info = (
        "👮 Lista de administradores:
"
        "• Admin 1: @admin1
"
        "• Admin 2: @admin2
"
        "Puedes contactarlos si necesitas ayuda."
    )
    await message.reply(staff_info)

@dp.message_handler(commands=["ayuda"])
async def ayuda_handler(message: types.Message):
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, f"🚨 Un usuario solicitó ayuda en el grupo: @{message.chat.username or 'sin username'}")
        except:
            pass
    await message.reply("✅ Los administradores han sido notificados. Pronto te responderán.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
