
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Lista de administradores
admins = [
    {"nombre": "Admin 1", "contacto": "@admin1"},
    {"nombre": "Admin 2", "contacto": "@admin2"}
]

# Mensaje de bienvenida
@dp.message_handler(commands=["start"])
async def cmd_start(message: Message):
    await message.reply("¡Hola y gracias por unirte a nuestra comunidad. Estamos muy contentos de tenerte aquí. "
                        "Antes de comenzar, por favor tómate un momento para leer nuestras reglas para mantener "
                        "un ambiente respetuoso y productivo para todos:

Usa /reglas para verlas.

"
                        "Si necesitas ayuda, puedes usar /ayuda.")

# Reglas
@dp.message_handler(commands=["reglas"])
async def cmd_reglas(message: Message):
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

# Staff
@dp.message_handler(commands=["staff"])
async def cmd_staff(message: Message):
    respuesta = "👤 Lista de administradores:
"
    for admin in admins:
        respuesta += f"- {admin['nombre']} ({admin['contacto']})
"
    await message.reply(respuesta)

# Ayuda
@dp.message_handler(commands=["ayuda"])
async def cmd_ayuda(message: Message):
    await message.reply("📩 Un administrador será notificado para ayudarte.")
    for admin in admins:
        try:
            await bot.send_message(admin["contacto"], f"El usuario @{message.from_user.username} ha solicitado ayuda en el grupo.")
        except:
            pass  # en caso de que el bot no pueda enviar mensaje privado

if __name__ == "__main__":
    executor.start_polling(dp)
