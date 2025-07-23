
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import os

API_TOKEN = "8046270772:AAHB7LBn9etmJK2c14fcrSQxZLgyqmY71AU"
GROUP_ID = -1002783169217

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    texto = f"👋 Bienvenido/a, {message.from_user.full_name}!"
    await message.reply(texto)

@dp.message_handler(commands=['ayuda'])
async def cmd_ayuda(message: types.Message):
    await bot.send_message(GROUP_ID, f"📢 Solicitud de ayuda enviada por: @{message.from_user.username or message.from_user.full_name}")
    await message.reply("✅ Solicitud de ayuda enviada.")

@dp.message_handler(commands=['staff'])
async def cmd_staff(message: types.Message):
    chat = await bot.get_chat_administrators(GROUP_ID)
    texto = "👮 Lista de administradores:

"
    keyboard = InlineKeyboardMarkup()
    for admin in chat:
        user = admin.user
        if user.username:
            texto += f"• @{user.username}
"
            keyboard.add(InlineKeyboardButton(text=f"Enviar mensaje a @{user.username}", url=f"https://t.me/{user.username}"))
        else:
            texto += f"• {user.full_name} (sin username)
"
    await message.reply(texto, reply_markup=keyboard)

@dp.message_handler(lambda message: any(entity.type == "mention" for entity in message.entities or []))
async def mention_notify(message: Message):
    chat_admins = await bot.get_chat_administrators(message.chat.id)
    mentions = [entity for entity in message.entities if entity.type == "mention"]
    for entity in mentions:
        mention_text = message.text[entity.offset:entity.offset + entity.length]
        for admin in chat_admins:
            user = admin.user
            if user.username and f"@{user.username}" == mention_text:
                try:
                    await bot.send_message(user.id, f"🔔 Has sido mencionado en un mensaje:

{message.text}")
                except Exception:
                    pass

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
