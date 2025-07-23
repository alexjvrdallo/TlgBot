
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, ChatMemberHandler

TOKEN = os.getenv("TU_TOKEN")
if not TOKEN:
    raise RuntimeError("No se encontró el TOKEN en las variables de entorno.")

BIENVENIDA = "👋 Bienvenido/a {name}!"
REGLAS = "📌 Reglas del grupo:
1. Sé respetuoso.
2. No spam ni enlaces.
3. Sigue las instrucciones de los admins."

PALABRAS_PROHIBIDAS = ["spam", "http", "www", "t.me", "idiota", "estúpido", "mierda"]

async def bienvenida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        text = f"👋 Bienvenido/a {member.full_name}!"
        await update.message.reply_text(text)
        await update.message.reply_text(REGLAS)

async def filtrar_mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()
    if any(palabra in texto for palabra in PALABRAS_PROHIBIDAS):
        await update.message.delete()
        await update.message.reply_text("⚠️ Tu mensaje fue eliminado por infringir las reglas.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(ChatMemberHandler(bienvenida, ChatMemberHandler.CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), filtrar_mensajes))
    app.run_polling()

if __name__ == "__main__":
    main()
