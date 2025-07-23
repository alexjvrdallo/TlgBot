import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_IDS = [123456789, 987654321]  # Reemplaza con los IDs reales
ADMIN_CONTACTS = ["@admin1", "@admin2"]

WELCOME_MESSAGE = (
    "¡Hola y gracias por unirte a nuestra comunidad. Estamos muy contentos de tenerte aquí. "
    "Antes de comenzar, por favor tómate un momento para leer nuestras reglas para mantener un ambiente "
    "respetuoso y productivo para todos:

Usa /reglas para ver las reglas y /ayuda si necesitas asistencia."
)

REGLAS = (
    "📌 Reglas del grupo:
"
    "1. Prohibido dar precios en público.
"
    "2. Respeto ante todo: no se toleran insultos, lenguaje ofensivo ni discriminación.
"
    "3. Nada de spam, promociones o enlaces sin autorización.
"
    "4. Evita mensajes repetitivos, cadenas o contenido no relacionado.
"
    "5. Las decisiones de los administradores son finales. Si tienes dudas, puedes contactarlos."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)

async def reglas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(REGLAS)

async def staff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "\n".join(ADMIN_CONTACTS)
    await update.message.reply_text(f"📋 Lista de administradores:\n{lista}")

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(chat_id=admin_id, text=f"🆘 Un usuario ha solicitado ayuda desde el grupo {update.effective_chat.title}.")
        except Exception as e:
            logging.error(f"Error al enviar mensaje al admin: {e}")
    await update.message.reply_text("✅ Los administradores han sido notificados y te contactarán pronto.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reglas", reglas))
    app.add_handler(CommandHandler("staff", staff))
    app.add_handler(CommandHandler("ayuda", ayuda))

    app.run_polling()