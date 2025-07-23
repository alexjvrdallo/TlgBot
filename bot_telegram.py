import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hola y gracias por unirte a nuestra comunidad. Estamos muy contentos de tenerte aquí.\n"
        "Antes de comenzar, por favor tómate un momento para leer nuestras reglas para mantener un ambiente respetuoso y productivo para todos:\n"
        "\n"
        "1. Respeto mutuo: Trata a todos los miembros con cortesía. No se tolerará lenguaje ofensivo, discriminación o acoso.\n"
        "2. Contenido apropiado: Comparte solo contenido relacionado con el propósito del grupo. Evita spam, publicidad no autorizada o material inapropiado.\n"
        "3. Privacidad: No compartas información personal tuya ni de otros sin consentimiento.\n"
        "4. Colaboración: Si tienes preguntas, dudas o aportes, compártelos con respeto.\n"
        "5. Moderación: Los administradores están para ayudar. Si necesitas asistencia, usa /ayuda.\n"
        "\n"
        "🆘 En cualquier momento puedes escribir /ayuda para contactar a los administradores.\n"
        "Gracias por formar parte de esta comunidad."
    )

async def reglas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "<b>Reglas del grupo:</b>\n"
        "1. Respeto mutuo entre todos los miembros.\n"
        "2. No se permite spam, contenido ofensivo o discriminatorio.\n"
        "3. Mantener el enfoque del grupo.\n"
        "4. No compartir información personal.\n"
        "5. Usa /ayuda si necesitas asistencia.",
        parse_mode="HTML"
    )

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    admins = await context.bot.get_chat_administrators(chat.id)
    mensaje = f"🔔 El usuario @{update.effective_user.username or update.effective_user.first_name} ha solicitado ayuda en el grupo {chat.title}."

    for admin in admins:
        try:
            await context.bot.send_message(chat_id=admin.user.id, text=mensaje)
        except:
            pass

    await update.message.reply_text("✅ Hemos notificado a los administradores. Pronto te contactarán.")

async def staff(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    admins = await context.bot.get_chat_administrators(chat.id)
    admin_list = "\n".join([f"• {admin.user.first_name} (@{admin.user.username})" if admin.user.username else f"• {admin.user.first_name}" for admin in admins])
    await update.message.reply_text(f"<b>Administradores del grupo:</b>\n{admin_list}", parse_mode="HTML")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reglas", reglas))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CommandHandler("staff", staff))

    app.run_polling()
