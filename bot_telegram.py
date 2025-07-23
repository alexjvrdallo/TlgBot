import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola y gracias por unirte a nuestra comunidad. Estamos muy contentos de tenerte aquí. "
        "Antes de comenzar, por favor tómate un momento para leer nuestras reglas para mantener "
        "un ambiente respetuoso y productivo para todos:\n\nUsa /reglas para verlas.\n"
        "Si necesitas ayuda, escribe /ayuda."
    )

async def reglas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Reglas del grupo:\n"
        "1. Prohibido dar precios en público.\n"
        "2. Respeto ante todo: no se toleran insultos, lenguaje ofensivo ni discriminación.\n"
        "3. Nada de spam, promociones o enlaces sin autorización.\n"
        "4. Evita mensajes repetitivos, cadenas o contenido no relacionado.\n"
        "5. Las decisiones de los administradores son finales. Si tienes dudas, puedes contactarlos."
    )

async def staff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👥 Lista de administradores:\n"
        "• Admin 1: @Admin1\n"
        "• Admin 2: @Admin2"
    )

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔔 Un administrador ha sido notificado.")
    admin_usernames = ["@Admin1", "@Admin2"]
    for username in admin_usernames:
        try:
            await context.bot.send_message(chat_id=username, text="🚨 Un usuario ha solicitado ayuda en el grupo.")
        except Exception as e:
            print(f"Error al enviar mensaje a {username}: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("reglas", reglas))
app.add_handler(CommandHandler("staff", staff))
app.add_handler(CommandHandler("ayuda", ayuda))

app.run_polling()
