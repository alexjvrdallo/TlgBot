import os
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, ContextTypes
import asyncio

GROUP_RULES = "Reglas del grupo: No spam, no enlaces, respeta a los demás."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola, soy el bot del grupo.")

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"👋 Bienvenido/a {member.full_name}!
{GROUP_RULES}"
        )

async def filter_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "http://" in update.message.text or "https://" in update.message.text:
        await update.message.delete()
        await update.message.reply_text("❌ No se permiten enlaces.")

def main():
    TOKEN = os.getenv("TOKEN")
    if not TOKEN:
        raise RuntimeError("No se encontró el TOKEN en las variables de entorno.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), filter_links))

    print("Bot iniciado.")
    app.run_polling()

if __name__ == "__main__":
    main()
