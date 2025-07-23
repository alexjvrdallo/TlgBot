
import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, ChatMemberHandler

logging.basicConfig(level=logging.INFO)

REGLAS = """📌 Reglas del grupo:
1. Sé respetuoso.
2. No spam.
3. Usa el grupo con responsabilidad."""

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chat_member
    if result.new_chat_member.status == "member":
        member = result.new_chat_member.user
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"👋 Bienvenido/a {member.full_name}!")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=REGLAS)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass  # Aquí puedes manejar mensajes si quieres

async def main():
    token = os.getenv("TU_TOKEN")
    if not token:
        raise RuntimeError("No se encontró el TOKEN en las variables de entorno.")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
