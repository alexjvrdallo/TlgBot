import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatMemberUpdated
from aiogram.filters import ChatMemberUpdatedFilter

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise RuntimeError("No se encontró el TOKEN en las variables de entorno.")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Log de bienvenida
@dp.chat_member(ChatMemberUpdatedFilter(member_status_changed=True))
async def on_user_join(event: ChatMemberUpdated, bot: Bot):
    if event.new_chat_member.status == "member":
        full_name = event.new_chat_member.user.full_name
        await bot.send_message(event.chat.id, f"👋 ¡Bienvenido/a {full_name}!")
        print(f"Nuevo usuario: {full_name}")

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Bot iniciado correctamente.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())