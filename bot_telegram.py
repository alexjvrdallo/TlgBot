
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatMemberUpdated
from aiogram.filters import ChatMemberUpdatedFilter

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("No se encontró el TOKEN en las variables de entorno.")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.chat_member(ChatMemberUpdatedFilter(member_status_changed=True))
async def on_user_join(event: ChatMemberUpdated):
    member = event.new_chat_member
    if member.status == "member":
        await bot.send_message(
            chat_id=event.chat.id,
            text=f"👋 Bienvenido/a {member.user.full_name}!"
        )

@dp.message()
async def on_message(message: types.Message):
    if message.text and "reglas" in message.text.lower():
        await message.answer("📌 Reglas del grupo:
1. Respeto
2. No spam
3. Seguir las normas de Telegram.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
