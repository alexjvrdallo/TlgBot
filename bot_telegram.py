
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Mensaje de bienvenida al entrar al grupo
@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def welcome_new_member(message: types.Message):
    for user in message.new_chat_members:
        texto = f"👋 Bienvenido/a, {user.full_name}!"
        await message.reply(texto)

# Comando /start
@dp.message_handler(commands=["start"])
async def start_command(message: Message):
    await message.reply("🤖 Bot activado y listo para recibir comandos.")

# Comando /ayuda
@dp.message_handler(commands=["ayuda"])
async def ayuda_command(message: Message):
    await bot.send_message(GROUP_ID, f"🚨 El usuario @{message.from_user.username} ha solicitado ayuda.")
    await message.reply("🚨 Solicitud de ayuda enviada.")

# Comando /staff
@dp.message_handler(commands=["staff"])
async def staff_command(message: Message):
    await message.reply("👨‍💼 Lista de administradores:
- Admin 1
- Admin 2")

# Comando /reglas
@dp.message_handler(commands=["reglas"])
async def reglas_command(message: Message):
    await message.reply("📜 Reglas del grupo:
1. Respeta a los demás.
2. No spam.
3. Sigue las instrucciones del staff.")

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
