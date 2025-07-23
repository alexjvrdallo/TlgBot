import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Lista de administradores
ADMIN_USERS = [
    {"nombre": "Alex", "contacto": "@AlexAdmin"},
    {"nombre": "Sofía", "contacto": "@SofiaAdmin"}
]

# Comando /start
@dp.message_handler(commands=["start"])
async def start_cmd(message: Message):
    await message.reply("¡Hola y gracias por unirte a nuestra comunidad. Estamos muy contentos de tenerte aquí. Antes de comenzar, por favor tómate un momento para leer nuestras reglas para mantener un ambiente respetuoso y productivo para todos:

Usa /reglas para ver las reglas del grupo.
Si necesitas ayuda, escribe /ayuda para contactar a los administradores.")

# Comando /reglas
@dp.message_handler(commands=["reglas"])
async def reglas_cmd(message: Message):
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

# Comando /staff
@dp.message_handler(commands=["staff"])
async def staff_cmd(message: Message):
    staff = "👮 Lista de administradores:
" + "
".join([f"- {admin['nombre']}: {admin['contacto']}" for admin in ADMIN_USERS])
    await message.reply(staff)

# Comando /ayuda
@dp.message_handler(commands=["ayuda"])
async def ayuda_cmd(message: Message):
    aviso = f"🚨 El usuario @{message.from_user.username} ha solicitado ayuda en el grupo."
    for admin in ADMIN_USERS:
        try:
            await bot.send_message(chat_id=admin["contacto"], text=aviso)
        except:
            pass
    await message.reply("✅ Los administradores han sido notificados. Te contactarán pronto.")

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
