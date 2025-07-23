
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Configurar logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Reglas del grupo
REGLAS = (
    "🚫 No se permiten insultos ni lenguaje ofensivo.\n"
    "🚫 No se permite SPAM ni enlaces a otros grupos o canales.\n"
    "✅ Respeta a los demás miembros.\n"
    "✅ Usa el grupo solo para su propósito específico.\n"
    "Si tienes dudas, contacta a un administrador."
)

# Mensaje de bienvenida
async def bienvenida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for miembro in update.message.new_chat_members:
        await update.message.reply_text(
            f"👋 Bienvenido/a {miembro.full_name} al grupo!\n\n{REGLAS}"
        )

# Filtrar SPAM o groserías (puedes editar la lista)
PALABRAS_PROHIBIDAS = ["spam", "grosería", "http", "www"]

async def filtrar_mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()
    if any(palabra in texto for palabra in PALABRAS_PROHIBIDAS):
        try:
            await update.message.delete()
            await update.message.reply_text("🚫 Ese mensaje ha sido eliminado por infringir las reglas.")
        except Exception as e:
            logging.warning(f"No se pudo borrar el mensaje: {e}")

# Inicializar el bot
async def main():
    token = os.getenv("TOKEN")
    if not token:
        raise RuntimeError("No se encontró el TOKEN en las variables de entorno.")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, bienvenida))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filtrar_mensajes))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
