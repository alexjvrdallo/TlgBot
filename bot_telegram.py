import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
from aiogram.utils.markdown import hbold

API_TOKEN = "8046270772:AAHB7LBn9etmJK2c14fcrSQxZLgyqmY71AU"
GROUP_ID = -1002783169217

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)

# Lista de administradores con nombres y user IDs
ADMINISTRADORES = [
    {"id": 123456789, "nombre": "Carlos"},
    {"id": 987654321, "nombre": "María"}
]

PALABRAS_PROHIBIDAS = ["maldito", "mardito", "idiota", "estúpido"]

@dp.message_handler(commands=['start'])
async def enviar_bienvenida(message: types.Message):
    texto = (
        f"👋 Bienvenido/a, {message.from_user.full_name}!

"
        "📌 Asegúrate de respetar las reglas del grupo para mantener un ambiente sano:
"
        "1. Respeto entre miembros.
"
        "2. No spam.
"
        "3. Uso del comando /ayuda en caso de emergencia.

"
        "Si necesitas algo, usa /ayuda para notificar a los administradores."
    )
    await message.reply(texto)

@dp.message_handler(commands=["ayuda"])
async def comando_ayuda(message: types.Message):
    for admin in ADMINISTRADORES:
        try:
            await bot.send_message(admin["id"], f"🆘 Solicitud de ayuda enviada.
Usuario: @{message.from_user.username or message.from_user.full_name}")
        except:
            pass
    await message.reply("📨 Tu solicitud ha sido enviada a los administradores.")

@dp.message_handler(commands=["staff"])
async def comando_staff(message: types.Message):
    texto = "<b>👮 Lista de administradores:</b>
"
    for admin in ADMINISTRADORES:
        texto += f"• <a href='tg://user?id={admin['id']}'>{admin['nombre']}</a>
"
    await message.reply(texto, parse_mode=ParseMode.HTML)

@dp.message_handler()
async def monitorear_mensajes(message: types.Message):
    contenido = message.text.lower()
    if any(palabra in contenido for palabra in PALABRAS_PROHIBIDAS):
        for admin in ADMINISTRADORES:
            try:
                await bot.send_message(admin["id"], f"🚨 Posible mensaje ofensivo:
Usuario: @{message.from_user.username or message.from_user.full_name}
Contenido: {message.text}")
            except:
                pass
