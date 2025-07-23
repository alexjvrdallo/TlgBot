
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

REGLAS = (
    "📌 Reglas del grupo:\n"
    "1. No spam\n"
    "2. Respeta a los demás\n"
    "3. Prohibido contenido ilegal"
)

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = update.message.new_chat_members[0]
    text = f"👋 Bienvenido/a {member.full_name}!"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=REGLAS)

if __name__ == "__main__":
    import os
    import asyncio

    async def main():
        token = os.getenv("TU_TOKEN")
        if not token:
            raise RuntimeError("No se encontró el TOKEN en las variables de entorno.")

        app = ApplicationBuilder().token(token).build()
        app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
        await app.run_polling()

    asyncio.run(main())
