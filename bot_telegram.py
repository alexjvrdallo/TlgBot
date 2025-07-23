import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from aiogram.dispatcher.filters import Command

API_TOKEN = "8046270772:AAHB7LBn9etmJK2c14fcrSQxZLgyqmY71AU"
GROUP_ID = -1002783169217

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

ADMINS = {
    123456789: "Admin1",
    987654321: "Admin2"
}

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    texto = f"👋 Bienvenido/a, {message.from_user.full_name}!

"
    texto += "Gracias por unirte al grupo. Para contactar con los administradores, usa el comando /ayuda.
"
    texto += "Puedes ver la lista de administradores con /staff."
    await message.reply(texto)

@dp.message_handler(commands=["ayuda"])
async def help_command(message: Message):
    await bot.send_message(GROUP_ID, f"📣 Solicitud de ayuda enviada por: {message.from_user.full_name} (@{message.from_user.username})")
    await message.reply("✅ Solicitud de ayuda enviada.")

@dp.message_handler(commands=["staff"])
async def list_admins(message: Message):
    texto = "👮 Lista de administradores:

"
    for admin_id, name in ADMINS.items():
        texto += f"• {name} - [Enviar mensaje](tg://user?id={admin_id})
"
    await message.reply(texto, parse_mode="Markdown")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)