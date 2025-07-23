from aiogram import Bot, Dispatcher, executor, types
import logging
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

if not API_TOKEN:
    raise ValueError("API_TOKEN not found in .env")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

ADMIN_IDS = ["123456789", "987654321"]  # Reemplaza con los IDs reales

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("¡Hola y gracias por unirte a nuestra comunidad. Estamos muy contentos de tenerte aquí. Antes de comenzar, por favor tómate un momento para leer nuestras reglas para mantener un ambiente respetuoso y productivo para todos:

Usa /reglas para ver las reglas del grupo.
Si necesitas ayuda, escribe /ayuda para notificar a los administradores.")

@dp.message_handler(commands=["reglas"])
async def send_rules(message: types.Message):
    reglas = (
        "<b>📌 Reglas del grupo:</b>
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
async def send_admins(message: types.Message):
    admins = (
        "<b>👥 Administradores:</b>
"
        "• Alex - <a href='tg://user?id=123456789'>Enviar mensaje</a>
"
        "• Carla - <a href='tg://user?id=987654321'>Enviar mensaje</a>"
    )
    await message.reply(admins)

@dp.message_handler(commands=["ayuda"])
async def notify_admins(message: types.Message):
    grupo = message.chat.id
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, f"🆘 El usuario @{message.from_user.username} solicitó ayuda en el grupo con ID {grupo}.")
        except Exception as e:
            logging.error(f"No se pudo enviar mensaje a {admin_id}: {e}")
    await message.reply("✅ Se ha notificado a los administradores. Pronto te responderán.")

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)