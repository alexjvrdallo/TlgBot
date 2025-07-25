Dijiste:
import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Obtener el token del entorno
TOKEN = os.getenv("BOT_TOKEN")

# Configuración de logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
         "🎉 ¡Bienvenido/a al grupo TrustDelivery 🎉\n"

"Hola y gracias por unirte a nuestra comunidad. Estamos muy contentos de tenerte aquí. Antes de comenzar, por favor tómate un momento para leer nuestras reglas para mantener un ambiente respetuoso y productivo para todos:\n"

"📌 Reglas del grupo:\n"

"Respeto ante todo: no se toleran insultos, lenguaje ofensivo ni discriminación.\n"

"Nada de spam, promociones o enlaces sin autorización.\n"

"Evita mensajes repetitivos, cadenas o contenido no relacionado.\n"

"Las decisiones de los administradores son finales. Si tienes dudas, puedes contactarlos.\n"

"🔧 Usa el comando /reglas para ver las reglas en cualquier momento.\n"

"👮‍♂ Usa el comando /staff para ver la lista de administradores del grupo.\n"

"🚨 Este grupo cuenta con un sistema automático de advertencias. Las faltas a las reglas serán sancionadas con:\n"

"1ª advertencia: recordatorio de las normas.\n"

"2ª advertencia: los administradores serán notificados.\n"

"3ª advertencia: silenciamiento temporal.\n"

"🤖 Además, el bot detectará groserías, spam y comportamientos sospechosos.\n"
"Usuarios reincidentes que intenten reingresar con otro nombre serán detectados y notificados a los administradores.\n"
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

# /reglas
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

# /ayuda
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

# /staff
async def staff(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    admins = await context.bot.get_chat_administrators(chat.id)
    admin_list = "\n".join([
        f"• {admin.user.first_name} (@{admin.user.username})"
        if admin.user.username else f"• {admin.user.first_name}"
        for admin in admins
    ])
    await update.message.reply_text(f"<b>Administradores del grupo:</b>\n{admin_list}", parse_mode="HTML")

# 🚪 Bienvenida automática
async def bienvenida(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for nuevo in update.message.new_chat_members:
        await update.message.reply_text(
            f"🎉 ¡Bienvenido/a al grupo TrustDelivery 🎉\n"

"Hola y gracias por unirte a nuestra comunidad. Estamos muy contentos de tenerte aquí. Antes de comenzar, por favor tómate un momento para leer nuestras reglas para mantener un ambiente respetuoso y productivo para todos:\n"

"📌 Reglas del grupo:\n"

"Respeto ante todo: no se toleran insultos, lenguaje ofensivo ni discriminación.\n"

"Nada de spam, promociones o enlaces sin autorización.\n"

"Evita mensajes repetitivos, cadenas o contenido no relacionado.\n"

"Las decisiones de los administradores son finales. Si tienes dudas, puedes contactarlos.\n"

"🔧 Usa el comando /reglas para ver las reglas en cualquier momento.\n"

"👮‍♂ Usa el comando /staff para ver la lista de administradores del grupo.\n"

"🚨 Este grupo cuenta con un sistema automático de advertencias. Las faltas a las reglas serán sancionadas con:\n"

"1ª advertencia: recordatorio de las normas.\n"

"2ª advertencia: los administradores serán notificados.\n"

"3ª advertencia: silenciamiento temporal.\n"

"🤖 Además, el bot detectará groserías, spam y comportamientos sospechosos.\n"
"Usuarios reincidentes que intenten reingresar con otro nombre serán detectados y notificados a los administradores.\n"
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

# /reglas
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

# 🔁 Lanzador
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    # Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reglas", reglas))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CommandHandler("staff", staff))

    # Detectar nuevos miembros
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, bienvenida))

    # Iniciar el bot
    app.run_polling()

