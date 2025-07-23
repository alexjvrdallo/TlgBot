
import os
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import logging

# Configurar logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Token desde variable de entorno
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("❌ No se encontró la variable TOKEN en Railway.")

# Palabras prohibidas y enlaces que se consideran spam
PROHIBIDAS = ["grosería", "insulto", "http", "www", "t.me", ".com", "oferta", "promo"]
REGLAS = (
    "📌 *Reglas del grupo:*
"
    "- No decir malas palabras
"
    "- No Spam de ningún tipo
"
    "- No hablar de precios en ningún grupo"
)

# Mensaje de bienvenida
async def bienvenida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for miembro in update.message.new_chat_members:
        await update.message.reply_text(
            f"👋 Bienvenido/a {miembro.full_name} al grupo.

{REGLAS}",
            parse_mode="Markdown"
        )

# Filtro de contenido
async def moderar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.message
    texto = mensaje.text.lower()

    if any(p in texto for p in PROHIBIDAS):
        try:
            await mensaje.delete()
            await mensaje.reply_text("🚫 Ese mensaje fue eliminado por infringir las reglas.")
        except Exception as e:
            logging.warning(f"No se pudo borrar mensaje: {e}")

# Arranque del bot
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Mensajes nuevos en grupo (bienvenida)
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, bienvenida))
    # Filtro de mensajes de texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, moderar))

    print("✅ Bot en funcionamiento. Esperando mensajes...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
