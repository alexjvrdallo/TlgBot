
import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("No se encontró el TOKEN en las variables de entorno.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy tu bot de grupo de Telegram.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    # Ejecutar sin cerrar el loop existente
    app.run_polling()

if __name__ == "__main__":
    main()
