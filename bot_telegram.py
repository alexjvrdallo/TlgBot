import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [123456789, 987654321]  # Reemplaza con los ID reales de los administradores

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola y gracias por unirte a nuestra comunidad. Estamos muy contentos de tenerte aquí. "
        "Antes de comenzar, por favor tómate un momento para leer nuestras reglas para mantener un ambiente "
        "respetuoso y productivo para todos:\n\nEscribe /reglas para verlas. Si necesitas ayuda, escribe /ayuda."
    )

async def staff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👨‍💼 Lista de administradores:\n- Admin1: @admin1\n- Admin2: @admin2"
    )

async def reglas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📜 Reglas del grupo:\n"
        "1. Respeto mutuo entre todos los miembros.\n"
        "2. No se permiten mensajes ofensivos, discriminatorios o violentos.\n"
        "3. Evita el spam o la promoción sin permiso de los administradores.\n"
        "4. Usa los canales adecuados para cada tema.\n"
        "5. Si necesitas ayuda, usa /ayuda para contactar a los administradores."
    )

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(chat_id=admin_id, text=f"🔔 El usuario @{update.effective_user.username} ha solicitado ayuda.")
        except:
            pass
    await update.message.reply_text("✅ Tu solicitud de ayuda ha sido enviada a los administradores.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("staff", staff))
    app.add_handler(CommandHandler("reglas", reglas))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.run_polling()
